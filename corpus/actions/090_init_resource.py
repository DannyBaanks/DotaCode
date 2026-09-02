# 090 init_resource — (entity, resource, value) -> — 
# Solo si no existía
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar init_resource en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a init_resource. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_init_resource"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
