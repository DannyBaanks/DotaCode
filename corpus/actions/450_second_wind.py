# 450 second_wind — (entity, dur) -> — 
# Daño letal cura en vez de matar
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar second_wind en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a second_wind. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_second_wind"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
