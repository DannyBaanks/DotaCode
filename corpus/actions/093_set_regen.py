# 093 set_regen — (entity, resource, rate_per_tick) -> — 
# Fija regeneración/tick
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar set_regen en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a set_regen. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_set_regen"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
