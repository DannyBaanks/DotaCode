# 003 exists — (entity) -> Bool 
# Verdadero si entity está viva
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar exists en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a exists. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_exists"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
