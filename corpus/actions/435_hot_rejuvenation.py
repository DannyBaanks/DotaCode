# 435 hot_rejuvenation — (target, dur, hot_per_tick, burst) -> — 
# HOT + burst al expirar
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar hot_rejuvenation en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a hot_rejuvenation. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_hot_rejuvenation"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
