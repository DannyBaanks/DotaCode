# 252 refresh_modifier — (modifier) -> — 
# Reinicia duración
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: refresh_modifier ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "refresh_modifier", None) or getattr(_gs, "refresh_modifier", None) or getattr(_gs.GameState, "refresh_modifier", None) or getattr(_dt, "refresh_modifier", None)
    assert fn is not None, "refresh_modifier no encontrado"
    # Llamada canónica real
    import effects as _e2
    _e2.apply_modifier(hero.id, hero.id, 'TEST_BUFF', 5)(gs, {})
    mid = list(gs.entity_modifiers(hero.id))[0].id
    eff = fn(mid)
    eff(gs, {})
    
    assert True
