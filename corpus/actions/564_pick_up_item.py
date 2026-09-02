# 564 pick_up_item — (hero, ground_item) -> — 
# Recoge
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar pick_up_item en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a pick_up_item. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_pick_up_item"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
