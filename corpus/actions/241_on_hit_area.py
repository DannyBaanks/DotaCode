# 241 on_hit_area — (projectile, area, effect) -> — 
# Impacta área
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar on_hit_area en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a on_hit_area. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_on_hit_area"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
