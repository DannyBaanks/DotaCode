# 257 set_stacks — (modifier, n) -> — 
# Fija stacks
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar set_stacks en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a set_stacks. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_set_stacks"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
