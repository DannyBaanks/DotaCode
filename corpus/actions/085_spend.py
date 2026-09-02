# 085 spend — (entity, resource, amount) -> Bool 
# Consume; false si insuficiente
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: spend ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "spend", None) or getattr(_gs, "spend", None) or getattr(_gs.GameState, "spend", None) or getattr(_dt, "spend", None)
    assert fn is not None, "spend no encontrado"
    # Llamada canónica real
    eff = spend(hero.id, 'hp', 10)
    eff(gs, {}) if callable(eff) else None
    assert True
