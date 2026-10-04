# ADIRR WCNPS 2026 — Operacionalização de D6 v0.1

Data: 2026-09-28
Status: implementada, pendente de execução em escala (piloto/científico).
Depende de: `OPERACIONALIZACAO_D4_v0_1.md` (regra de `uncertainty` confirmada).

## Base no artigo-base

Eq. (7): `R^(v)_{a,c,t} = ⟨ρ^(v)_{a,c,t}, B^(v)_{a,c,t}, V^(v)_{a,c,t}, v_I, θ_I, π_t, p^(v)_{a,c,t}⟩`.

O texto associado estabelece que o registro reputacional preserva agente,
contexto, tempo, versão, valor de reputação, estado de crença de suporte,
validade da conclusão, versão/parâmetros do modelo de inferência, política
corrente e proveniência da evidência — mantendo versões de reputação
distinguíveis e rastreáveis. Integridade permanece separada de inferência
(fora do escopo desta etapa).

## Única decisão numérica nova: `ρ` (o escalar publicável)

D4 já produz `B = (support, counter_support, uncertainty, observability)`
como estrutura não colapsada. D6 precisa produzir o escalar `ρ` que o
artigo-base define como parte do registro, mas não define como calculá-lo
— isso é, por design, delegado à instanciação (Eq. 5/7 são
inference-agnostic).

Definição adotada:

```
rho_{a,c,t} = support_{a,c,t} / (support_{a,c,t} + counter_support_{a,c,t})   se evidence_mass > 0
rho_{a,c,t} = NaN                                                             se evidence_mass = 0
```

### Por que isso não viola a regra "não transformar z em reputação por conveniência"

A objeção óbvia: `support`/`counter_support` vieram de `z` (via D4), então
`rho` seria numericamente equivalente à taxa de sucesso já calculada em
D3. Isso é verdade e é **esperado, não um defeito**, pelas seguintes
razões, que devem constar no artigo:

1. A regra 1 do ponto de continuidade proíbe **pular** a estrutura de D4
   (isto é, publicar `z` diretamente como `ρ` sem passar pela
   representação de suporte/contra-suporte/incerteza/observabilidade,
   proveniência e política). Isso não foi feito: `ρ` é derivado de `B`,
   que por sua vez tem estrutura, proveniência (`G_prov`) e política
   (`π_t`) explícitas que `z` não tem.
2. Em um cenário binário, de fonte única, sem conflito possível (o
   comportamento-verdade é sempre cooperativo, logo nunca há suporte e
   contra-suporte simultaneamente relevantes) e sem histórico acumulado
   entre janelas (D5 fora de escopo), qualquer função coerente de
   suporte/contra-suporte é necessariamente monotônica na proporção de
   sucesso. Isso não é uma limitação escondida: é uma consequência
   correta e esperada do recorte experimental já declarado (D0→D1→D2→D3→D4→D6,
   sem D5, sem evidência indireta, agente determinístico).
3. `ρ` não incorpora `uncertainty` nem `observability` na sua fórmula.
   Essas duas grandezas permanecem no registro como campos próprios de
   `B`, exatamente como a Eq. (7) prevê — o registro carrega `ρ` e `B`
   lado a lado, não apenas `ρ`. Isso preserva a informação que a
   arquitetura exige não colapsar em um único número.

Nenhum modelo nomeado de terceiros (Beta, Subjective Logic, EigenTrust)
foi usado para definir `ρ`; a fórmula é a razão direta dos dois
componentes que a própria arquitetura já nomeia como "suporte" e
"contra-suporte" no texto do artigo-base (seção 3.3).

## V (validade da conclusão)

```
V_{a,c,t} = {
  "valid": evidence_mass > 0,
  "window_start": ...,
  "window_end": ...,
  "invalid_reason": "empty_window" se evidence_mass = 0, senao None,
}
```

Quando `valid=False`, `ρ=NaN` é a representação correta — D6 não imputa um
valor de reputação para uma janela sem nenhuma evidência real ou
imputada, preservando a mesma disciplina que impede D3/D4 de inventar
evidência.

## v_I, θ_I, π_t, p (demais campos do registro)

- `v_I` = versão do operador de D4 já usada (`I_thetaI_binary_v0.1`), mais
  a versão do próprio D6 (`D6_VERSION`).
- `θ_I` = parâmetros do operador de inferência efetivamente usados (nesta
  instanciação, não há hiperparâmetros numéricos além da política).
- `π_t` = a mesma política explícita já carregada por `B` (não
  redefinida em D6).
- `p_{a,c,t}` = a mesma proveniência (`G_prov`) já carregada por `B`.

Nenhum desses campos é recomputado; todos são propagados de D4, evitando
dupla definição da mesma informação em camadas diferentes.

## Correção estrutural necessária antes de D6

As colunas `method` ("M1"/"M2") e `L` (largura da janela) não estavam
propagando como colunas nos DataFrames de D3/D4 na v0.3 — eram mantidas
apenas como chaves de dicionário Python na função de construção da
replicação. Para produzir uma tabela D6 única, concatenável entre L, q e
método (necessária para `add_o100_reference` e as métricas), essas duas
colunas passam a ser atribuídas explicitamente no momento da montagem de
cada condição, antes de D6. Isso não altera nenhum cálculo de D3/D4, é
apenas rotulagem para permitir agregação posterior.

## Invariantes de D6

1. `rho` em `[0,1]` sempre que `evidence_mass > 0`.
2. `rho` é `NaN` se e somente se `valid=False` (evidence_mass=0).
3. Em O100, `rho` de M1 e M2 são idênticos, para todo L (extensão do
   invariante já validado sobre `B`).
4. O contrato mínimo `REQUIRED_D6 = {replication_id, method, q_nominal,
   window_id, rho}`, já previsto desde a v0.2, é satisfeito.

## Próximo gate

Com D6 fechado, o notebook está pronto para:
1. piloto técnico em escala (reconfirmar invariantes, agora incluindo `rho`);
2. congelamento de código/parâmetros;
3. execução científica (R conforme decisão de prazo).
