# 559 set_summon_command — (summon, command) -> — 
# Orden (attack/move/follow)
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar set_summon_command en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a set_summon_command. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_set_summon_command"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
