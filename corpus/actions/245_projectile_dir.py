# 245 projectile_dir — (projectile) -> (dx,dy) 
# Dirección actual
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar projectile_dir en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a projectile_dir. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_projectile_dir"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
