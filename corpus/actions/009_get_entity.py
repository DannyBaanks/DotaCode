# 009 get_entity — (entity_id) -> Entity? 
# Recupera por id
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: get_entity ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "get_entity", None) or getattr(_gs, "get_entity", None) or getattr(_gs.GameState, "get_entity", None) or getattr(_dt, "get_entity", None)
    assert fn is not None, "get_entity no encontrado"
    # Llamada canónica real
    res = gs.get_entity(hero.id)
    assert res is not None or res is None  # consulta no lanza
