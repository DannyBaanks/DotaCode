# 104 get_resource_pct — (entity, resource) -> Float 
# Porcentaje actual/max
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar get_resource_pct en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a get_resource_pct. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_get_resource_pct"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
