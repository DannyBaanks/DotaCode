# 099 transfer_pct — (from, to, resource, pct) -> — 
# Transfiere porcentaje
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar transfer_pct en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a transfer_pct. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_transfer_pct"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
