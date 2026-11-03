---
name: reativacao-black
description: Use quando for reabordar, na Black, leads que já receberam proposta do Programa SMTM, ou quando o Iago colar a resposta de um lead à mensagem 1. Lê a transcrição da call de cada lead e entrega o resumo para o Iago e duas mensagens de WhatsApp (reconexão e oferta Black), prontas para copiar e conferidas.
---

# Reativação Black: leads que já receberam proposta

Para cada lead que ouviu a proposta do Programa SMTM e não fechou, a skill entrega três coisas, prontas para o Iago:

1. **Resumo do lead:** quem é, o que queria, o que travou e o que foi oferecido, para o Iago não precisar reler a call.
2. **Mensagem 1 (reconexão):** a meta que o lead contou na call e pelo menos três problemas dele, em bullets.
3. **Mensagem 2 (oferta Black):** para enviar depois que ele responder. Liga cada problema ao que o programa faz, lista a condição de Black e sugere dia e horário com o Iago. Vai junto com o PDF da Condição Black. Se o Iago colar a resposta do lead, a mensagem 2 é reescrita considerando essa resposta (seção "Com a resposta do lead").

A proposta customizada não faz parte desta skill. Quem monta é o Iago.

## Entrada

- Uma pasta com as transcrições das calls de proposta (anotações do Gemini exportadas como .txt, .md ou .docx), um arquivo por call.
- `references/oferta-black.md`: só os itens marcados como VALE entram nas mensagens.

## Antes de começar

1. Leia por inteiro `references/oferta-black.md`, `references/leitura-da-call.md`, `references/mensagens.md`, `references/o-que-o-programa-resolve.md` e `references/exemplos.md`.
2. Prepare as transcrições:
   ```
   python3 <pasta-da-skill>/scripts/preparar.py <pasta-das-transcricoes> --saida <pasta-de-trabalho>
   ```
   O script grava `_preparo/indice.json`, com um registro por lead (calls, data, tipo, quem apresentou, duração, alertas), e uma transcrição limpa por call, com número de linha. O resumo do Gemini fica de fora.
3. Crie `<pasta-de-trabalho>/saida/`. Se já existir arquivo de um lead lá, pule esse lead, a menos que tenham pedido para refazer.
4. Anote a data de hoje: a mensagem 2 diz há quanto tempo foi a call.

## Para cada lead (um de cada vez)

**Nunca carregue as transcrições de dois leads no mesmo contexto:** as falas se misturam. Com muitos leads, use um subagente por lead, passando o caminho deste SKILL.md, das referências, das transcrições do lead e a data de hoje.

1. **Leia todas as calls do lead inteiras**, até a última linha. Se uma transcrição passar do limite de leitura, leia por partes (offset) até o fim. Com mais de uma call, a mais recente define onde a negociação parou.
2. **Monte a ficha do lead** conforme `leitura-da-call.md`: nome, empresa, segmento, B2B ou B2C, time, meta de resultado, falas emocionais, pelo menos três problemas, números, plano apresentado, objeção, combinado e quem apresentou. Cada item leva a frase literal e a linha. O que a call não diz fica como "não dito na call".
3. **Escreva o resumo para o Iago:** os seis itens do formato abaixo, cada um em uma ou duas linhas (até 35 palavras), só fatos da call.
4. **Escreva a mensagem 1** pelas regras de `mensagens.md`: meta de resultado, se ele disse, e pelo menos três problemas em bullets e negrito. A abertura muda se quem apresentou não foi o Iago.
5. **Escreva a mensagem 2** pela sequência de `mensagens.md`: tempo desde a call, cada problema ligado ao que o programa faz (só com `o-que-o-programa-resolve.md`), a lista da condição de Black com os itens VALE e a sugestão de dia e horário.
6. **Confira cada mensagem** antes de salvar:
   - Cada problema e a meta estão mesmo na transcrição, com as palavras dele? Conferir na linha.
   - Um empresário que não estava na call conseguiria receber essa mensagem? Se sim, ela está genérica: reescreva.
   - Tem preço, percentual, prazo ou benefício que não está como VALE? Tire.
   - A entrega citada na mensagem 2 está em `o-que-o-programa-resolve.md`, com o verbo de lá? Se não, tire.
   - O dono leria e pensaria "então a culpa é minha?"? Algum bullet julga o time ou o gerente ("acomodado", "não quer")? Reescreva descrevendo a situação.
   - Respeita o limite de palavras (70 na mensagem 1, 170 na mensagem 2)?
   - Tem cara de texto de IA (frase de efeito, travessão, "jornada", "transformar")? Reescreva até soar como o Iago no WhatsApp.
7. **Salve** em `saida/<AAAA-MM-DD>_<Lead>.md`, no formato abaixo.
8. **Rode o conferidor** e corrija o que ele apontar:
   ```
   python3 <pasta-da-skill>/scripts/conferir.py <pasta-de-trabalho>/saida
   ```

No fim, gere `saida/_resumo.md` com uma tabela: lead, empresa, data da call, quem apresentou, plano apresentado, objeção (em poucas palavras) e status ("pronto" ou "REVISAR: motivo"). Abaixo da tabela, inclua estas linhas: "A skill leu só as transcrições. Antes de enviar, confira no WhatsApp e na Clint se houve contato depois da call: o lead pode ter fechado, recusado ou já ter sido reabordado." e "Mande o PDF da Condição Black junto com a mensagem 2."

## Formato do arquivo de cada lead

Cada balão das mensagens vai num bloco de código próprio (três crases antes e depois). Assim o Iago copia o texto cru, com os asteriscos do negrito, e nada que não é mensagem fica junto. Tudo o que é instrução para o Iago fica fora dos blocos, numa seção separada.

````
# <Nome> · <Empresa>

Call: <aplicação | sessão estratégica> em <DD/MM/AAAA> · apresentou: <nome> · transcrição: <caminho do arquivo preparado>
Status: <pronto | REVISAR ANTES DE ENVIAR: motivo>

## Para o Iago
- Quem é: <cargo, empresa, segmento, B2B ou B2C, time>
- O que ele queria: <meta, nas palavras dele>
- O que trava: <problemas principais, nas palavras dele>
- Por que não fechou: <objeção, nas palavras dele>
- Proposta apresentada: <plano e valores ditos na call>
- Combinado no fim da call: <...>

## Mensagem 1 · reconexão

```
<balão 1>
```

```
<balão 2, com os bullets>
```

```
<balão 3>
```

## Mensagem 2 · oferta Black (enviar depois da resposta do lead)

```
<balão 1>
```

```
<balão 2>
```

```
<balão 3, com a lista da condição>
```

```
<balão 4: sugestão de dia e horário>
```

## Antes de enviar a mensagem 2 (não copiar)
- Mande o PDF da Condição Black junto com a mensagem 2.
- Se quiser a mensagem 2 ajustada à resposta do lead, cole a resposta dele no chat.

## Base da mensagem (falas da call)
- Meta: "<frase literal>" (<hh:mm:ss>, linha <n>) | não dita na call
- Problema 1: "<frase literal>" (<hh:mm:ss>, linha <n>)
- Problema 2: "<frase literal>" (<hh:mm:ss>, linha <n>)
- Problema 3: "<frase literal>" (<hh:mm:ss>, linha <n>)
- Objeção: "<frase literal>" (<hh:mm:ss>, linha <n>)
- Plano apresentado: "<frase literal>" (<hh:mm:ss>, linha <n>) | não chegou à proposta

## Atenção
- <lacunas, dúvidas, sinais de que não é para enviar. "Nada" se não houver>
````

Um "Problema" a mais para cada bullet além do terceiro.

## Formato das mensagens (WhatsApp)

- **Sempre em bloco de código**, no arquivo e quando mostrar no chat. Fora do bloco, o chat transforma `*texto*` em itálico e o asterisco some na cópia.
- **Dentro do bloco só vai o que é para enviar.** Instrução, aviso, "enviar junto", nome da seção: tudo fora do bloco.
- Negrito com **um** asterisco de cada lado: `*texto*`. Nunca `**texto**`, que aparece no WhatsApp com asterisco sobrando.
- Bullets com hífen e espaço no começo da linha: `- *texto*`.
- Sem exagero: negrito só nos bullets. Sem emoji, sem título, sem tabela, sem outro markdown.

## Com a resposta do lead

Quando o Iago colar no chat a resposta de um lead à mensagem 1:

1. Identifique o lead pelo nome. Leia o arquivo dele em `saida/` e, se precisar, a transcrição preparada. Se não houver arquivo, rode o fluxo normal para esse lead antes.
2. Reescreva a mensagem 2 considerando a resposta:
   - a abertura reage ao que ele respondeu, com as palavras dele;
   - problema que ele confirmou ou trouxe de novo entra no "a gente resolve com", só com as entregas de `o-que-o-programa-resolve.md`;
   - problema que ele disse que resolveu sai;
   - o resto da estrutura não muda: lista da condição de Black e sugestão de dia e horário.
3. Se a resposta disser que ele fechou com outra empresa, não quer mais contato ou resolveu tudo, não escreva a oferta: avise o Iago e pare.
4. Acrescente ao arquivo do lead a seção `## Mensagem 2 · com a resposta do lead`, com a resposta dele citada fora dos blocos e a mensagem nova em blocos, e rode o conferidor.
5. No chat, mostre a mensagem nova em blocos de código, um por balão, e, fora dos blocos, a lembrança do PDF.

Sem resposta do lead, a mensagem 2 sai no padrão, escrita para o caso mais comum (os desafios continuam).

## O que nunca fazer

- Inventar meta, problema, número, nome de sócio ou detalhe que não está na transcrição.
- Usar o resumo do Gemini como fonte.
- Prometer resultado, prazo ou condição que não esteja como VALE em `oferta-black.md`.
- Citar crescimento médio de clientes ou outro número sobre resultados da Metta que não esteja como VALE.
- Mandar a mensagem 2 junto com a mensagem 1.
- Enviar qualquer mensagem. A skill só escreve: quem envia é o Iago.
