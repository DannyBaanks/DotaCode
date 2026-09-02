# 536 summon_skeleton — (owner, dur, count) -> [EntityId] 
# Varios esqueletos
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar summon_skeleton en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a summon_skeleton. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_summon_skeleton"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
