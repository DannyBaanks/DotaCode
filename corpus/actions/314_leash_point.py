# 314 leash_point — (target, point, max_dist, dur) -> — 
# No alejarse de punto
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar leash_point en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a leash_point. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_leash_point"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
