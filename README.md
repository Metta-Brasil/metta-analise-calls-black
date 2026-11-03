# Skills do time comercial da Metta

## Para que serve este repositório

Este repositório reúne, num lugar só, as skills do Claude Code que o time comercial da Metta usa.

Uma skill é um pacote de instruções, referências e scripts que ensina o Claude a fazer uma tarefa específica do jeito da Metta. Sem a skill, cada pessoa escreve o próprio pedido e o resultado muda de uma vez para outra. Com a skill, o critério fica dentro dela: como ler uma call, qual é a voz do closer, o que pode e o que não pode entrar numa mensagem e como conferir o resultado antes de entregar.

O repositório existe para três coisas:

- **Instalar uma vez:** cada pessoa do time instala uma vez e passa a ter todas as skills do comercial no Claude Code.
- **Todos com a mesma versão:** quando uma regra muda, como a condição da Black, a mudança é feita aqui e chega a todo o time pela atualização. Ninguém trabalha com arquivo antigo.
- **Crescer sem reinstalar:** uma skill nova entra no repositório e aparece para o time na próxima atualização.

## Skills disponíveis

- **reativacao-black:** lê as transcrições das calls de proposta do Programa SMTM e, para cada lead que não fechou, entrega um resumo para o Iago e duas mensagens de WhatsApp: a de reconexão e a da oferta Black. A skill só escreve. Quem envia é o Iago.

## Como o repositório é organizado

```
metta-skills-comercial/
├── README.md                     → este guia
├── .gitignore                    → impede que transcrição e resultado subam por engano
├── .claude-plugin/
│   └── marketplace.json          → a "loja" metta-brasil, que lista os plugins
└── plugins/
    └── metta-comercial/          → o plugin que o time instala
        ├── .claude-plugin/
        │   └── plugin.json       → nome e descrição do plugin
        └── skills/
            └── reativacao-black/ → a skill
                ├── SKILL.md      → passo a passo que o Claude segue
                ├── references/
                │   ├── leitura-da-call.md  → como ler a call e montar a ficha do lead
                │   ├── mensagens.md        → voz do Iago, regras da mensagem 1 e da 2
                │   ├── oferta-black.md     → condição da Black (só o que está VALE entra)
                │   └── exemplos.md         → exemplo completo fictício, bom e ruim
                └── scripts/
                    ├── preparar.py  → limpa e indexa as transcrições
                    └── conferir.py  → confere as mensagens antes de entregar
```

São três camadas:

1. **Marketplace** (`metta-brasil`): o endereço que o time adiciona uma vez no Claude Code.
2. **Plugin** (`metta-comercial`): o que o time instala. Ele carrega todas as skills do comercial.
3. **Skills:** cada uma numa pasta dentro de `skills/`. Uma skill nova entra como outra pasta ao lado de `reativacao-black/`.

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
