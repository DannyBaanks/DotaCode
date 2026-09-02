# 347 auras_of — (entity) -> [Aura] 
# Auras que le afectan
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar auras_of en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a auras_of. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_auras_of"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
