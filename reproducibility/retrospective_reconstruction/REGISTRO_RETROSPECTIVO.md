# Registro de rastreabilidade da reconstrução retrospectiva

- Data: 2026-11-15 · Responsável: Claude (Anthropic), sessão de assistência, a pedido do pesquisador
- Origem: `jorgeosvaldotorres-sketch/doutorado-ppgee-unb`, commit `3376de5` (notebook); resultados `06342bc9196fd1795a5b604cadf365b98036dd6e`
- Hash notebook: `97f4a43d95ecf0cf8e081e9ad7614809f1c97cde3fb1714d727b1f6987a0b491`
- Hashes dos CSVs históricos: `validation/input_hashes.sha256` (per_replicacao `d9acb1d9368c02b736a7d82f777d2a01fbd165bca27158dea917cde93b253130`; metricas_finais `d88347a3db68f3d6be5306704ce7628d981ea97bab8a5b73f1f1da566cbe20e2`; delta_pareado `256e15512515e7237572a37904effa305d941bfd5c368fee38271a55f93bc91d`)
- Funções congeladas reutilizadas: `ProtocolConfig`, `child_rng`, `generate_uniform_stream`, `nested_observation_masks`, `generate_d0_events`, `validate_d1`, `attach_observability`, `assign_d2_windows`, `prepare_m1/m2_input`, `check_pre_d3_invariants`, `run_d3`, `run_d4`, `run_d6`, `check_d6_contract`, `run_d6_over_grid`, `build_replication_through_d4`, `add_o100_reference`, `mcse`, `summarize_replication_metrics`, testes da célula 25.
- Rotinas retrospectivas: laço de réplicas com `multiprocessing` (4 processos), `Delta_r`, `n_invalid`, agregação, escrita de CSV, comparador.
- Comandos: ver README. Resultados: VALIDATION_REPORT.md e `validation/comparison_env{1,2}.json`.
- Lacunas das funções congeladas: o notebook não define `n_invalid`, `Delta_r`, `DP_Rep`, agregação por condição nem exportação (documentado; não alterado).
- Resultado final: **aprovado com ressalvas**.
- Commit/URL de publicação: ver relatório de entrega da sessão (preenchido após publicação).
