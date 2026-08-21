"""GameState — estado global del mundo DotaCode.

Referencia: SPEC §2 (GameState)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

try:
    from .prng import PRNG
    from .dtypes import Entity, Modifier, Event, EventQueue, Trigger
except ImportError:
    from prng import PRNG
    from dtypes import Entity, Modifier, Event, EventQueue, Trigger


@dataclass
class OutputEntry:
    tick: int
    type: str       # OUT_CHAR | OUT_NUMBER | OUT_STATE | OUT_STRING
    value: Any
    entity: int | None = None


@dataclass
class TraceEntry:
    tick: int
    event_id: int
    event_type: str
    source: int | None
    target: int | None
    entity: int
    state_before: dict[str, Any]
    effect: str
    state_after: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)


class GameState:
    """Estado global del mundo DotaCode.

    Contiene todas las entidades, modifiers, eventos, variables,
    y el generador aleatorio determinista.
    """

    def __init__(self, seed: int = 0):
        self.tick: int = 0
        self.entities: dict[int, Entity] = {}
        self.modifiers: dict[int, Modifier] = {}
        self.triggers: dict[int, Trigger] = {}
        self.events: EventQueue = EventQueue()
        self.rng: PRNG = PRNG(seed)
        self.vars: dict[str, Any] = {}
        self.globals: dict[str, Any] = {}
        self.output: list[OutputEntry] = []
        self.seed: int = seed
        self.paused: bool = False
        self.trace: list[TraceEntry] = []
        self._next_entity_id = 1
        self._next_modifier_id = 1
        self._next_trigger_id = 1
        self._next_event_id = 1

    # -----------------------------------------------------------------------
    # ID generation
    # -----------------------------------------------------------------------

    def new_entity_id(self) -> int:
        eid = self._next_entity_id
        self._next_entity_id += 1
        return eid

    def new_modifier_id(self) -> int:
        mid = self._next_modifier_id
        self._next_modifier_id += 1
        return mid

    def new_trigger_id(self) -> int:
        tid = self._next_trigger_id
        self._next_trigger_id += 1
        return tid

    def new_event_id(self) -> int:
        eid = self._next_event_id
        self._next_event_id += 1
        return eid

    # -----------------------------------------------------------------------
    # Entity operations
    # -----------------------------------------------------------------------

    def spawn_entity(
        self,
        type: str,
        state: dict[str, Any] | None = None,
        position: tuple[int, int] = (0, 0),
        tags: set[str] | None = None,
        owner: int | None = None,
    ) -> Entity:
        eid = self.new_entity_id()
        e = Entity(
            id=eid,
            type=type,
            state=state or {},
            position=position,
            spawn_pos=position,
            tags=tags or set(),
            owner=owner,
        )
        self.entities[eid] = e
        return e

    def get_entity(self, eid: int) -> Entity | None:
        return self.entities.get(eid)

    def destroy_entity(self, eid: int) -> bool:
        if eid in self.entities:
            del self.entities[eid]
            return True
        return False

    def alive_entities(self) -> list[Entity]:
        return [e for e in self.entities.values() if e.alive]

    def entities_with_tag(self, tag: str) -> list[Entity]:
        return [e for e in self.entities.values() if e.alive and tag in e.tags]

    # -----------------------------------------------------------------------
    # Modifier operations
    # -----------------------------------------------------------------------

    def add_modifier(self, mod: Modifier) -> Modifier:
        self.modifiers[mod.id] = mod
        entity = self.get_entity(mod.target)
        if entity:
            entity.modifier_ids.append(mod.id)
        return mod

    def remove_modifier(self, mod_id: int) -> bool:
        mod = self.modifiers.get(mod_id)
        if not mod:
            return False
        entity = self.get_entity(mod.target)
        if entity and mod_id in entity.modifier_ids:
            entity.modifier_ids.remove(mod_id)
        del self.modifiers[mod_id]
        return True

    def get_modifier(self, mod_id: int) -> Modifier | None:
        return self.modifiers.get(mod_id)

    def entity_modifiers(self, eid: int) -> list[Modifier]:
        entity = self.get_entity(eid)
        if not entity:
            return []
        return [self.modifiers[mid] for mid in entity.modifier_ids if mid in self.modifiers]

    def has_modifier_type(self, eid: int, mod_type: str) -> bool:
        return any(m.type == mod_type for m in self.entity_modifiers(eid))

    # -----------------------------------------------------------------------
    # Trigger operations
    # -----------------------------------------------------------------------

    def add_trigger(self, trigger: Trigger) -> Trigger:
        self.triggers[trigger.id] = trigger
        entity = self.get_entity(trigger.source)
        if entity:
            entity.trigger_ids.append(trigger.id)
        return trigger

    def remove_trigger(self, tid: int) -> bool:
        if tid in self.triggers:
            trigger = self.triggers[tid]
            entity = self.get_entity(trigger.source)
            if entity and tid in entity.trigger_ids:
                entity.trigger_ids.remove(tid)
            del self.triggers[tid]
            return True
        return False

    def entity_triggers(self, eid: int) -> list[Trigger]:
        entity = self.get_entity(eid)
        if not entity:
            return []
        return [self.triggers[tid] for tid in entity.trigger_ids if tid in self.triggers]

    def all_triggers(self) -> list[Trigger]:
        return list(self.triggers.values())

    # -----------------------------------------------------------------------
    # Gating check
    # -----------------------------------------------------------------------

    def is_gated(self, eid: int, action_type: Any) -> bool:
        """Verifica si una entity tiene un modifier que bloquea la acción."""
        for mod in self.entity_modifiers(eid):
            if action_type in mod.gate:
                return True
        return False

    # -----------------------------------------------------------------------
    # Output
    # -----------------------------------------------------------------------

    def add_output(self, type: str, value: Any, entity: int | None = None):
        self.output.append(OutputEntry(tick=self.tick, type=type, value=value, entity=entity))

    # -----------------------------------------------------------------------
    # Trace
    # -----------------------------------------------------------------------

    def add_trace(
        self,
        event_id: int,
        event_type: str,
        source: int | None,
        target: int | None,
        entity: int,
        state_before: dict[str, Any],
        effect: str,
        state_after: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ):
        self.trace.append(TraceEntry(
            tick=self.tick,
            event_id=event_id,
            event_type=event_type,
            source=source,
            target=target,
            entity=entity,
            state_before=state_before,
            effect=effect,
            state_after=state_after,
            metadata=metadata or {},
        ))

    # -----------------------------------------------------------------------
    # Snapshot (para determinismo / testing)
    # -----------------------------------------------------------------------

    def snapshot(self) -> dict:
        """Captura el estado completo para verificación."""
        return {
            "tick": self.tick,
            "entities": {
                eid: {
                    "type": e.type,
                    "state": dict(e.state),
                    "position": e.position,
                    "alive": e.alive,
                    "tags": set(e.tags),
                }
                for eid, e in self.entities.items()
            },
            "modifiers": {
                mid: {
                    "type": m.type,
                    "target": m.target,
                    "duration": m.duration,
                    "stacks": m.stacks,
                }
                for mid, m in self.modifiers.items()
            },
            "vars": dict(self.vars),
            "globals": dict(self.globals),
        }
