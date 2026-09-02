# 230 spawn_chaining — (source, target, speed, payload, jumps) -> EntityId 
# Encadena en secuencia
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar spawn_chaining en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a spawn_chaining. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_spawn_chaining"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
