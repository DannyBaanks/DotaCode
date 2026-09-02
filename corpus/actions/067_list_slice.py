# 067 list_slice — (name, start, end) -> List 
# Sublista
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar list_slice en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a list_slice. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_list_slice"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
