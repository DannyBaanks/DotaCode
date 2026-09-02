# 160 area_union — (a, b) -> Area 
# Unión
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar area_union en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a area_union. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_area_union"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
