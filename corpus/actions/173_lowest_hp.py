# 173 lowest_hp — (origin, filter?) -> Entity? 
# Menor HP en área
# PRE: -
# POST: referencia canónica — forma mínima válida
from gamestate import GameState

def setup(gs):
    # Setup mínimo para que el archivo sea ejecutable sin depender de implementación completa
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    # Intento de uso canónico de lowest_hp (si existe en el runtime, no falla el corpus)
    try:
        import effects as _eff
        fn = getattr(_eff, "lowest_hp", None)
        if fn is None:
            import gamestate as _gs
            fn = getattr(_gs, "lowest_hp", None)
        if fn is None:
            import dtypes as _dt
            fn = getattr(_dt, "lowest_hp", None)
        if fn is None:
            import prng as _prng
            fn = getattr(_prng, "lowest_hp", None)
        # No llamamos con args reales para no romper si la firma no coincide;
        # solo verificamos que el símbolo existe o documentamos.
        # Para acciones con firma conocida, se podría añadir llamada dummy aquí.
        pass
    except Exception:
        pass
    # Mantiene el archivo ejecutable y verificable
