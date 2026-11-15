"""
Comparação registro a registro e de agregados (reconstrução retrospectiva vs CSVs históricos).
TOLERÂNCIAS DECLARADAS ANTES DA EXECUÇÃO COMPLETA (não alteradas depois):
  - Estrutural: igualdade exata de colunas, chaves, contagens.
  - Numérico: "igual exato" = igualdade bit a bit; "diferença de ponto flutuante" = |a-b| <= 1e-12 + 1e-9*|b|;
    acima disso = "divergência efetiva". (Entre ambientes distintos o freeze histórico relata concordância
    até a 6ª casa; para a Etapa D usa-se atol=1e-9, declarado em separado.)
"""
import sys, json
import numpy as np, pandas as pd
ATOL, RTOL = 1e-12, 1e-9

def cmp_frames(h, r, keys, name):
    out = {"name": name}
    out["cols_hist"], out["cols_retro"] = list(h.columns), list(r.columns)
    out["same_columns_and_order"] = list(h.columns) == list(r.columns)
    out["rows_hist"], out["rows_retro"] = len(h), len(r)
    out["dup_keys_hist"] = int(h.duplicated(keys).sum()); out["dup_keys_retro"] = int(r.duplicated(keys).sum())
    m = h.merge(r, on=keys, how="outer", suffixes=("_h", "_r"), indicator=True)
    out["only_in_hist"] = int((m["_merge"] == "left_only").sum()); out["only_in_retro"] = int((m["_merge"] == "right_only").sum())
    both = m[m["_merge"] == "both"]
    out["same_row_order"] = bool(h[keys].reset_index(drop=True).equals(r[keys].reset_index(drop=True)))
    vals = [c for c in h.columns if c not in keys]
    out["columns"] = {}
    for c in vals:
        a, b = both[c + "_r"].to_numpy(dtype=float), both[c + "_h"].to_numpy(dtype=float)
        exact = (a == b) | (np.isnan(a) & np.isnan(b))
        diff = np.abs(a - b)
        fp = (~exact) & (diff <= ATOL + RTOL * np.abs(b))
        eff = (~exact) & ~fp
        out["columns"][c] = dict(n=len(a), exact=int(exact.sum()), fp_only=int(fp.sum()), effective=int(eff.sum()),
                                 max_abs_diff=float(np.nanmax(diff)) if len(diff) else 0.0)
    out["all_exact"] = out["same_columns_and_order"] and out["only_in_hist"] == 0 and out["only_in_retro"] == 0 and \
        all(v["exact"] == v["n"] for v in out["columns"].values())
    out["any_effective_divergence"] = any(v["effective"] > 0 for v in out["columns"].values()) or \
        out["only_in_hist"] > 0 or out["only_in_retro"] > 0
    return out

def main(hist_dir, retro_dir, out_json, atol=None):
    global ATOL
    if atol is not None: ATOL = atol
    rd = lambda d, n: pd.read_csv(f"{d}/{n}")
    res = {}
    res["per_replicacao"] = cmp_frames(rd(hist_dir, "execucao_cientifica_per_replicacao.csv"),
        rd(retro_dir, "retro_per_replicacao.csv"), ["replication_id", "method", "q_nominal", "L"], "per_replicacao")
    res["metricas_finais"] = cmp_frames(rd(hist_dir, "execucao_cientifica_metricas_finais.csv"),
        rd(retro_dir, "retro_metricas_finais.csv"), ["method", "q_nominal", "L"], "metricas_finais")
    res["delta_pareado"] = cmp_frames(rd(hist_dir, "execucao_cientifica_delta_pareado.csv"),
        rd(retro_dir, "retro_delta_pareado.csv"), ["q_nominal", "L"], "delta_pareado")
    h = rd(hist_dir, "execucao_cientifica_per_replicacao.csv"); r = rd(retro_dir, "retro_per_replicacao.csv")
    res["structure"] = dict(rows_retro=len(r), n_replication_ids=int(r.replication_id.nunique()),
        n_conditions=int(len(r.groupby(["method", "q_nominal", "L"]))), n_invalid_sum_retro=int(r.n_invalid.sum()),
        n_invalid_sum_hist=int(h.n_invalid.sum()), dup_keys=int(r.duplicated(["replication_id","method","q_nominal","L"]).sum()))
    res["tolerance"] = dict(atol=ATOL, rtol=RTOL)
    json.dump(res, open(out_json, "w"), indent=2)
    return res

if __name__ == "__main__":
    r = main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else None)
    for k in ("per_replicacao", "metricas_finais", "delta_pareado"):
        v = r[k]; print(k, "all_exact=", v["all_exact"], "effective_div=", v["any_effective_divergence"],
                        {c: (x["exact"], x["fp_only"], x["effective"], x["max_abs_diff"]) for c, x in v["columns"].items()})
    print(r["structure"])
