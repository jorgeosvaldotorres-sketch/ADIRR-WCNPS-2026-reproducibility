# Reconstrução retrospectiva de reprodução técnica — ADIRR WCNPS/ICITS 2026

> **Reconstrução retrospectiva de reprodução técnica, desenvolvida após a execução científica original de setembro de 2026. Não representa a recuperação da rotina histórica.**

- Data de criação: 2026-11-15
- Origem das funções: notebook congelado `ADIRR_WCNPS_2026_COLAB_v0_4.ipynb`, commit `3376de5`, SHA-256 `97f4a43d95ecf0cf8e081e9ad7614809f1c97cde3fb1714d727b1f6987a0b491`
- Resultados de referência: commit `06342bc9196fd1795a5b604cadf365b98036dd6e`

## Estado separado dos dois processos

| | Estado |
|---|---|
| **Auditoria histórica** (15/11/2026) | A rotina original de orquestração das 2.000 réplicas **não foi recuperada**. Conclusão inalterada. |
| **Reprodução técnica retrospectiva** | Código posterior reproduz os CSVs históricos (ver `VALIDATION_REPORT.md`). **Aprovada com ressalvas** (ressalvas no relatório). |

Uma reprodução validada **não comprova** que o mesmo código foi executado em setembro de 2026. Ela mostra que a instanciação congelada pode ser reproduzida por uma rotina posterior, nas condições verificadas.

## O que contém

- `code/frozen_loader.py` — executa sem alteração as células de código do notebook v0.4 (verifica o hash antes). Nenhuma função congelada é copiada ou reescrita.
- `code/retro_reproduction.py` — orquestração retrospectiva (laço de réplicas, `Delta_r`, `n_invalid`, agregados, CSVs).
- `code/compare_with_historical.py` — comparação registro a registro e de agregados, com tolerâncias declaradas a priori.
- `code/stage_AB_checks.py` — integridade estática e invariantes.
- `validation/` — resultados da comparação, metadados de execução, versões, hashes de entrada.
- `VALIDATION_REPORT.md`, `REGISTRO_RETROSPECTIVO.md` (log de rastreabilidade), `CHANGELOG.md`, `MANIFEST_SHA256.txt`.

Os CSVs históricos **não** são duplicados: ficam em `results/` (repositório público) e `05_Experimentos/ADIRR_WCNPS_2026/04_resultados/` (privado).

## Como reproduzir (não escreve nos repositórios; use diretório de trabalho isolado)

```bash
W=$(mktemp -d); mkdir $W/inputs $W/out
cp <notebook v0.4 do commit 3376de5> $W/inputs/ADIRR_WCNPS_2026_COLAB_v0_4.ipynb
python3 -I code/stage_AB_checks.py $W/inputs/ADIRR_WCNPS_2026_COLAB_v0_4.ipynb $W/out/stage_AB.json 20
python3 -I code/retro_reproduction.py $W/inputs/ADIRR_WCNPS_2026_COLAB_v0_4.ipynb $W/out/env
# HIST = pasta com os 3 CSVs históricos (cópia)
python3 -I code/compare_with_historical.py $HIST $W/out/env $W/out/comparison.json
```

Dependências: Python 3.13, NumPy, Pandas (versões testadas em `validation/env*_freeze.txt`). Tempo ≈ 2,5 min com 4 processos.
