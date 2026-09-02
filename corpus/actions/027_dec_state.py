# 027 dec_state — (entity, key, delta?) -> — 
# Decrementa
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: dec_state ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "dec_state", None) or getattr(_gs, "dec_state", None) or getattr(_gs.GameState, "dec_state", None) or getattr(_dt, "dec_state", None)
    assert fn is not None, "dec_state no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 'hp', 1)
    before = hero.state['hp']
    eff(gs, {})
    
    assert hero.state['hp'] == before - 1
