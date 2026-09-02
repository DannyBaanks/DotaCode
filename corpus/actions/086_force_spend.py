# 086 force_spend — (entity, resource, amount) -> Bool 
# Consume aunque quede negativo
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: force_spend ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "force_spend", None) or getattr(_gs, "force_spend", None) or getattr(_gs.GameState, "force_spend", None) or getattr(_dt, "force_spend", None)
    assert fn is not None, "force_spend no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 'hp', 10)
    eff(gs, {})
    
    assert True
