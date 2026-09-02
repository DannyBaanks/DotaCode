# 702 output_entity_state — (entity, key?) -> — 
# Volcado de entity
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar output_entity_state en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a output_entity_state. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_output_entity_state"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
