# Skills do time comercial da Metta

Skills para o Claude Code. Hoje tem uma:

- **reativacao-black:** lê as transcrições das calls de proposta do Programa SMTM e, para cada lead que não fechou, entrega um resumo para o Iago e duas mensagens de WhatsApp: a de reconexão e a da oferta Black. A skill só escreve. Quem envia é o Iago.

## Instalar (uma vez)

O computador precisa ter Claude Code, git e Python 3.

No Claude Code, digite os dois comandos:

```
/plugin marketplace add Metta-Brasil/metta-skills-comercial
/plugin install metta-comercial@metta-brasil
```

Depois, feche e abra o Claude Code.

Se o primeiro comando der erro de SSH, use o endereço completo:

```
/plugin marketplace add https://github.com/Metta-Brasil/metta-skills-comercial.git
```

## Receber as atualizações

A condição da Black e as regras da skill são atualizadas neste repositório. Para receber as mudanças automaticamente, ligue a atualização automática: digite `/plugin`, abra a aba **Marketplaces**, escolha **metta-brasil** e selecione **Enable auto-update**.

Para atualizar na hora:

```
/plugin marketplace update metta-brasil
```

## Rodar a reativação Black

1. Baixe do Drive as anotações do Gemini das calls de proposta: clique com o botão direito na pasta e escolha "Fazer download". A skill lê .docx, .txt e .md, um arquivo por call. Se o lead teve duas calls, inclua as duas.
2. Crie uma pasta de trabalho, coloque as anotações numa subpasta chamada `transcricoes` e abra o Claude Code na pasta de trabalho.
3. Digite:

```
Use a skill reativacao-black. As transcrições estão em ./transcricoes. Use ./trabalho como pasta de trabalho.
```

O resultado fica em `trabalho/saida/`:
- um arquivo por lead, com o resumo para o Iago, a mensagem 1, a mensagem 2 e as falas da call usadas como base;
- `_resumo.md`, com a tabela de todos os leads e o status de cada um.

## Antes de o Iago enviar

- **Confira o WhatsApp e a Clint de cada lead.** A skill lê só a call. Se o lead fechou, recusou ou já foi reabordado depois dela, a mensagem não serve.
- **Status REVISAR:** leia o motivo antes de usar.
- **A mensagem 2 só vai depois da resposta à mensagem 1.** Se o lead disser que o problema já foi resolvido, não mande a mensagem 2 como está.

## Condição da Black

A condição fica em `plugins/metta-comercial/skills/reativacao-black/references/oferta-black.md`. Só o que está como **VALE** entra nas mensagens. As mudanças são feitas pelo marketing, neste repositório, e chegam a todos pela atualização.

## Importante

Este repositório é público. Nunca suba transcrição, resultado da skill nem dado de lead ou de cliente.
