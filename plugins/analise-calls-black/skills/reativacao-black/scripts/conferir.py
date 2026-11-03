#!/usr/bin/env python3
"""Confere os arquivos gerados pela skill reativacao-black.

Uso:
    python3 conferir.py <pasta_saida>

Para cada <lead>.md da pasta (menos os que começam com "_"):
  - as falas citadas em "Base da mensagem" existem na transcrição, perto da linha indicada;
  - tamanho das mensagens (mensagem 1 até 70 palavras, mensagem 2 até 170; limites provisórios);
  - mensagem 1 com pelo menos três bullets e três "Problema" citados na base;
  - número na mensagem 1 só se estiver nas falas citadas (a meta do lead);
  - formato do WhatsApp: *negrito* com um asterisco; asterisco duplo é erro;
  - nada de preço, percentual, prazo, urgência, palavra proibida ou travessão nos balões;
  - "mentoria"/"consultoria" fora das mensagens;
  - mensagem 2 termina com a sugestão de horário e indica o PDF;
  - mensagem 1 usa pelo menos uma palavra das falas do lead (sinal de que não está genérica).

Saída: um relatório por lead, com ERRO (corrigir antes de entregar) e AVISO (olhar).
Código de saída 1 se houver algum ERRO.
"""
import re
import sys
import unicodedata
from pathlib import Path

# Limites provisórios: revisar depois do reteste com o formato novo (meta + bullets + lista da Black).
LIMITE_M1 = 70
LIMITE_M2 = 170

PROIBIDAS = [
    "alavancar", "alavanque", "potencializar", "potencialize", "framework", "destrave seu potencial",
    "mindset", "jornada", "transformacao", "transforme", "imperdivel", "incrivel oportunidade",
    "otimizar", "robusta", "sinergia", "prezado", "venho por meio", "espero que esteja bem",
]
URGENCIA = ["ultimas vagas", "ultima chance", "so hoje", "so ate", "corre que", "acaba hoje", "vagas limitadas", "contagem regressiva"]
STOP = set("""a o e é de da do das dos em no na nos nas um uma uns umas que para pra por com sem se ser ter tem tinha
como mais mas muito muita isso esse essa este esta aqui ali lá ele ela eles elas eu você voce vocês voces a gente gente
nós nos não nao sim já ja só so porque quando onde qual quais então entao assim tá ta né ne pro pra coisa coisas fazer
hoje agora vai vou foi era está estava estão estao meu minha seu sua nosso nossa""".split())


def norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s)).strip()


def palavras(s: str):
    return re.findall(r"[A-Za-zÀ-ÿ0-9$%]+(?:[.,][0-9]+)?", s)


def secoes(md: str):
    out, atual = {}, None
    for l in md.split("\n"):
        if l.startswith("## "):
            atual = l[3:].strip().lower()
            out[atual] = []
        elif atual is not None:
            out[atual].append(l)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def achar(secs, prefixo):
    for k, v in secs.items():
        if k.startswith(prefixo):
            return v
    return None


def baloes(txt: str):
    linhas = [l for l in txt.split("\n") if not re.match(r"\s*(Se (ele|ela|o lead) responder|Enviar junto)", l)]
    return "\n".join(linhas).strip()


def carregar_transcricao(caminho: str):
    p = Path(caminho.strip())
    if not p.exists():
        return None
    linhas = {}
    for l in p.read_text(encoding="utf-8", errors="ignore").split("\n"):
        n, _, t = l.partition("|")
        if n.isdigit():
            linhas[int(n)] = t
    return linhas


def trigramas(ws):
    return {tuple(ws[i:i + 3]) for i in range(len(ws) - 2)}


def conferir_citacao(cit: str, linha: int, transc: dict):
    """Procura a citação na janela da linha indicada e no arquivo todo."""
    alvo = norm(cit).split()
    if len(alvo) < 3:
        return "curta demais para conferir", None
    tg = trigramas(alvo)

    def melhor(janela_ids):
        texto = norm(" ".join(transc.get(i, "") for i in janela_ids)).split()
        if not texto:
            return 0.0
        return len(tg & trigramas(texto)) / max(1, len(tg))

    perto = melhor(range(max(1, linha - 4), linha + 5)) if linha else 0.0
    if perto >= 0.8:
        return None, perto
    ids = sorted(transc)
    best, best_i = 0.0, None
    for j in range(0, len(ids), 3):
        sc = melhor(ids[j:j + 8])
        if sc > best:
            best, best_i = sc, ids[j]
    if best >= 0.8:
        return f"está na transcrição, mas perto da linha {best_i}, não da {linha}", best
    return f"não encontrada na transcrição (melhor semelhança {best:.0%})", best


def conferir_arquivo(p: Path):
    erros, avisos = [], []
    md = p.read_text(encoding="utf-8")
    secs = secoes(md)

    m_call = re.search(r"transcri[cç][aã]o:\s*(.+)", md)
    transc = carregar_transcricao(m_call.group(1)) if m_call else None
    if transc is None:
        erros.append("não achei a transcrição indicada na linha 'Call:'")

    m1 = achar(secs, "mensagem 1")
    m2 = achar(secs, "mensagem 2")
    base = achar(secs, "base da mensagem") or ""
    status = re.search(r"Status:\s*(.+)", md)
    revisar = bool(status and "REVISAR" in status.group(1).upper())

    for nome, txt, lim in (("mensagem 1", m1, LIMITE_M1), ("mensagem 2", m2, LIMITE_M2)):
        if txt is None:
            if not revisar:
                erros.append(f"{nome}: seção não encontrada")
            continue
        b = baloes(txt)
        n = len(palavras(b))
        if n > lim:
            erros.append(f"{nome}: {n} palavras (limite {lim})")
        nb = norm(b)
        for w in PROIBIDAS:
            if re.search(r"\b" + w + r"\b", nb):
                erros.append(f"{nome}: palavra proibida '{w}'")
        for w in URGENCIA:
            if re.search(r"\b" + w + r"\b", nb):
                erros.append(f"{nome}: urgência '{w}'")
        if re.search(r"\bmentoria\b|\bconsultoria\b", nb):
            erros.append(f"{nome}: usa 'mentoria' ou 'consultoria' (o produto é 'programa')")
        if re.search(r"\d+\s*%|\b\d+\s*x\b|\bparcelas? de\b|\b12 vezes\b", b, re.I):
            achados = re.findall(r"\d+\s*%|\b\d+\s*x\b|\bparcelas? de\b|\b12 vezes\b", b, re.I)
            erros.append(f"{nome}: tem percentual ou parcela {achados}: preço e desconto ficam para a conversa")
        base_digitos = set(re.findall(r"\d+", re.sub(r"(?<=\d)[.,](?=\d)", "", base)))
        for num in re.findall(r"\d+(?:[.,]\d+)*", b):
            limpo = re.sub(r"[.,]", "", num)
            if nome == "mensagem 2" and re.fullmatch(r"20(26|27)|5|2|1", limpo):
                continue  # 2027, 5x2, NR-1, +2 meses: texto fixo da condição
            if limpo not in base_digitos:
                (erros if nome == "mensagem 1" else avisos).append(
                    f"{nome}: o número '{num}' não aparece nas falas citadas em 'Base da mensagem': só número dito pelo lead")
        if "—" in b or "–" in b:
            erros.append(f"{nome}: tem travessão")
        if "**" in b:
            erros.append(f"{nome}: asterisco duplo: no WhatsApp o negrito é *texto*, com um asterisco")
        if re.search(r"^\s*#|^\s*\|", b, re.M):
            erros.append(f"{nome}: tem título ou tabela de markdown no balão")
        bullets = re.findall(r"^\s*[-•]\s+(.+)$", b, re.M)
        if any("*" not in x for x in bullets):
            avisos.append(f"{nome}: bullet sem negrito")
        if nome == "mensagem 1" and len(bullets) < 3 and not revisar:
            erros.append(f"mensagem 1: {len(bullets)} bullet(s); são pelo menos três problemas do lead")
        if nome == "mensagem 2" and len(bullets) < 3 and not revisar:
            avisos.append("mensagem 2: sem a lista da condição de Black em bullets")
        if b.count("!") > 1:
            avisos.append(f"{nome}: {b.count('!')} exclamações")
        if nome == "mensagem 1" and b.count("?") == 0:
            avisos.append("mensagem 1: não termina com pergunta")
        if nome == "mensagem 2":
            ultimo = [x for x in b.split("\n\n") if x.strip()][-1] if b.strip() else ""
            if "?" not in ultimo or not re.search(r"apresent|convers|mostrar|falar", norm(ultimo)):
                avisos.append("mensagem 2: o último balão não é a sugestão de dia e horário")
            if not re.search(r"Enviar junto:.*PDF", txt):
                avisos.append("mensagem 2: falta a linha 'Enviar junto: PDF da Condição Black.'")

    resumo = achar(secs, "para o iago") or ""
    for item in re.findall(r"^-\s*(.+)$", resumo, re.M):
        n = len(palavras(item))
        if n > 45:
            avisos.append(f"resumo para o Iago: item com {n} palavras (até 35): \"{item[:50]}...\"")

    cits = re.findall(r'^-\s*([^:\n]+):\s*"(.+?)"\s*\(([\d:]+)?[^)]*?linha\s*(\d+)\)', base, re.M)
    if not cits and not revisar:
        erros.append("base da mensagem: nenhuma fala citada com linha")
    n_prob = sum(1 for r, *_ in cits if r.strip().lower().startswith("problema"))
    if n_prob < 3 and not revisar:
        erros.append(f"base da mensagem: {n_prob} 'Problema' citado(s) com linha; são pelo menos três")
    if transc:
        for rotulo, cit, _ts, ln in cits:
            prob, _ = conferir_citacao(cit, int(ln), transc)
            if prob:
                erros.append(f"citação '{rotulo.strip()}': {prob}: \"{cit[:80]}\"")

    if m1 and cits:
        lead_words = {w for _, c, _, _ in cits for w in norm(c).split() if len(w) > 3 and w not in STOP}
        m1_words = {w for w in norm(baloes(m1)).split() if len(w) > 3 and w not in STOP}
        if not (lead_words & m1_words):
            avisos.append("mensagem 1 não usa nenhuma palavra das falas citadas: conferir se está genérica")

    return erros, avisos, revisar


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    pasta = Path(sys.argv[1]).expanduser()
    arquivos = sorted(x for x in pasta.glob("*.md") if not x.name.startswith("_"))
    total_erros = 0
    for p in arquivos:
        erros, avisos, revisar = conferir_arquivo(p)
        total_erros += len(erros)
        marca = "OK" if not erros else "CORRIGIR"
        print(f"\n[{marca}] {p.name}{'  (status: REVISAR)' if revisar else ''}")
        for e in erros:
            print(f"  ERRO  {e}")
        for a in avisos:
            print(f"  AVISO {a}")
    print(f"\n{len(arquivos)} arquivo(s), {total_erros} erro(s).")
    sys.exit(1 if total_erros else 0)


if __name__ == "__main__":
    main()
