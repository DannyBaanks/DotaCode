# 678 random_enemy_of — (entity) -> Entity? 
# Enemigo aleatorio
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar random_enemy_of en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a random_enemy_of. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_random_enemy_of"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
