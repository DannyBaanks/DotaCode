# 365 reflect_exact — (target, pct) -> — 
# Reflejo exacto
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar reflect_exact en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a reflect_exact. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_reflect_exact"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
