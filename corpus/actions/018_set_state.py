# 018 set_state — (entity, key, value) -> — 
# Asigna valor
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: set_state ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "set_state", None) or getattr(_gs, "set_state", None) or getattr(_gs.GameState, "set_state", None) or getattr(_dt, "set_state", None)
    assert fn is not None, "set_state no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 'hp', 999)
    eff(gs, {})
    
    assert hero.state['hp'] == 999
