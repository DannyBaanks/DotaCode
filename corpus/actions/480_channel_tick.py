# 480 channel_tick — (ability, source, dur, effect_per_tick) -> — 
# Con efecto cada tick
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar channel_tick en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a channel_tick. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_channel_tick"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
