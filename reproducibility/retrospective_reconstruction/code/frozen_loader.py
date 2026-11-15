"""
RECONSTRUÇÃO RETROSPECTIVA DE REPRODUÇÃO TÉCNICA (loader).
Reconstrução retrospectiva de reprodução técnica, desenvolvida após a execução
científica original de setembro de 2026. Não representa a recuperação da
rotina histórica.

Carrega as funções CONGELADAS executando, sem alteração, as células de código
do notebook v0.4 (commit 3376de5). Nenhuma função congelada é copiada ou
reescrita aqui. O hash do notebook é verificado antes de qualquer execução.
"""
import hashlib, json

NOTEBOOK_SHA256 = "97f4a43d95ecf0cf8e081e9ad7614809f1c97cde3fb1714d727b1f6987a0b491"
# Células de código que apenas DEFINEM funções/configuração (e, em 21/23, rodam a réplica 0
# como no notebook original). Células 27 e 29 (resumo de smoke e checks globais) não são necessárias.
DEF_CELLS = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25)

def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def load_frozen(notebook_path):
    h = sha256_file(notebook_path)
    assert h == NOTEBOOK_SHA256, f"Hash do notebook difere do congelado: {h}"
    nb = json.load(open(notebook_path, encoding="utf-8"))
    ns = {"__name__": "frozen_v0_4"}
    cell_hashes = {}
    for i in DEF_CELLS:
        c = nb["cells"][i]
        assert c["cell_type"] == "code"
        src = "".join(c["source"])
        cell_hashes[i] = hashlib.sha256(src.encode("utf-8")).hexdigest()
        exec(compile(src, f"<notebook_v0_4_cell_{i}>", "exec"), ns)
    return ns, cell_hashes
