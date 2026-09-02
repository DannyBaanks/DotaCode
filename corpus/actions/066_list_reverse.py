# 066 list_reverse — (name) -> — 
# Invierte in-place
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar list_reverse en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a list_reverse. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_list_reverse"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
