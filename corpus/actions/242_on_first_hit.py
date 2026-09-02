# 242 on_first_hit — (projectile, effect) -> — 
# Primer impacto
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar on_first_hit en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a on_first_hit. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_on_first_hit"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
