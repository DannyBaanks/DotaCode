# 343 aura_affects_enemies — (aura) -> — 
# Configura para enemigos
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar aura_affects_enemies en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a aura_affects_enemies. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_aura_affects_enemies"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
