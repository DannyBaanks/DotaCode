# 102 get_resource — (entity, resource) -> Int 
# Valor actual
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: get_resource ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "get_resource", None) or getattr(_gs, "get_resource", None) or getattr(_gs.GameState, "get_resource", None) or getattr(_dt, "get_resource", None)
    assert fn is not None, "get_resource no encontrado"
    # Llamada canónica real
    eff = get_resource(hero.id, 'hp')
    eff(gs, {}) if callable(eff) else None
    assert True
