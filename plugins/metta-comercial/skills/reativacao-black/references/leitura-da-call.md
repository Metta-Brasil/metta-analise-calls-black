# Como ler uma call de proposta da Metta

A mensagem só fica boa se a leitura da call for boa. Esta é a parte que mais pesa na qualidade.

## O arquivo

- As calls vêm das anotações do Gemini (Google Meet). O topo do arquivo tem a data, os convidados e um **resumo automático do Gemini**. Depois vem a linha "<nome do evento> - Transcrição", com a transcrição de verdade.
- **O resumo do Gemini não é fonte.** Ele erra, generaliza e inventa conclusão. Use só a transcrição. O `preparar.py` já separa as duas partes.
- A transcrição tem uma marca de tempo (00:12:34) a cada minuto, mais ou menos, e as falas no formato `Nome: texto`. Para citar o minuto de uma fala, use a última marca de tempo acima dela.
- Erros comuns de reconhecimento: "Meta" no lugar de "Metta"; valores com a vírgula ou o milhar no lugar errado ("12 vezes de 3,5" pode ser 12x R$ 3.500; confira se o valor é repetido logo em seguida); números colados, como "4060" (= "40, 60"); nomes com grafia diferente ou em minúscula. Corrija pelo contexto, registre a leitura em "Atenção" e nunca copie o erro para a mensagem.
- O lead nem sempre aparece pelo nome: às vezes o rótulo é o nome da empresa ("Comercial Exemplo Ltda: ...") ou de quem estava logado. Descubra quem é quem pelo conteúdo.
- **Leia a transcrição inteira, até "A transcrição foi encerrada após".** A objeção e o combinado final estão nos últimos 15 minutos. Ler só o começo produz uma mensagem errada.
- Se o lead tiver mais de uma call (primeira reunião e retorno), leia todas. A mais recente define onde a negociação parou.

## Como a call é organizada

As calls de aplicação ("Mentoria Supere a Meta Todos os Meses") e de sessão estratégica ("Diagnóstico Supere a Meta Todos os Meses") seguem o mesmo roteiro. Saber onde cada coisa aparece economiza leitura e evita erro:

| O que você procura | Onde costuma estar |
|---|---|
| Como chamar o lead (nome, apelido) | Abertura: como o closer o chama |
| Empresa, segmento, tamanho do time | Primeiros 15 minutos: o lead conta a empresa |
| Desafio e dor, nas palavras dele | Contexto do lead e perguntas de diagnóstico (minuto 5 a 35). Perguntas típicas: distância entre o melhor e o pior vendedor, se o time defende preço, se as vendas acontecem sem o dono, impacto na família e na tranquilidade |
| Desejo (meta de TER e de SER) | Pergunta "qual a sua meta de TER e de SER", "o que você quer mudar" |
| Números dele (vendedores, quanto vende o melhor e o pior, faturamento, meta) | Mapa de oportunidade, por volta do minuto 30 |
| Proposta: plano e valores | Fim da call (minuto 50 a 75): "12x de ...", Premium, Exclusivo |
| Objeção e por que não fechou | Negociação e fechamento: sócio, cônjuge, orçamento, momento, comparar com outra empresa |
| Combinado | Últimos minutos: retorno marcado, envio de proposta, conversa com o sócio |

## O que extrair (ficha do lead)

Antes de escrever qualquer mensagem, monte a ficha. Toda informação leva o minuto da fala. O que a call não diz fica como "não dito na call". **Nunca complete com suposição.**

1. **Nome:** como o closer o chamou na call e o nome completo, se aparecer.
2. **Empresa e segmento.**
3. **Time:** quantos vendedores, se tem gerente, quem gerencia. Registre a composição como ele disse ("4 vendedores e eu"), sem arredondar.
4. **Desafio principal:** a dor que ele mesmo trouxe, com a frase literal. Prefira a que ele repetiu ou a que veio com emoção ("tô cansado", "trabalho no escuro"). Não use a dor que o closer sugeriu e ele só confirmou com "é".
5. **Desejo:** onde ele quer chegar, com a frase literal.
6. **Números dele**, se ditos: faturamento, meta, quanto vende o melhor e o pior vendedor.
7. **Proposta apresentada:** plano (Premium, Exclusivo, Elite) e valores ditos, inclusive o valor com desconto.
8. **Objeção / por que não fechou:** com a frase literal. Tipos: preço/orçamento/caixa, momento ("agora não", correria, fim de ano), decisor (sócio, cônjuge, pai, financeiro), confiança (já se frustrou com mentoria ou consultoria), comparação com concorrente, outra prioridade.
9. **Combinado no fim:** retorno marcado, o que ficou de mandar, com quem ele ia conversar.
10. **Quem apresentou:** está no índice do `preparar.py` (`apresentou`). Confira na transcrição: é a pessoa da Metta com mais fala. Não confunda com convidados do topo (Silvio, Kárita), que muitas vezes nem falam.
11. **Nome da empresa:** se não for dito na call, olhe `emails_convidados` no índice. O domínio do e-mail do lead costuma ser o site da empresa (fulano@nomedaempresa.com.br → Nome da Empresa). Use como pista e marque "pelo e-mail do convite" no resumo. Gmail, Hotmail, Outlook e afins não dizem nada. Nome que veio só do e-mail não entra nas mensagens: a grafia pode estar errada.

## Sinais de que não é para mandar mensagem (ou de revisar antes)

- Call com menos de 15 minutos, sem proposta: no-show, reagendamento ou conversa interna.
- A call não chegou à proposta (o preço não foi apresentado: acabou o tempo, ficou para uma segunda reunião). Pode existir uma call seguinte que não está na pasta. Escreva as mensagens, mas a mensagem 2 não pode dizer "mais em conta do que a proposta que te apresentei": troque por "condição especial de Black".
- O lead fechou na call ou depois (pagou sinal, assinou, falou em data de início).
- O lead disse que contratou outra empresa ou que não quer mais contato.
- Quem estava na call não era o dono (gerente, funcionário).

Nesses casos, faça o resumo, escreva **REVISAR ANTES DE ENVIAR** e explique o motivo em uma linha. Escreva a mensagem só se ela ainda fizer sentido.
