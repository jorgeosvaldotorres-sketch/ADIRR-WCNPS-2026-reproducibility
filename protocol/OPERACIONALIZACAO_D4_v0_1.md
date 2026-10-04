# ADIRR WCNPS 2026 — Operacionalização de D4 v0.1

Data: 2026-09-28
Status: proposta para revisão. Não implementa código de terceiros; contém
um ponto de decisão explícito (seção "Decisão pendente de confirmação")
que precisa de validação antes do congelamento.

## Base no artigo-base

Eq. (5): `B_{a,c,t} = I_θI(z_{a,c,t}, E^dir_{a,c,t}, E^ind_{a,c,t},
G^prov_{a,c,t}, π_t)`.

Seção 3.3 do artigo-base estabelece que, para permanecer inference-agnostic,
a arquitetura usa quatro noções conceituais: suporte, contra-suporte,
incerteza e observabilidade. Suporte e contra-suporte denotam evidência a
favor ou contra uma conclusão; incerteza reflete evidência insuficiente;
observabilidade indica se o comportamento pôde ser observado. O texto é
explícito: manter observabilidade separada evita que ausência de
oportunidade seja confundida com evidência inconclusiva; coexistência de
suporte e contra-suporte relevantes denota conflito.

## Regras obrigatórias herdadas do ponto de continuidade (2026-09-22)

1. Não transformar `z` em reputação por conveniência.
2. Preservar a distinção entre representação comportamental (`z`) e estado
   de crença (`B`).
3. Evidência direta complementar sem dupla contagem.
4. Evidência indireta fora do cenário inicial, salvo decisão explícita.
5. Proveniência/dependência representada explicitamente, mesmo que
   simplificada.
6. Política `π_t` explícita.
7. Não importar modelo Beta, média simples ou outra regra externa como
   definição de D4.
8. D6 só é fechado depois de D4 operacionalizado.

## Decisão de instanciação

Para o cenário binário, cooperativo, determinístico e de fonte única, D4
instancia `B_{a,c,t}` como uma tupla explícita e não colapsada:

`B_{a,c,t} = (support_{a,c,t}, counter_support_{a,c,t}, uncertainty_{a,c,t}, observability_{a,c,t})`

- `support_{a,c,t}` = massa de suporte positivo já computada em D3
  (`positive_support` de `z`), somada a evidência direta complementar não
  codificada em `z` — nesta etapa, zero (ver E^dir abaixo).
- `counter_support_{a,c,t}` = massa de suporte negativo já computada em D3
  (`negative_support` de `z`), pela mesma regra.
- `observability_{a,c,t}` = `z_observability_rate`, herdada diretamente de
  `z`, sem recomputar. Mantida como campo próprio, nunca combinada
  aritmeticamente com suporte/contra-suporte, para não reintroduzir a
  confusão que a arquitetura proíbe.
- `uncertainty_{a,c,t}`: ver "Decisão pendente de confirmação" abaixo.

Esta escolha não introduz equação nova: é a instanciação do operador
`I_θI` já previsto pela Eq. (5), usando exatamente o vocabulário
conceitual que o artigo-base já declara (seção 3.3), sem adotar um modelo
nomeado de terceiros (Beta, Subjective Logic, média) como definição do
próprio operador.

## E^dir (evidência direta complementar)

Declarada explicitamente como vazia nesta etapa: `E^dir_{a,c,t} = ∅`.

**Correção de linguagem (Fase A, revisão científica, 2026-09-30 ou
posterior):** a formulação anterior ("evidência direta já está
codificada em z") colapsava uma distinção que a Eq. (5) preserva
estruturalmente — representação comportamental (`z`) e evidência direta
complementar são categorias distintas, mesmo quando uma delas está vazia
no cenário. A justificativa correta é: **neste cenário, de fonte única,
não existe evidência direta complementar disponível além daquela já
utilizada na formação de `z`** — não que essa evidência tenha sido
absorvida ou codificada em `z`. `E^dir` fica vazio por ausência de
conteúdo no cenário sintético, não por colapso conceitual da categoria.
Introduzir `E^dir` não-vazio exigiria uma segunda fonte de evidência
direta distinta da que já alimenta `z`, o que não existe neste primeiro
cenário. Isso evita dupla contagem (regra 3), e mantém a arquitetura
aberta para cenários futuros com múltiplas fontes diretas.

## E^ind (evidência indireta)

Declarada explicitamente como vazia: `E^ind_{a,c,t} = ∅`, conforme regra 4
e decisão estratégica original (sem recomendações indiretas nesta etapa).

## G^prov (proveniência/dependência)

Representada de forma mínima, não omitida: cada evento é anotado com uma
proveniência trivial de fonte única —
`G^prov_{a,c,t} = {"sources": ["agent_coop_01_observer"], "dependency_edges": []}`.
Isso satisfaz a regra 5 (representação explícita) sem simular dependências
que não existem no cenário sintético de fonte única.

## π_t (política)

Representada explicitamente como objeto de configuração, não implícita no
código:

```
π_t = {
  "window_semantics": "tumbling",
  "direct_evidence_policy": "excluida nesta etapa - ja codificada em z",
  "indirect_evidence_policy": "excluida nesta etapa - decisao estrategica",
  "conflict_rule": "suporte e contra-suporte simultaneos e relevantes denotam conflito, nao sao resolvidos nesta etapa",
}
```

## Decisão sobre `uncertainty` — CONFIRMADA em 2026-09-28

A proposta abaixo foi adotada como definitiva. Nenhuma alternativa contínua
foi adotada, pelo motivo já registrado: qualquer função decrescente e
contínua da massa de evidência se aproxima estruturalmente de uma família
paramétrica de incerteza de terceiros (Subjective Logic/Beta), o que a
regra 7 veta. A regra binária abaixo é a única formulação, entre as
avaliadas, que não importa esse tipo de família.

## Definição de `uncertainty` (histórico da decisão)

Esta é a única peça de D4 que exige uma escolha numérica, e é exatamente
onde o risco de reintroduzir um modelo externo "pela porta dos fundos"
existe (ex.: qualquer função decrescente contínua da massa de evidência se
aproxima estruturalmente de termos de incerteza de Subjective Logic ou de
variância de uma Beta).

Proposta mínima, nativa da ADIRR e não paramétrica:

`uncertainty_{a,c,t} = 1` se `evidence_mass_{a,c,t} = 0` (nenhuma evidência
real nem imputada disponível na janela); caso contrário, `uncertainty_{a,c,t} = 0`.

Consequências desta escolha, que devem ser verificadas e discutidas no
artigo, não apenas assumidas:

- Em M1 (ausência preservada), `uncertainty=1` só ocorre em janelas
  totalmente vazias, cuja probabilidade sob O40/L=50 já foi calculada como
  ≈8,08×10⁻¹² (seção 5.9.3 do manuscrito). Ou seja, na prática, com os
  parâmetros já fixados, `uncertainty` será quase sempre 0 mesmo sob
  observabilidade severa — a redução de observabilidade se manifesta via
  `observability_rate` e via composição de `support`/`counter_support`,
  não via `uncertainty`.
- Em M2 (imputação neutra), toda ausência recebe massa η°=(0,5;0,5), logo
  `evidence_mass` nunca é zero e `uncertainty=0` sempre, **por construção
  — consequência lógica direta da regra binária combinada com a regra de
  imputação, não um resultado observado independentemente** (correção de
  linguagem, Fase A). Isso evidencia uma limitação da regra binária
  adotada (não distingue ausência total de evidência de ausência
  parcial, quando alguma evidência real está presente) e não deve ser
  apresentado como demonstração geral de que a ADIRR, ou a imputação
  neutra em geral, "mascara" incerteza — essa consequência é específica
  desta instanciação mínima.
- Uncertainty e observability permanecem estruturalmente distintos mesmo
  quando, neste cenário determinístico e sem conflito real, covariam
  empiricamente. Essa covariação é uma limitação de escopo do primeiro
  cenário (sem conflito possível, porque o comportamento-verdade é sempre
  cooperativo) e deve ser declarada como tal nas Limitações, não
  apresentada como propriedade geral da arquitetura.

Esta proposta não é implementada até confirmação. Alternativas descartadas
e por quê:
- Função contínua decrescente de `evidence_mass` (ex. `1/(1+massa)`): mais
  expressiva, mas se aproxima estruturalmente de uma família paramétrica
  de incerteza (Subjective Logic/Beta) o suficiente para exigir a mesma
  discussão de "importação de modelo externo" que a regra 7 veta. Reservada
  como extensão futura, se a evidência do cenário determinístico mostrar
  necessidade.
- Igualar `uncertainty` a `1 - observability_rate`: rejeitada por
  conflacionar as duas noções que a arquitetura exige manter separadas
  (violaria a própria premissa central do experimento).

## O que ainda não é fechado por este documento

- D6 (mapeamento de `B` para o escalar publicável `ρ`) permanece como
  próximo gate, não coberto aqui.
- A grade fatorial q×L (`DESENHO_FATORIAL_Q_L_v0_1.md`) aplica-se
  igualmente a D4: `B` é computado por combinação (replicação, q, L,
  janela), sem alteração da lógica acima.
