# 367 redirect_damage — (target, pct, to) -> — 
# Redirige daño a otra entity
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar redirect_damage en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a redirect_damage. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_redirect_damage"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
