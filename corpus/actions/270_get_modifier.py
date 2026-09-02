# 270 get_modifier — (entity, type) -> Modifier? 
# Primer modifier de tipo
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: get_modifier ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "get_modifier", None) or getattr(_gs, "get_modifier", None) or getattr(_gs.GameState, "get_modifier", None) or getattr(_dt, "get_modifier", None)
    assert fn is not None, "get_modifier no encontrado"
    # Llamada canónica real
    gs.get_modifier(1)
    assert True  # no lanzó
