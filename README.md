# Análise de calls para a Black · Metta

## Para que serve este repositório

Este repositório tem uma função só: analisar as calls de proposta do Programa SMTM para a campanha Black.

A skill lê a transcrição da call de cada lead que recebeu proposta e não fechou. Para cada um, ela entrega ao Iago:

- um resumo do lead: quem é, o que queria, o que travou e o que foi oferecido;
- a mensagem 1 de WhatsApp, de reconexão, com a meta que o lead contou na call e pelo menos três problemas dele, em bullets;
- a mensagem 2, que liga cada problema ao que o programa faz, lista a condição de Black e sugere dia e horário com o Iago. Ela vai junto com o PDF da Condição Black.

A skill só escreve. Quem envia é o Iago.

Uma skill é um pacote de instruções, referências e scripts que ensina o Claude a fazer uma tarefa do jeito da Metta. Aqui, o critério fica dentro dela: como ler a call, qual é a voz do Iago, o que pode e o que não pode entrar na mensagem e como conferir o resultado antes de entregar.

O repositório existe para que quem roda a análise:

- **instale uma vez** no Claude Code;
- **use sempre a mesma versão:** quando a condição da Black muda, a mudança é feita aqui e chega a todos pela atualização.

## Como o repositório é organizado

```
metta-analise-calls-black/
├── README.md                     → este guia
├── .gitignore                    → impede que transcrição e resultado subam por engano
├── .claude-plugin/
│   └── marketplace.json          → a "loja" metta-black, que aponta para o plugin
└── plugins/
    └── analise-calls-black/      → o plugin que se instala
        ├── .claude-plugin/
        │   └── plugin.json       → nome e descrição do plugin
        └── skills/
            └── reativacao-black/ → a skill
                ├── SKILL.md      → passo a passo que o Claude segue
                ├── references/
                │   ├── leitura-da-call.md  → como ler a call e montar a ficha do lead
                │   ├── mensagens.md        → voz do Iago, regras da mensagem 1 e da 2
                │   ├── oferta-black.md     → condição da Black (só o que está VALE entra)
                │   ├── o-que-o-programa-resolve.md → entregas do programa para ligar problema e solução
                │   └── exemplos.md         → exemplo completo fictício, bom e ruim
                └── scripts/
                    ├── preparar.py  → limpa e indexa as transcrições
                    └── conferir.py  → confere as mensagens antes de entregar
```

São três camadas:

1. **Marketplace** (`metta-black`): o endereço que o time adiciona uma vez no Claude Code.
2. **Plugin** (`analise-calls-black`): o que se instala.
3. **Skill** (`reativacao-black`): a análise das calls para a Black.

## Instalar (uma vez)

Quem roda a análise é o Iago, no próprio computador. O computador precisa ter o Claude Code (no terminal ou na aba Code do app Claude, numa sessão local), git e Python 3.

No Claude Code, digite os dois comandos:

```
/plugin marketplace add Metta-Brasil/metta-analise-calls-black
/plugin install analise-calls-black@metta-black
```

Depois, feche e abra o Claude Code.

Se o primeiro comando der erro de SSH, use o endereço completo:

```
/plugin marketplace add https://github.com/Metta-Brasil/metta-analise-calls-black.git
```

## Receber as atualizações

A condição da Black e as regras da skill são atualizadas neste repositório. Para receber as mudanças automaticamente, ligue a atualização automática: digite `/plugin`, abra a aba **Marketplaces**, escolha **metta-black** e selecione **Enable auto-update**.

Para atualizar na hora:

```
/plugin marketplace update metta-black
```

## Rodar a análise das calls

1. Baixe do Drive as anotações do Gemini das calls de proposta: clique com o botão direito na pasta e escolha "Fazer download". A skill lê .docx, .txt e .md, um arquivo por call. Se o lead teve duas calls, inclua as duas.
2. Crie uma pasta de trabalho, coloque as anotações numa subpasta chamada `transcricoes` e abra o Claude Code na pasta de trabalho.
3. Digite:

```
Use a skill reativacao-black. As transcrições estão em ./transcricoes. Use ./trabalho como pasta de trabalho.
```

O resultado fica em `trabalho/saida/`:
- um arquivo por lead, com o resumo para o Iago, a mensagem 1, a mensagem 2 e as falas da call usadas como base;
- `_resumo.md`, com a tabela de todos os leads e o status de cada um.

Cada mensagem vem inteira num bloco de código único, já com a formatação do WhatsApp (`*negrito*` e bullets): um clique para copiar, uma mensagem para enviar. Copie só o que está dentro do bloco. As instruções, como mandar o PDF junto, ficam fora dele.

## Ajustar a mensagem 2 com a resposta do lead

Quando o lead responder à mensagem 1, cole a resposta no Claude Code, na mesma pasta de trabalho:

```
Use a skill reativacao-black. Resposta do <nome do lead>: <cole aqui a resposta>
```

A skill reescreve a mensagem 2 considerando a resposta e acrescenta ao arquivo do lead. Sem a resposta, vale a mensagem 2 padrão.

## Antes de o Iago enviar

- **Confira o WhatsApp e a Clint de cada lead.** A skill lê só a call. Se o lead fechou, recusou ou já foi reabordado depois dela, a mensagem não serve.
- **Status REVISAR:** leia o motivo antes de usar.
- **A mensagem 2 só vai depois da resposta à mensagem 1.** Se o lead disser que o problema já foi resolvido, não mande a mensagem 2 como está.
- **Mande o PDF da Condição Black junto com a mensagem 2.** Se o lead não abrir o PDF, a condição está na mensagem.

## Condição da Black

A condição fica em `plugins/analise-calls-black/skills/reativacao-black/references/oferta-black.md`. Só o que está como **VALE** entra nas mensagens. As mudanças são feitas pelo marketing, neste repositório, e chegam a todos pela atualização.

## Importante

Este repositório é público. Nunca suba transcrição, resultado da skill nem dado de lead ou de cliente.
