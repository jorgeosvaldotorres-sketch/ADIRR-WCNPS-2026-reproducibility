"""
RECONSTRUÇÃO RETROSPECTIVA DE REPRODUÇÃO TÉCNICA.
Reconstrução retrospectiva de reprodução técnica, desenvolvida após a execução
científica original de setembro de 2026. Não representa a recuperação da
rotina histórica.

Orquestração complementar: percorre as réplicas, usa as funções congeladas do
notebook v0.4 sem alterá-las e escreve CSVs de estrutura compatível com os
históricos. DEFINIÇÕES ADOTADAS A PRIORI (não ajustadas após ver resultados):
  DMA_r, MAE_r = frozen summarize_replication_metrics (média/ média do |D| por réplica)
  n_invalid    = nº de janelas com valid == False por (réplica, método, q, L)
  Delta_r      = DMA_r(M2) - DMA_r(M1) na mesma (réplica, q, L), atribuído às duas linhas
  DP_Rep       = desvio-padrão (ddof=1) de DMA_r entre réplicas (mesma convenção do mcse congelado)
  MCSE_DMA/MAE = frozen mcse() sobre DMA_r / MAE_r;  Delta_bar/MCSE_Delta = média e mcse de Delta_r
"""
import sys, time, json, platform
import numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from frozen_loader import load_frozen

NB = None
NS = None

def _init(nb_path):
    global NS
    NS, _ = load_frozen(nb_path)

def one_replication(rid):
    d4 = NS["build_replication_through_d4"](rid)
    d6 = NS["run_d6_over_grid"](d4)
    df = NS["add_o100_reference"](d6)
    m = NS["summarize_replication_metrics"](df)
    inv = (df.assign(_inv=~df["valid"].astype(bool))
             .groupby(["replication_id", "method", "q_nominal", "L"], as_index=False)["_inv"].sum()
             .rename(columns={"_inv": "n_invalid"}))
    m = m.merge(inv, on=["replication_id", "method", "q_nominal", "L"], validate="one_to_one")
    return m

def run(nb_path, out_dir, R=None, procs=4):
    ns, cell_hashes = load_frozen(nb_path)
    cfg = ns["CFG"]
    R = cfg.scientific_replications if R is None else R
    t0 = time.time()
    with Pool(procs, initializer=_init, initargs=(nb_path,)) as p:
        parts = p.map(one_replication, range(R), chunksize=20)
    elapsed = time.time() - t0
    per = pd.concat(parts, ignore_index=True)
    # Delta_r = DMA_r(M2) - DMA_r(M1)
    piv = per.pivot_table(index=["replication_id", "q_nominal", "L"], columns="method", values="DMA_r")
    delta = (piv["M2"] - piv["M1"]).rename("Delta_r").reset_index()
    per = per.merge(delta, on=["replication_id", "q_nominal", "L"], validate="many_to_one")
    per = per[["method", "q_nominal", "L", "DMA_r", "MAE_r", "n_invalid", "replication_id", "Delta_r"]]
    mcse = ns["mcse"]
    rows = []
    for (m, q, L), g in per.groupby(["method", "q_nominal", "L"]):
        rows.append(dict(method=m, q_nominal=q, L=L, DMA=g.DMA_r.mean(), MAE=g.MAE_r.mean(),
                         DP_Rep=g.DMA_r.std(ddof=1), MCSE_DMA=mcse(g.DMA_r), MCSE_MAE=mcse(g.MAE_r),
                         n_rep=len(g)))
    fin = pd.DataFrame(rows)
    drows = []
    for (q, L), g in per[per.method == "M2"].groupby(["q_nominal", "L"]):
        drows.append(dict(q_nominal=q, L=L, Delta_bar=g.Delta_r.mean(), MCSE_Delta=mcse(g.Delta_r)))
    dlt = pd.DataFrame(drows)
    import os; os.makedirs(out_dir, exist_ok=True)
    per.to_csv(f"{out_dir}/retro_per_replicacao.csv", index=False)
    fin.to_csv(f"{out_dir}/retro_metricas_finais.csv", index=False)
    dlt.to_csv(f"{out_dir}/retro_delta_pareado.csv", index=False)
    meta = dict(retrospective=True, R=R, elapsed_s=elapsed, procs=procs,
                python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__,
                platform=platform.platform(), notebook_cell_sha256=cell_hashes,
                master_seed=cfg.master_seed, T=cfg.T, L=list(cfg.L_levels), q=list(cfg.q_levels))
    json.dump(meta, open(f"{out_dir}/retro_run_metadata.json", "w"), indent=2)
    return meta

if __name__ == "__main__":
    nb, out = sys.argv[1], sys.argv[2]
    R = int(sys.argv[3]) if len(sys.argv) > 3 else None
    print(json.dumps(run(nb, out, R), indent=2))
