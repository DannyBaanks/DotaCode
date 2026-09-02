# 165 ray_cast — (from, dir, max_dist, filter?) -> Entity? 
# Rayo hasta max_dist
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar ray_cast en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a ray_cast. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_ray_cast"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
