#!/usr/bin/env python3
"""Prepara as transcrições para a skill reativacao-black.

Uso:
    python3 preparar.py <pasta_com_transcricoes> [--saida <pasta_de_trabalho>]

Lê .txt, .md e .docx (anotações do Gemini exportadas do Google Docs), separa a
transcrição do resumo automático do Gemini, identifica data, lead, quem falou
e quanto cada um falou, agrupa calls do mesmo lead e grava:

    <saida>/_preparo/<lead>__<AAAA-MM-DD>.txt   transcrição limpa, com número de linha
    <saida>/_preparo/indice.json                um registro por lead
    <saida>/_preparo/indice.md                  a mesma coisa em tabela, para conferir

Só usa a biblioteca padrão do Python.
"""
import json
import re
import sys
import unicodedata
import zipfile
from collections import Counter, OrderedDict
from pathlib import Path

# Pessoas da Metta que aparecem como falantes nas calls. Quem tiver mais fala
# entre elas é quem apresentou a proposta.
METTA = {
    "iago paseto": "Iago",
    "iago": "Iago",
    "thiago caetano": "Thiago Caetano",
    "vanessa larissa lima": "Vanessa",
    "vanessa": "Vanessa",
    "tiago alves": "Tiago Alves",
    "silvio metta": "Silvio",
    "diana santana": "Diana",
    "karita de oliveira": "Kárita",
    "kárita de oliveira": "Kárita",
}

TS_RE = re.compile(r"^\s*(\d{2}:\d{2}:\d{2})\s*$")
SPK_RE = re.compile(r"^([^\s:][^:\n]{1,48}):\s+(.*)$")
FIM_RE = re.compile(r"encerrada após (\d{2}:\d{2}:\d{2})")
DATA_RE = re.compile(r"(20\d\d)[/_\-. ](\d\d)[/_\-. ](\d\d)")


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def chave(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", sem_acento(s).lower()).strip()


def ler_docx(p: Path) -> str:
    with zipfile.ZipFile(p) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab/>", "\t", xml)
    xml = re.sub(r"<w:br/>", "\n", xml)
    txt = re.sub(r"<[^>]+>", "", xml)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&apos;", "'")):
        txt = txt.replace(a, b)
    return txt


def ler(p: Path) -> str:
    if p.suffix.lower() == ".docx":
        return ler_docx(p)
    return p.read_text(encoding="utf-8", errors="ignore")


def separar_transcricao(txt: str):
    """Devolve (cabecalho, transcricao). O cabeçalho tem convidados e o resumo do Gemini."""
    linhas = txt.replace("\r", "").replace("\ufeff", "").split("\n")
    ini = None
    for i, l in enumerate(linhas):
        if "📖" in l or re.search(r"-\s*Transcri[cç][aã]o\s*$", l.strip()):
            ini = i
            break
    if ini is None:  # arquivo só com a transcrição
        return "", "\n".join(linhas)
    return "\n".join(linhas[:ini]), "\n".join(linhas[ini:])


def lead_do_nome(nome: str) -> str:
    base = re.sub(r"^[A-Z]+_", "", nome)  # cópias tipo IAGO_...
    base = base.replace("_", " ")
    partes = [x.strip() for x in re.split(r"\s+-\s+", base) if x.strip()]
    # padrão Gemini: "<Evento> - <Lead> - <data> - Anotações do Gemini"
    for i, p in enumerate(partes):
        if DATA_RE.search(p) and i > 0:
            cand = partes[i - 1]
            if not re.search(r"supere a met|anota|gemini|transcri", cand, re.I):
                return cand
    if len(partes) >= 2:
        return partes[1]
    return re.sub(r"\.(txt|md|docx)$", "", nome)


def analisar(p: Path):
    txt = ler(p)
    cab, tr = separar_transcricao(txt)
    falas = Counter()
    nomes_originais = {}
    for l in tr.split("\n"):
        m = SPK_RE.match(l.strip())
        if not m:
            continue
        spk = m.group(1).strip()
        if TS_RE.match(spk) or len(spk.split()) > 5 or re.search(r"presentation|apresenta[cç][aã]o de", spk, re.I):
            continue
        k = chave(spk)
        falas[k] += len(m.group(2))
        nomes_originais.setdefault(k, spk)
    total = sum(falas.values()) or 1
    metta_falas = {k: v for k, v in falas.items() if k in METTA or k.split(" ")[0] in ("iago", "vanessa")}
    apresentou = None
    if metta_falas:
        k = max(metta_falas, key=metta_falas.get)
        apresentou = METTA.get(k) or nomes_originais[k]
    lado_lead = {nomes_originais[k]: round(100 * v / total) for k, v in falas.most_common() if k not in metta_falas}
    fim = FIM_RE.findall(txt)
    tss = TS_RE.findall(tr) if False else re.findall(r"^\s*(\d{2}:\d{2}:\d{2})\s*$", tr, re.M)
    dur = fim[-1] if fim else (tss[-1] if tss else None)
    mins = None
    if dur:
        h, m, s = (int(x) for x in dur.split(":"))
        mins = h * 60 + m
    dm = DATA_RE.search(p.name) or DATA_RE.search(cab[:300])
    data = f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}" if dm else None
    tipo = "aplicação" if re.search(r"mentoria", p.name, re.I) else ("sessão estratégica" if re.search(r"diagn", p.name, re.I) else "outro")
    emails = sorted({e.lower() for e in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", cab) if "mettabrasil" not in e.lower()})
    alertas = []
    if mins is not None and mins < 15:
        alertas.append(f"call curta ({mins} min): provável no-show ou reagendamento")
    if not tr.strip() or not falas:
        alertas.append("não achei falas identificadas: conferir se o arquivo tem a transcrição")
    if apresentou is None:
        alertas.append("não achei ninguém da Metta entre os falantes")
    return {
        "arquivo": str(p),
        "lead": lead_do_nome(p.name),
        "data": data,
        "tipo": tipo,
        "apresentou": apresentou,
        "emails_convidados": emails,
        "fala_metta_pct": {
            (METTA.get(k) or nomes_originais[k]): round(100 * v / total) for k, v in metta_falas.items()
        },
        "falantes_lado_lead_pct": lado_lead,
        "duracao": dur,
        "caracteres_transcricao": len(tr),
        "alertas": alertas,
        "_transcricao": tr,
    }


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    pasta = Path(args[0]).expanduser().resolve()
    saida = Path(args[args.index("--saida") + 1]).expanduser().resolve() if "--saida" in args else pasta.parent
    prep = saida / "_preparo"
    prep.mkdir(parents=True, exist_ok=True)

    arquivos = sorted(x for x in pasta.rglob("*") if x.suffix.lower() in (".txt", ".md", ".docx") and not x.name.startswith(("~", ".")))
    calls = [analisar(a) for a in arquivos]

    leads = OrderedDict()
    for c in sorted(calls, key=lambda c: (chave(c["lead"]), c["data"] or "")):
        leads.setdefault(chave(c["lead"]), []).append(c)

    indice = []
    for k, cs in leads.items():
        registros = []
        for c in cs:
            nome_arq = f"{re.sub(r'[^A-Za-z0-9]+', '-', sem_acento(c['lead'])).strip('-')}__{c['data'] or 'sem-data'}.txt"
            destino = prep / nome_arq
            linhas = c["_transcricao"].split("\n")
            destino.write_text("\n".join(f"{i + 1}|{l}" for i, l in enumerate(linhas)), encoding="utf-8")
            r = {x: y for x, y in c.items() if not x.startswith("_")}
            r["transcricao_preparada"] = str(destino)
            r["linhas"] = len(linhas)
            registros.append(r)
        indice.append({
            "lead": cs[-1]["lead"],
            "calls": registros,
            "call_mais_recente": registros[-1]["data"],
            "apresentou_na_ultima_call": registros[-1]["apresentou"],
        })

    (prep / "indice.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")
    md = ["| Lead | Calls | Última call | Tipo | Apresentou | Duração | Alertas |", "|---|---|---|---|---|---|---|"]
    for it in indice:
        u = it["calls"][-1]
        al = "; ".join(a for c in it["calls"] for a in c["alertas"]) or ""
        md.append(f"| {it['lead']} | {len(it['calls'])} | {u['data']} | {u['tipo']} | {u['apresentou']} | {u['duracao']} | {al} |")
    (prep / "indice.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"\n{len(arquivos)} arquivo(s), {len(indice)} lead(s). Índice em {prep / 'indice.json'}")


if __name__ == "__main__":
    main()
