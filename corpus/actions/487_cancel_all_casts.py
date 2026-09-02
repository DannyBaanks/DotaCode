# 487 cancel_all_casts — (entity) -> — 
# Cancela todas
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar cancel_all_casts en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a cancel_all_casts. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_cancel_all_casts"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
