# 584 is_in_shop_range — (hero) -> Bool 
# Cerca de tienda
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar is_in_shop_range en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a is_in_shop_range. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_is_in_shop_range"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
