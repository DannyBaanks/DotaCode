# 101 share_resource — (entity, resource, allies, pct) -> — 
# Distribuye entre aliados
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar share_resource en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a share_resource. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_share_resource"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
