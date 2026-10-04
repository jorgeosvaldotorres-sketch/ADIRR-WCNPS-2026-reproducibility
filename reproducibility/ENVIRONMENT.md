# Validated execution environments

The frozen notebook was cross-validated in two independent software environments.

| Environment | Python | NumPy | Pandas |
|---|---:|---:|---:|
| Google Colab (researcher execution) | 3.13.15 | 2.1.3 | 2.2.3 |
| Independent local validation | 3.11.15 | 2.4.6 | 3.0.6 |

The pilot produced numerically identical results to six decimal places across all 24 experimental conditions in both environments.

This documents cross-environment computational reproducibility for the tested configurations. It does not imply compatibility with arbitrary future library versions.

The frozen notebook and freeze manifest are the authoritative executable and configuration records for reruns.
