# 019 set_state_if — (entity, key, value, cond) -> — 
# Asigna solo si condición se cumple
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar set_state_if en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a set_state_if. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_set_state_if"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
