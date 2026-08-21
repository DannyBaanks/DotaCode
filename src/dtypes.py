"""Tipos core de DotaCode: Entity, Modifier, Event, EventQueue.

Referencia: SPEC §2 (GameState), ACTIONS.md
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


# ---------------------------------------------------------------------------
# Action types (para gating)
# ---------------------------------------------------------------------------

class ActionType(Enum):
    MOVE = auto()
    CAST = auto()
    ATTACK = auto()
    ITEM_USE = auto()
    CHANNEL = auto()
    SUMMON = auto()


# ---------------------------------------------------------------------------
# Modifier
# ---------------------------------------------------------------------------

class Severity(Enum):
    BASIC = auto()
    STRONG = auto()
    HARD = auto()


@dataclass
class Modifier:
    id: int
    source: int           # EntityId del caster
    target: int           # EntityId del receptor
    type: str
    duration: int         # ticks restantes, -1 = infinito
    max_dur: int          # duración original
    stacks: int = 1
    stacks_max: int | None = None
    gate: set[ActionType] = field(default_factory=set)
    severity: Severity = Severity.BASIC
    undispellable: bool = False
    on_tick: Any = None   # Effect | None
    on_event: Any = None  # Effect | None
    tags: set[str] = field(default_factory=set)

    @property
    def is_expired(self) -> bool:
        return self.duration == 0

    def tick_down(self) -> bool:
        """Decrementa duración. Retorna True si expiró."""
        if self.duration > 0:
            self.duration -= 1
            return self.duration == 0
        return False


# ---------------------------------------------------------------------------
# Event
# ---------------------------------------------------------------------------

@dataclass
class Event:
    id: int
    tick: int
    type: str
    source: int | None = None
    target: int | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    consumed: bool = False


# ---------------------------------------------------------------------------
# EventQueue — heap por (tick, insertion_order)
# ---------------------------------------------------------------------------

class EventQueue:
    """Cola de eventos ordenada por tick, FIFO dentro del mismo tick."""

    def __init__(self):
        self._heap: list[tuple[int, int, Event]] = []
        self._counter = 0  # insertion order

    def push(self, ev: Event):
        heapq.heappush(self._heap, (ev.tick, self._counter, ev))
        self._counter += 1

    def peek(self) -> Event | None:
        if not self._heap:
            return None
        return self._heap[0][2]

    def pop(self) -> Event | None:
        while self._heap:
            _, _, ev = heapq.heappop(self._heap)
            if not ev.consumed:
                return ev
        return None

    def has_pending(self, up_to_tick: int | None = None) -> bool:
        if not self._heap:
            return False
        if up_to_tick is None:
            return True
        return self._heap[0][0] <= up_to_tick

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def __len__(self) -> int:
        return len(self._heap)

    def drain(self, tick: int) -> list[Event]:
        """Extrae todos los eventos con tick <= dado (no consumidos)."""
        result = []
        while self._heap and self._heap[0][0] <= tick:
            _, _, ev = heapq.heappop(self._heap)
            if not ev.consumed:
                result.append(ev)
        return result

    def cancel(self, event_id: int) -> bool:
        """Marca un evento como consumido (no se procesará)."""
        for _, _, ev in self._heap:
            if ev.id == event_id:
                ev.consumed = True
                return True
        return False


# ---------------------------------------------------------------------------
# Entity
# ---------------------------------------------------------------------------

@dataclass
class Entity:
    id: int
    type: str
    state: dict[str, Any] = field(default_factory=dict)
    trigger_ids: list[int] = field(default_factory=list)
    modifier_ids: list[int] = field(default_factory=list)
    position: tuple[int, int] = (0, 0)
    spawn_pos: tuple[int, int] = (0, 0)
    tags: set[str] = field(default_factory=set)
    alive: bool = True
    owner: int | None = None

    def get(self, key: str, default=None):
        return self.state.get(key, default)

    def set(self, key: str, value):
        self.state[key] = value

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags


# ---------------------------------------------------------------------------
# Trigger
# ---------------------------------------------------------------------------

@dataclass
class Trigger:
    id: int
    on: str                    # tipo de evento que escucha
    if_cond: Any = None        # Condition: (σ, ev) → bool
    then: list[Any] = field(default_factory=list)  # [Effect]
    action_type: ActionType | None = None
    source: int = 0            # EntityId dueña
