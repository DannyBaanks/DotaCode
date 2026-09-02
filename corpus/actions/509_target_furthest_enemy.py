# 509 target_furthest_enemy — (source) -> Entity? 
# Enemigo más lejano
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar target_furthest_enemy en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a target_furthest_enemy. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_target_furthest_enemy"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
