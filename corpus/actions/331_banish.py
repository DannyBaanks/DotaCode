# 331 banish — (target, dur) -> — 
# Dispara modifiers temporalmente
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar banish en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a banish. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_banish"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
