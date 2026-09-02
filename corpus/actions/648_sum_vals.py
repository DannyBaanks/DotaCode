# 648 sum_vals — (values[]) -> Float 
# Suma
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar sum_vals en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a sum_vals. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_sum_vals"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
