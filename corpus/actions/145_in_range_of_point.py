# 145 in_range_of_point — (entity, x, y, range) -> Bool 
# Dentro de rango de punto
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar in_range_of_point en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a in_range_of_point. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_in_range_of_point"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
