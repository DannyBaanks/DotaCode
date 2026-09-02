# 493 copy_cast — (target, ability, source, params) -> — 
# Copia y ejecuta en otro
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar copy_cast en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a copy_cast. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_copy_cast"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
