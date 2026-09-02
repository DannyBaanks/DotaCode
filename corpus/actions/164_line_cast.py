# 164 line_cast — (from, to, filter?) -> Entity? 
# Primera entity en línea
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar line_cast en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a line_cast. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_line_cast"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
