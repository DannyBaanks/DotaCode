# 532 summon_leashed — (type, owner, pos, leash_r, dur) -> EntityId 
# Con leash
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar summon_leashed en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a summon_leashed. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_summon_leashed"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
