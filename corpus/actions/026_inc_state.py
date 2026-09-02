# 026 inc_state — (entity, key, delta?) -> — 
# Incrementa (delta=1 por defecto)
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: inc_state ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "inc_state", None) or getattr(_gs, "inc_state", None) or getattr(_gs.GameState, "inc_state", None) or getattr(_dt, "inc_state", None)
    assert fn is not None, "inc_state no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 'hp', 1)
    before = hero.state['hp']
    eff(gs, {})
    
    assert hero.state['hp'] == before + 1, f"inc_state POST hp 100->101, got {hero.state['hp']}"
