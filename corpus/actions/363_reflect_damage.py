# 363 reflect_damage — (target, pct, source?) -> — 
# Refleja % del daño recibido
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar reflect_damage en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a reflect_damage. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_reflect_damage"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
