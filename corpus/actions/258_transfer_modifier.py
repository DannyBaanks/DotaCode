# 258 transfer_modifier — (modifier, new_target) -> — 
# Mueve a otra entity
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar transfer_modifier en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a transfer_modifier. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_transfer_modifier"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
