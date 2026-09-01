"""Trigger matching y ejecución.

Referencia: SPEC §5 (Matching de triggers), §6 (Evaluación de condiciones)
"""

from __future__ import annotations

from typing import Any, Callable

try:
    from .gamestate import GameState
    from .dtypes import Event, Trigger, ActionType
except ImportError:
    from gamestate import GameState
    from dtypes import Event, Trigger, ActionType


# Herencia de tipos de evento
_EVENT_HIERARCHY: dict[str, list[str]] = {
    "ON_MELEE_HIT": ["ON_HIT", "ON_DAMAGE"],
    "ON_SPELL_HIT": ["ON_HIT", "ON_DAMAGE"],
    "ON_AUTO_ATTACK": ["ON_ATTACK", "ON_DAMAGE"],
    "ON_CAST_RESOLVED": ["ON_CAST"],
    "ON_KILL": ["ON_DEATH"],
}


def event_parents(event_type: str) -> list[str]:
    """Retorna los padres de un tipo de evento."""
    return _EVENT_HIERARCHY.get(event_type, [])


def match_event(trigger_on: str, event_type: str) -> bool:
    """Aplica el matching exacto, wildcard y de herencia de SPEC §5."""
    if trigger_on == "_" or trigger_on == event_type:
        return True

    pending = list(event_parents(event_type))
    seen: set[str] = set()
    while pending:
        parent = pending.pop()
        if parent in seen:
            continue
        if parent == trigger_on:
            return True
        seen.add(parent)
        pending.extend(event_parents(parent))
    return False


def eval_condition(
    cond: Callable[[GameState, Event], bool] | None,
    gs: GameState,
    ev: Event,
) -> bool:
    """Evalúa condición del trigger. None = siempre True."""
    if cond is None:
        return True
    return cond(gs, ev)


def is_gated(gs: GameState, eid: int, action_type: ActionType | None) -> bool:
    """Verifica si la entity está gated para la acción."""
    if action_type is None:
        return False
    return gs.is_gated(eid, action_type)


def find_matching_triggers(
    gs: GameState,
    ev: Event,
) -> list[tuple[Trigger, Any]]:
    """Encuentra todos los triggers que matchean el evento.

    Retorna [(trigger, entity_owner)] ordenados por relevancia.
    """
    results = []
    for trigger in gs.all_triggers():
        if match_event(trigger.on, ev.type):
            # Verificar que el source del trigger esté vivo
            source_entity = gs.get_entity(trigger.source)
            if source_entity and source_entity.alive:
                # Verificar condición
                if eval_condition(trigger.if_cond, gs, ev):
                    # Verificar gating
                    if not is_gated(gs, trigger.source, trigger.action_type):
                        results.append((trigger, source_entity))
    return results
