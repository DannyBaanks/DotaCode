# 519 targets_in_line — (from, to, width, filter?) -> [Entity] 
# Todas en línea
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar targets_in_line en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a targets_in_line. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_targets_in_line"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
