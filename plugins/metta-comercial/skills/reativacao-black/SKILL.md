---
name: reativacao-black
description: Use quando for reabordar, na Black, leads que já receberam proposta do Programa SMTM. Lê a transcrição da call de cada lead e entrega o resumo para o Iago e duas mensagens de WhatsApp (reconexão e oferta Black), personalizadas e conferidas.
---

# Reativação Black: leads que já receberam proposta

Para cada lead que ouviu a proposta do Programa SMTM e não fechou, a skill entrega três coisas, prontas para o Iago:

1. **Resumo do lead:** quem é, o que queria, o que travou e o que foi oferecido, para o Iago não precisar reler a call.
2. **Mensagem 1 (reconexão):** curta, lembrando o desafio que o lead contou na call.
3. **Mensagem 2 (oferta Black):** para enviar depois que ele responder. Liga a condição de Black ao problema dele e convida para uma conversa.

A proposta customizada não faz parte desta skill. Quem monta é o Iago.

## Entrada

- Uma pasta com as transcrições das calls de proposta (anotações do Gemini exportadas como .txt, .md ou .docx), um arquivo por call.
- `references/oferta-black.md` revisado: só os itens marcados como VALE entram nas mensagens.

## Antes de começar

1. Leia por inteiro `references/oferta-black.md`, `references/leitura-da-call.md`, `references/mensagens.md` e `references/exemplos.md`.
2. Prepare as transcrições:
   ```
   python3 <pasta-da-skill>/scripts/preparar.py <pasta-das-transcricoes> --saida <pasta-de-trabalho>
   ```
   O script grava `_preparo/indice.json`, com um registro por lead (calls, data, tipo, quem apresentou, duração, alertas), e uma transcrição limpa por call, com número de linha. O resumo do Gemini fica de fora.
3. Crie `<pasta-de-trabalho>/saida/`. Se já existir arquivo de um lead lá, pule esse lead, a menos que tenham pedido para refazer.

## Para cada lead (um de cada vez)

**Nunca carregue as transcrições de dois leads no mesmo contexto:** as falas se misturam. Com muitos leads, use um subagente por lead, passando o caminho deste SKILL.md, das referências e das transcrições do lead.

1. **Leia todas as calls do lead inteiras**, até a última linha. Se uma transcrição passar do limite de leitura, leia por partes (offset) até o fim. Com mais de uma call, a mais recente define onde a negociação parou.
2. **Monte a ficha do lead** conforme `leitura-da-call.md`: nome, empresa, segmento, time, desafio, desejo, números, proposta, objeção, combinado e quem apresentou. Cada item leva a frase literal e o minuto. O que a call não diz fica como "não dito na call".
3. **Escreva o resumo para o Iago:** os seis itens do formato abaixo, cada um em uma ou duas linhas (até 35 palavras), só fatos da call. É para ele bater o olho antes de mandar a mensagem, não para substituir a ficha.
4. **Escreva a mensagem 1** pelas regras de `mensagens.md`. A abertura muda se quem apresentou não foi o Iago.
5. **Escreva a mensagem 2:** escolha a alavanca da Black pela objeção do lead (tabela em `mensagens.md`), aplique a regra do "já paga" e use só os itens VALE.
6. **Confira cada mensagem** antes de salvar:
   - O detalhe citado está mesmo na transcrição, com as palavras dele? Conferir na linha.
   - Um empresário que não estava na call conseguiria receber essa mensagem? Se sim, ela está genérica: reescreva.
   - Tem preço, percentual, prazo ou benefício que não está como VALE? Tire.
   - O dono leria e pensaria "então a culpa é minha?"? Reescreva.
   - Respeita o limite de palavras (45 na mensagem 1, 100 na mensagem 2)?
   - Tem cara de texto de IA (frase de efeito, lista de três, travessão, "jornada", "transformar")? Reescreva até soar como o Iago no WhatsApp.
7. **Salve** em `saida/<AAAA-MM-DD>_<Lead>.md`, no formato abaixo.
8. **Rode o conferidor** e corrija o que ele apontar:
   ```
   python3 <pasta-da-skill>/scripts/conferir.py <pasta-de-trabalho>/saida
   ```

No fim, gere `saida/_resumo.md` com uma tabela: lead, empresa, data da call, quem apresentou, objeção (em poucas palavras), alavanca usada na mensagem 2 e status ("pronto" ou "REVISAR: motivo"). Abaixo da tabela, inclua esta linha: "A skill leu só as transcrições. Antes de enviar, confira no WhatsApp e na Clint se houve contato depois da call: o lead pode ter fechado, recusado ou já ter sido reabordado."

## Formato do arquivo de cada lead

```
# <Nome> · <Empresa>

Call: <aplicação | sessão estratégica> em <DD/MM/AAAA> · apresentou: <nome> · transcrição: <caminho do arquivo preparado>
Status: <pronto | REVISAR ANTES DE ENVIAR: motivo>

## Para o Iago
- Quem é: <cargo, empresa, segmento, time>
- O que ele queria: <desejo, nas palavras dele>
- O que trava: <desafio principal, nas palavras dele>
- Por que não fechou: <objeção, nas palavras dele>
- Proposta apresentada: <plano e valores ditos na call>
- Combinado no fim da call: <...>

## Mensagem 1 · reconexão

<balão 1>

<balão 2>

## Mensagem 2 · oferta Black (enviar depois da resposta do lead)

<balão 1>

<balão 2>

<balão 3>

Se o lead responder que o desafio já foi resolvido, não envie esta mensagem como está.

## Base da mensagem (falas da call)
- Desafio: "<frase literal>" (<hh:mm:ss>, linha <n>)
- Desejo: "<frase literal>" (<hh:mm:ss>, linha <n>)
- Objeção: "<frase literal>" (<hh:mm:ss>, linha <n>)
- Números usados: "<frase literal>" (<hh:mm:ss>, linha <n>) | não usados

## Atenção
- <lacunas, dúvidas, sinais de que não é para enviar. "Nada" se não houver>
```

Os balões são texto puro de WhatsApp: sem markdown, sem negrito e sem marcadores de lista.

## O que nunca fazer

- Inventar desafio, número, nome de sócio ou detalhe que não está na transcrição.
- Usar o resumo do Gemini como fonte.
- Prometer resultado, prazo ou condição que não esteja como VALE em `oferta-black.md`.
- Mandar a mensagem 2 junto com a mensagem 1.
- Enviar qualquer mensagem. A skill só escreve: quem envia é o Iago.
