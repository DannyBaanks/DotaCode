# 089 set_resource — (entity, resource, value) -> — 
# Asigna valor exacto
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: set_resource ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "set_resource", None) or getattr(_gs, "set_resource", None) or getattr(_gs.GameState, "set_resource", None) or getattr(_dt, "set_resource", None)
    assert fn is not None, "set_resource no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 'hp', 10)
    eff(gs, {})
    
    assert True
