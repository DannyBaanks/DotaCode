# 341 on_exit_aura — (aura, effect) -> — 
# Al salir del radio
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar on_exit_aura en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a on_exit_aura. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_on_exit_aura"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
