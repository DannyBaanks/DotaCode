# 023 get_state_default — (entity, key, default) -> Value 
# Lee con default si no existe
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar get_state_default en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a get_state_default. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_get_state_default"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
