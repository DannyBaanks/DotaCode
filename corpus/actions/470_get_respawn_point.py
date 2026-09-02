# 470 get_respawn_point — (entity) -> Pos 
# Punto de respawn
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar get_respawn_point en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a get_respawn_point. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_get_respawn_point"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
