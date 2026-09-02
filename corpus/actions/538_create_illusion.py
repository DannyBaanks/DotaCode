# 538 create_illusion — (source, owner, dur, dmg_out, dmg_in) -> EntityId 
# Con modificadores de daño
# STATUS: CATALOG_ONLY — NOT_EXECUTABLE — NOT_IMPLEMENTED
# Esta acción está en ACTIONS.md pero NO existe aún en src/effects|gamestate|dtypes|prng.
# No es una flashcard ejercitada; es referencia de catálogo para humanos/LLMs.
# Para que sea ejercitada, implementar create_illusion en el runtime y regenerar.
# PRE: — (no aplicable)
# POST: — (no aplicable)

def setup(gs):
    # No-Op honesto: no finge llamar a create_illusion. Marca explícitamente el estado.
    gs.globals["CATALOG_ONLY_create_illusion"] = True
    # NOT_IMPLEMENTED — no se verifica comportamiento
    pass
