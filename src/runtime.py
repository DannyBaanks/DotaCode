"""Runtime principal de DotaCode — run_loop.

Referencia: SPEC §3 (Ciclo de ejecución)
"""

from __future__ import annotations

from typing import Any, Callable

try:
    from .gamestate import GameState
    from .dtypes import Event, Trigger, Modifier, ActionType
    from .triggers import find_matching_triggers, is_gated
    from .effects import remove_modifier, emit, gain, schedule
except ImportError:
    from gamestate import GameState
    from dtypes import Event, Trigger, Modifier, ActionType
    from triggers import find_matching_triggers, is_gated
    from effects import remove_modifier, emit, gain, schedule


# ============================================================================
# Process next event
# ============================================================================

def process_event(gs: GameState, ev: Event) -> GameState:
    """Procesa un evento: matching de triggers → ejecución de effects."""
    if ev.consumed:
        return gs

    # Marcar como procesado
    ev.consumed = True

    # Construir contexto
    ctx: dict[str, Any] = {
        "event_id": ev.id,
        "event_type": ev.type,
        "source": ev.source,
        "target": ev.target,
        "event": ev,
    }

    # 1. Encontrar y ejecutar triggers que matchean
    matches = find_matching_triggers(gs, ev)
    for trigger, owner in matches:
        # Snapshot antes del trigger
        state_before = _entity_snapshot(gs, owner.id)

        # Ejecutar cada effect del trigger
        for effect_fn in trigger.then:
            gs = effect_fn(gs, ctx)

        # Trace
        state_after = _entity_snapshot(gs, owner.id)
        gs.add_trace(
            ev.id, ev.type, ev.source, ev.target,
            owner.id, state_before, f"trigger({trigger.on})", state_after,
        )

    # 2. Procesar scheduled effects (ON_SCHEDULED)
    if ev.type == "ON_SCHEDULED" and "effect" in ev.payload:
        effect_fn = ev.payload["effect"]
        caller_ctx = ev.payload.get("caller_ctx", {})
        ctx.update(caller_ctx)
        state_before = {}
        if ev.target:
            state_before = _entity_snapshot(gs, ev.target)
        gs = effect_fn(gs, ctx)
        if ev.target:
            state_after = _entity_snapshot(gs, ev.target)
            gs.add_trace(
                ev.id, ev.type, ev.source, ev.target,
                ev.target, state_before, "scheduled_effect", state_after,
            )

    # 3. Procesar modifiers on_tick
    for mod in list(gs.modifiers.values()):
        if mod.on_tick and mod.duration != 0:
            target_entity = gs.get_entity(mod.target)
            if target_entity and target_entity.alive:
                ctx_mod = {
                    "event_id": ev.id,
                    "event_type": ev.type,
                    "source": mod.source,
                    "target": mod.target,
                    "modifier": mod,
                }
                gs = mod.on_tick(gs, ctx_mod)

    # 4. Decrementar cooldowns (recursos con sufijo _cooldown)
    for e in gs.alive_entities():
        for key in list(e.state.keys()):
            if key.endswith("_cooldown") and e.state[key] > 0:
                before = e.state[key]
                e.state[key] = max(0, e.state[key] - 1)
                if e.state[key] == 0:
                    emit("ON_COOLDOWN_READY", source=e.id,
                         payload={"ability": key})(gs, ctx)

    # 5. Aplicar regeneración de recursos
    for e in gs.alive_entities():
        for key in list(e.state.keys()):
            if key.endswith("_regen") and e.state[key] > 0:
                resource = key[:-6]  # quitar _regen
                rate = e.state[key]
                if rate > 0:
                    current = e.state.get(resource, 0)
                    max_key = resource + "_max"
                    maximum = e.state.get(max_key, None)
                    if maximum is not None:
                        e.state[resource] = min(current + rate, maximum)
                    else:
                        e.state[resource] = current + rate

    # 6. Decrementar duración de modifiers
    expired = []
    for mod in list(gs.modifiers.values()):
        if mod.duration > 0:
            if mod.tick_down():
                expired.append(mod)
        elif mod.duration == 0 and mod.max_dur > 0:
            expired.append(mod)

    for mod in expired:
        emit("ON_MODIFIER_EXPIRED", source=mod.source, target=mod.target,
             payload={"type": mod.type})(gs, ctx)
        gs.remove_modifier(mod.id)

    return gs


# ============================================================================
# Run loop
# ============================================================================

def run_loop(gs: GameState, max_ticks: int = 10000) -> GameState:
    """Bucle principal de ejecución.

    Procesa eventos tick por tick hasta que no queden más o se alcance max_ticks.
    """
    while not gs.events.is_empty():
        if gs.tick > max_ticks:
            break

        if gs.paused:
            gs.tick += 1
            continue

        # Sacar siguiente evento
        ev = gs.events.pop()
        if ev is None:
            break

        # Si el evento es de un tick futuro, avanzar el reloj
        if ev.tick > gs.tick:
            gs.tick = ev.tick

        # Procesar
        gs = process_event(gs, ev)

    return gs


def run(seed: int, setup_fn: Callable[[GameState], None], max_ticks: int = 10000) -> GameState:
    """Función principal de ejecución.

    1. Crea GameState con seed
    2. Ejecuta setup_fn para configurar handlers y estado inicial
    3. Ejecuta run_loop
    4. Retorna GameState final con trace
    """
    gs = GameState(seed=seed)
    setup_fn(gs)
    gs = run_loop(gs, max_ticks)
    return gs


# ============================================================================
# Helpers
# ============================================================================

def _entity_snapshot(gs: GameState, eid: int) -> dict[str, Any]:
    """Captura estado de una entity para trace."""
    e = gs.get_entity(eid)
    if not e:
        return {}
    return dict(e.state)
