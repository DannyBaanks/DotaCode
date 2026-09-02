# 167 cone_cast — (origin, dir, angle, range, filter?) -> [Entity] 
# Todas en cono
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar cone_cast en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a cone_cast. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_cone_cast"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
