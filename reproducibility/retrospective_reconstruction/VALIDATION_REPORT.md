# Relatório de validação — reconstrução retrospectiva (2026-11-15)

**Resultado final: APROVADO COM RESSALVAS** (critérios do documento de autorização, §8).

## Procedimento
Área isolada fora dos repositórios (`/home/user/adirr_retro_workspace`); entradas copiadas e marcadas somente leitura, hashes em `validation/input_hashes.sha256`; cópias pública e privada conferidas como idênticas (notebook e 6 arquivos de resultados). Tolerâncias fixadas antes da execução completa: estrutura exata; numérico "exato" = bit a bit; "ponto flutuante" = |a−b| ≤ 1e-12 + 1e-9·|b|.

Definições adotadas a priori (a rotina original não existe para consulta): `DMA_r`, `MAE_r` = `summarize_replication_metrics` congelada; `Delta_r` = DMA_r(M2) − DMA_r(M1) na mesma (réplica,q,L); `n_invalid` = janelas com `valid=False`; `DP_Rep` = desvio-padrão ddof=1 de `DMA_r`; `MCSE` = `mcse()` congelada.

## Etapa A — integridade estática: aprovada
Hash do notebook confere; células executadas literalmente (hash por célula em `stage_AB.json`); `ProtocolConfig` = manifesto de freeze; nenhum nome de função congelada redefinido no código retrospectivo; política de sementes (`SeedSequence(20260922, spawn_key=(rep,))`) confere nas réplicas 0, 1 e 1999.

## Etapa B — invariantes (réplicas 0–19): aprovada
M1=M2 em O100; incerteza/ρ estruturais de M1 em O40; M2 sempre válido com incerteza 0; ρ∈[0,1]; máscaras aninhadas; mesmas janelas M1/M2; contagem de pseudo-evidência neutra (0,5; 0,5) só em M2 e ausência preservada em M1; ρ(M2)=0,5+0,5·taxa observada. **Ressalva:** a grade real não contém janela inválida (n_invalid=0 também no histórico), então esse ramo foi verificado apenas por teste unitário controlado de `run_d6` (`stage_B_invalid_window_unit_check.json`), não por dados reais.

## Etapa C — reprodução técnica (R=2000, 24 condições)
Estrutura: 48.000 registros, 2.000 réplicas, 24 condições, 0 chaves duplicadas, 0 faltantes/excedentes, mesmas colunas e ordem de colunas, n_invalid total 0 (= histórico).

| Arquivo | Resultado |
|---|---|
| `per_replicacao` (48.000 registros, chave réplica+método+q+L) | **100% igualdade exata** em DMA_r, MAE_r, n_invalid, Delta_r. Arquivo **byte a byte idêntico** (SHA-256 `d9acb1d9368c02b736a7d82f777d2a01fbd165bca27158dea917cde93b253130`). |
| `metricas_finais` (24 linhas) | DP_Rep, MCSE_DMA, MCSE_MAE, n_rep exatos; DMA exato em 20/24 e MAE em 18/24; as demais diferem **1 ulp (1,1e-16)**, dentro da tolerância. |
| `delta_pareado` (12 linhas) | MCSE_Delta exato; Delta_bar exato em 8/12, 4 com 1,1e-16. |

Divergências efetivas: **nenhuma**. Divergências estruturais: **nenhuma**.
Origem das diferenças de 1 ulp: não determinada; é compatível com ordem de soma/agrupamento distinta na agregação original (**hipótese, não verificada**; a rotina original é desconhecida).

## Etapa D — segundo ambiente
| Ambiente | Python | NumPy | Pandas | Tempo (4 proc.) |
|---|---|---|---|---|
| 1 | 3.13.18 | 2.5.3 | 3.0.5 | 146 s |
| 2 | 3.13.18 | 2.1.3 | 2.2.3 | 138 s |

Saídas dos dois ambientes **idênticas byte a byte** entre si (3 CSVs) e com os mesmos resultados da comparação histórica. **Ressalva:** mesma máquina, SO e versão de Python; só NumPy/Pandas variaram (inclui as versões NumPy 2.1.3/Pandas 2.2.3 do Colab original, mas não o Python 3.13.15 dele). Não é independência de hardware/SO.

## Ressalvas finais
1. Definições de `DP_Rep` (ddof=1), `Delta_r` e `n_invalid` foram escolhidas a priori e **confirmadas** pelos dados, mas a rotina original continua desconhecida.
2. Ramo de janela inválida só por teste unitário.
3. Etapa D com independência limitada.
4. Esta validação não prova que o mesmo código rodou em setembro de 2026.
