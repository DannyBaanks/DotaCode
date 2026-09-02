# 030 state_gt — (entity, key, value) -> Bool 
# state > value
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar state_gt en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a state_gt. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_state_gt"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
