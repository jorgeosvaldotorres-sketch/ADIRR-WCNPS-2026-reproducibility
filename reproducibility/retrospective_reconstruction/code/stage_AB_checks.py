"""
Etapas A (integridade estática) e B (invariantes) — reconstrução retrospectiva de reprodução técnica.
Não produz resultados científicos: apenas verifica invariantes em réplicas 0..N-1 da grade já congelada.
"""
import sys, ast, json
import numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from frozen_loader import load_frozen, NOTEBOOK_SHA256, DEF_CELLS
nb_path, out_json = sys.argv[1], sys.argv[2]
N = int(sys.argv[3]) if len(sys.argv) > 3 else 20
ns, cell_hashes = load_frozen(nb_path)
res = {"A": {}, "B": {}}
A = res["A"]
A["notebook_sha256_ok"] = True
A["cell_sha256"] = cell_hashes
cfg = ns["CFG"]
A["config_matches_freeze_manifest"] = (cfg.master_seed, cfg.T, cfg.L_levels, cfg.q_levels, cfg.pilot_replications,
    cfg.scientific_replications, cfg.mcse_ratio_target, cfg.neutral_weight_positive, cfg.neutral_weight_negative) == \
    (20260922, 1000, (25, 50, 100), (1.0, 0.8, 0.6, 0.4), 100, 2000, 0.025, 0.5, 0.5)
# nenhum nome congelado é redefinido nos módulos retrospectivos
frozen_names = {n for i in DEF_CELLS for n in
    [x.name for x in ast.parse("".join(json.load(open(nb_path))["cells"][i]["source"])).body if isinstance(x, (ast.FunctionDef, ast.ClassDef))]}
redef = {}
for f in ("retro_reproduction.py", "compare_with_historical.py", "frozen_loader.py"):
    tree = ast.parse(open(__file__.rsplit("/", 1)[0] + "/" + f).read())
    redef[f] = sorted(frozen_names & {x.name for x in ast.walk(tree) if isinstance(x, (ast.FunctionDef, ast.ClassDef))})
A["frozen_function_names"] = sorted(frozen_names)
A["frozen_names_redefined_in_retro_code"] = redef
A["seed_policy_ok"] = all(np.array_equal(ns["generate_uniform_stream"](r),
    np.random.default_rng(np.random.SeedSequence(20260922, spawn_key=(r,))).random(1000)) for r in (0, 1, 1999))
# Etapa B
B = res["B"]; fails = []; counts = dict(reps=N, o100_m1_eq_m2=0, m2_unc0_valid=0, m1_struct_o40=0, rho_bounds=0,
    nested_masks=0, same_opportunities_windows=0, m2_neutral_count=0, m1_no_neutral=0, m2_rho_formula=0, invalid_handling=0)
for r in range(N):
    d4 = ns["build_replication_through_d4"](r)
    d6 = ns["run_d6_over_grid"](d4)
    try:
        ns["test_o100_m1_equals_m2"](d6); counts["o100_m1_eq_m2"] += 1
        ns["test_m2_uncertainty_always_zero_and_rho_valid"](d6); counts["m2_unc0_valid"] += 1
        ns["test_m1_uncertainty_and_rho_structural_at_o40"](d6); counts["m1_struct_o40"] += 1
        ns["test_rho_bounds"](d6); counts["rho_bounds"] += 1
        masks = ns["nested_observation_masks"](ns["generate_uniform_stream"](r)); counts["nested_masks"] += 1
        # mesmas oportunidades/janelas entre M1 e M2 (B sobre janelas): mesma estrutura de chaves
        ok = True
        for (L, q), mm in d4.items():
            a, b = mm["M1"], mm["M2"]
            ok &= a["window_id"].equals(b["window_id"]) and len(a) == cfg.T // L
        assert ok; counts["same_opportunities_windows"] += 1
        # preservação do tratamento de ausência (M1) e pseudo-evidência neutra (M2) via entradas pré-D3
        d1 = ns["validate_d1"](ns["generate_d0_events"](r))
        for L in cfg.L_levels:
            for q in cfg.q_levels:
                d2 = ns["assign_d2_windows"](ns["attach_observability"](d1, masks[q], q), L)
                m1, m2 = ns["prepare_m1_input"](d2), ns["prepare_m2_input"](d2)
                assert (m2["evidence_kind"] == "neutral_imputation").sum() == (~d2["observed"]).sum()
                assert (m1["evidence_kind"] == "neutral_imputation").sum() == 0
                assert m1.loc[~m1["observed"], "support_positive"].isna().all()
                assert (m2.loc[~m2["observed"], ["support_positive", "support_negative"]] == 0.5).all().all()
        counts["m2_neutral_count"] += 1; counts["m1_no_neutral"] += 1
        # M2: rho = 0.5 + 0.5*taxa observada na janela (identidade algébrica documentada)
        m2 = d6[d6["method"] == "M2"]
        for (L, q), g in m2.groupby(["L", "q_nominal"]):
            mask = masks[q]; K = cfg.T // L
            rate = mask.reshape(K, L).mean(axis=1)
            assert np.allclose(g.sort_values("window_id")["rho"].to_numpy(), 0.5 + 0.5 * rate)
        counts["m2_rho_formula"] += 1
        inv = d6[~d6["valid"]]
        assert (inv["method"] == "M1").all() and (inv["q_nominal"] < 1).all() and inv["rho"].isna().all()
        assert (np.isclose(d6.loc[~d6["valid"], "support"] + d6.loc[~d6["valid"], "counter_support"], 0)).all()
        counts["invalid_handling"] += 1
    except AssertionError as e:
        fails.append((r, repr(e)[:200]))
B["counts"] = counts; B["failures"] = fails
res["pass_A"] = bool(A["config_matches_freeze_manifest"] and A["seed_policy_ok"] and not any(redef.values()))
res["pass_B"] = not fails and all(v == N for k, v in counts.items() if k != "reps")
json.dump(res, open(out_json, "w"), indent=2)
print(json.dumps({"pass_A": res["pass_A"], "pass_B": res["pass_B"], "B": B, "redef": redef,
                  "config_ok": A["config_matches_freeze_manifest"], "seed_ok": A["seed_policy_ok"]}, indent=1))
