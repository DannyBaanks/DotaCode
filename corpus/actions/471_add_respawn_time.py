# 471 add_respawn_time — (entity, delta) -> — 
# Añade/quita tiempo
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar add_respawn_time en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a add_respawn_time. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_add_respawn_time"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
