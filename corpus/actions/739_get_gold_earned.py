# 739 get_gold_earned — (entity) -> Int 
# Oro ganado
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar get_gold_earned en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a get_gold_earned. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_get_gold_earned"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
