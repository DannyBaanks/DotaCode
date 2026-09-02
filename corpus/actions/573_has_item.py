# 573 has_item — (hero, item) -> Bool 
# Tiene el item
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar has_item en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a has_item. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_has_item"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
