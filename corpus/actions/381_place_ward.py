# 381 place_ward — (owner, x, y, type, dur, vision_radius) -> EntityId 
# Ward con visión de área
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar place_ward en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a place_ward. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_place_ward"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
