# ADIRR WCNPS 2026 — Operacionalização de D3 v0.1

Data: 2026-09-22  
Status: implementada no notebook Colab v0.2 e validada por smoke test.

## Base no artigo-base

O artigo-base define D3 por:

`z_{a,c,t} = φ(E_{a,c}(W_t), m_{a,c}(W_t), θ_φ)`.

O texto associado estabelece que:

- D3 transforma a janela de eventos e a máscara de observação em uma representação comportamental;
- candidatos de features incluem taxas de sucesso/falha, atraso, disponibilidade, tendência, volatilidade, recorrência/mudança comportamental e concentração de fontes;
- a lista é um repertório de projeto, não uma lista obrigatória;
- a seleção depende do domínio, das propriedades observáveis e do mecanismo de inferência;
- `z` pode conter features interpretáveis ou um estado latente com incerteza;
- a representação comportamental não é reputação.

## Decisão de instanciação

Para o primeiro cenário WCNPS, o domínio é binário, cooperativo, estacionário e sem recomendações indiretas.

A instanciação mínima de `φ` seleciona somente features diretamente justificadas pelo cenário:

1. taxa de sucesso na evidência disponível;
2. taxa de falha na evidência disponível;
3. taxa de observabilidade da janela, derivada da máscara;
4. massa de evidência e contagens auxiliares para auditoria.

Também são preservados:
- número de oportunidades;
- número de observações;
- número de ausências;
- suportes positivo e negativo agregados;
- quantidade de imputações neutras em M2;
- versão da extração;
- parâmetros `θ_φ`.

## Regra metodológica

Esta implementação **não cria uma nova equação arquitetural**.

Ela instancia o operador `φ` já previsto pela Eq. (4), selecionando features que o próprio artigo-base lista como admissíveis.

As definições computacionais de taxa e contagem são decisões de implementação do experimento e não substituem a formulação da arquitetura.

## M1 e M2

### M1 — observabilidade explícita
- posições observadas carregam a evidência real;
- posições ausentes não adicionam suporte positivo ou negativo;
- em agente cooperativo determinístico, a taxa de sucesso deve permanecer 1 nas janelas com evidência observada.

### M2 — imputação neutra
- posições observadas são idênticas a M1;
- posições ausentes adicionam pseudo-suporte `(0,5;0,5)`;
- a massa de evidência cresce, sem direção líquida da pseudo-evidência;
- a taxa de sucesso pode deslocar-se em direção à neutralidade à medida que a observabilidade cai.

## Invariantes D3

A implementação verifica:

1. taxa de observabilidade em `[0,1]`;
2. em janelas com massa de evidência, taxa de sucesso + taxa de falha = 1;
3. M1 e M2 preservam a mesma taxa de observabilidade para a mesma máscara;
4. em M2, número de imputações neutras = número de ausências;
5. D3 não produz `ρ` e não executa inferência reputacional.

## Smoke test

O smoke test executado para a replicação 0 em O40 produziu:

- 20 janelas;
- M1: taxa média de sucesso = 1,0;
- M2: taxa média de sucesso = 0,6825;
- taxa média realizada de observabilidade = 0,365.

Esses valores são usados apenas para validação técnica da infraestrutura e **não constituem resultado científico**.

## Próximo gate

D4 permanece não implementado.

A próxima etapa é operacionalizar fielmente D4 a partir da Eq. (5) e do texto do artigo-base, preservando a distinção:

- representação comportamental `z`;
- evidência direta complementar não codificada em `z`;
- evidência indireta;
- proveniência/dependência;
- política;
- estado de crença contextual.
