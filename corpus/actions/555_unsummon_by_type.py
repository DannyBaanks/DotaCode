# 555 unsummon_by_type — (owner, type) -> — 
# Por tipo
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar unsummon_by_type en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a unsummon_by_type. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_unsummon_by_type"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
