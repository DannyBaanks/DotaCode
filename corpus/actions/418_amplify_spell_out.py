# 418 amplify_spell_out — (entity, pct, dur?) -> — 
# Amplifica daño saliente
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar amplify_spell_out en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a amplify_spell_out. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_amplify_spell_out"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
