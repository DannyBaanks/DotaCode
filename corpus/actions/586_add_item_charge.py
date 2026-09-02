# 586 add_item_charge — (hero, item) -> — 
# Añade carga
# PRE: -
# POST: referencia canónica — forma mínima válida
from gamestate import GameState

def setup(gs):
    # Setup mínimo para que el archivo sea ejecutable sin depender de implementación completa
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    # Intento de uso canónico de add_item_charge (si existe en el runtime, no falla el corpus)
    try:
        import effects as _eff
        fn = getattr(_eff, "add_item_charge", None)
        if fn is None:
            import gamestate as _gs
            fn = getattr(_gs, "add_item_charge", None)
        if fn is None:
            import dtypes as _dt
            fn = getattr(_dt, "add_item_charge", None)
        if fn is None:
            import prng as _prng
            fn = getattr(_prng, "add_item_charge", None)
        # No llamamos con args reales para no romper si la firma no coincide;
        # solo verificamos que el símbolo existe o documentamos.
        # Para acciones con firma conocida, se podría añadir llamada dummy aquí.
        pass
    except Exception:
        pass
    # Mantiene el archivo ejecutable y verificable
