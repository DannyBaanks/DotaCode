"""Primitivas de Effects — las 10 categorías del runtime.

Cada función toma GameState y retorna GameState (mutado).
Estos son los bloques de construcción de las 744 acciones.

Referencia: SPEC §8 (Primitivas del runtime)
"""

from __future__ import annotations

from typing import Any, Callable

try:
    from .gamestate import GameState
    from .dtypes import Entity, Modifier, Event, Severity, ActionType
except ImportError:
    from gamestate import GameState
    from dtypes import Entity, Modifier, Event, Severity, ActionType


# Type alias
Effect = Callable[[GameState, dict[str, Any]], GameState]


# ============================================================================
# 8.1. ENTITY
# ============================================================================

def spawn(
    type: str,
    state: dict[str, Any] | None = None,
    position: tuple[int, int] = (0, 0),
    tags: set[str] | None = None,
    owner: int | None = None,
) -> Effect:
    """Crea una nueva entity. Retorna EntityId en ctx['result']."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.spawn_entity(type, state, position, tags, owner)
        ctx["result"] = e.id
        return gs
    return _effect


def destroy(eid: int) -> Effect:
    """Destruye una entity, emite ON_DESTROY."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            gs.add_trace(
                ctx.get("event_id", 0), ctx.get("event_type", "?"),
                ctx.get("source"), ctx.get("target"), eid,
                dict(e.state), "destroy", dict(e.state),
            )
            gs.destroy_entity(eid)
            emit("ON_DESTROY", source=eid)(gs, ctx)
        return gs
    return _effect


def set_alive(eid: int, value: bool) -> Effect:
    """Cambia estado alive de una entity."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            before = dict(e.state)
            e.alive = value
            gs.add_trace(
                ctx.get("event_id", 0), ctx.get("event_type", "?"),
                ctx.get("source"), ctx.get("target"), eid,
                before, "set_alive", dict(e.state),
            )
        return gs
    return _effect


def set_owner(eid: int, owner: int | None) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.owner = owner
        return gs
    return _effect


def add_tag(eid: int, tag: str) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.tags.add(tag)
        return gs
    return _effect


def remove_tag(eid: int, tag: str) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.tags.discard(tag)
        return gs
    return _effect


# ============================================================================
# 8.2. STATE
# ============================================================================

def set_state(eid: int, key: str, value: Any) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            before = dict(e.state)
            e.state[key] = value
            gs.add_trace(
                ctx.get("event_id", 0), ctx.get("event_type", "?"),
                ctx.get("source"), ctx.get("target"), eid,
                before, f"set({key})", dict(e.state),
            )
        return gs
    return _effect


def get_state(eid: int, key: str) -> Effect:
    """Lee estado, retorna en ctx['result']."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        ctx["result"] = e.state.get(key) if e else None
        return gs
    return _effect


def inc_state(eid: int, key: str, delta: int = 1) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.state[key] = e.state.get(key, 0) + delta
        return gs
    return _effect


def dec_state(eid: int, key: str, delta: int = 1) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.state[key] = e.state.get(key, 0) - delta
        return gs
    return _effect


def clamp_state(eid: int, key: str, lo: int, hi: int) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e and key in e.state:
            e.state[key] = max(lo, min(hi, e.state[key]))
        return gs
    return _effect


# ============================================================================
# 8.3. RESOURCE
# ============================================================================

def spend(eid: int, resource: str, amount: int) -> Effect:
    """Consume recurso. Retorna True/False en ctx['result']."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            current = e.state.get(resource, 0)
            if current >= amount:
                e.state[resource] = current - amount
                ctx["result"] = True
                gs.add_trace(
                    ctx.get("event_id", 0), ctx.get("event_type", "?"),
                    ctx.get("source"), ctx.get("target"), eid,
                    {resource: current}, f"spend({resource})", {resource: e.state[resource]},
                )
            else:
                ctx["result"] = False
        return gs
    return _effect


def force_spend(eid: int, resource: str, amount: int) -> Effect:
    """Consume aunque quede negativo."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            before = e.state.get(resource, 0)
            e.state[resource] = before - amount
            ctx["result"] = True
        return gs
    return _effect


def gain(eid: int, resource: str, amount: int) -> Effect:
    """Añade recurso (respeta max si existe)."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            current = e.state.get(resource, 0)
            max_key = resource + "_max"
            maximum = e.state.get(max_key, None)
            if maximum is not None:
                e.state[resource] = min(current + amount, maximum)
            else:
                e.state[resource] = current + amount
            gs.add_trace(
                ctx.get("event_id", 0), ctx.get("event_type", "?"),
                ctx.get("source"), ctx.get("target"), eid,
                {resource: current}, f"gain({resource})", {resource: e.state[resource]},
            )
        return gs
    return _effect


def force_gain(eid: int, resource: str, amount: int) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.state[resource] = e.state.get(resource, 0) + amount
        return gs
    return _effect


def set_resource(eid: int, resource: str, value: int) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.state[resource] = value
        return gs
    return _effect


def get_resource(eid: int, resource: str) -> Effect:
    """Lee recurso, retorna en ctx['result']."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        ctx["result"] = e.state.get(resource, 0) if e else 0
        return gs
    return _effect


# ============================================================================
# 8.4. TIME
# ============================================================================

def schedule(effect: Effect, tick_offset: int) -> Effect:
    """Programa un efecto en tick futuro."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        eid = gs.new_event_id()
        ev = Event(
            id=eid,
            tick=gs.tick + tick_offset,
            type="ON_SCHEDULED",
            source=ctx.get("source"),
            target=ctx.get("target"),
            payload={"effect": effect, "caller_ctx": dict(ctx)},
        )
        gs.events.push(ev)
        return gs
    return _effect


def cancel_event(event_id: int) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        gs.events.cancel(event_id)
        return gs
    return _effect


def periodic(effect: Effect, every: int = 1, times: int | None = None) -> Effect:
    """Repite efecto cada N ticks. times=None = infinito."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        remaining = [times] if times is not None else [None]

        def _periodic_tick(gs_inner: GameState, ctx_inner: dict) -> GameState:
            gs_inner = effect(gs_inner, ctx_inner)
            if remaining[0] is not None:
                remaining[0] -= 1
                if remaining[0] <= 0:
                    return gs_inner
            schedule(_periodic_tick, every)(gs_inner, ctx_inner)
            return gs_inner

        schedule(_periodic_tick, every)(gs, ctx)
        return gs
    return _effect


# ============================================================================
# 8.5. EVENT
# ============================================================================

def emit(
    event_type: str,
    source: int | None = None,
    target: int | None = None,
    payload: dict[str, Any] | None = None,
    tick_offset: int = 0,
) -> Effect:
    """Emite un evento (mismo tick o futuro)."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        eid = gs.new_event_id()
        ev = Event(
            id=eid,
            tick=gs.tick + tick_offset,
            type=event_type,
            source=source if source is not None else ctx.get("source"),
            target=target if target is not None else ctx.get("target"),
            payload=payload or {},
        )
        gs.events.push(ev)
        return gs
    return _effect


def emit_delayed(event_type: str, delay: int, **kwargs) -> Effect:
    return emit(event_type, tick_offset=delay, **kwargs)


def broadcast(event_type: str, source: int | None = None, payload: dict | None = None) -> Effect:
    """Emite a todas las entities vivas."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        for e in gs.alive_entities():
            emit(event_type, source=source, target=e.id, payload=payload)(gs, ctx)
        return gs
    return _effect


def consume_event(ev: Event) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        ev.consumed = True
        return gs
    return _effect


# ============================================================================
# 8.6. MODIFIER
# ============================================================================

def apply_modifier(
    source: int,
    target: int,
    mod_type: str,
    duration: int,
    stacks: int = 1,
    gate: set[ActionType] | None = None,
    severity: Severity = Severity.BASIC,
    undispellable: bool = False,
    tags: set[str] | None = None,
    on_tick: Effect | None = None,
    on_event: Effect | None = None,
) -> Effect:
    """Aplica un buff/debuff a una entity."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        mod_id = gs.new_modifier_id()
        mod = Modifier(
            id=mod_id,
            source=source,
            target=target,
            type=mod_type,
            duration=duration,
            max_dur=duration,
            stacks=stacks,
            gate=gate or set(),
            severity=severity,
            undispellable=undispellable,
            on_tick=on_tick,
            on_event=on_event,
            tags=tags or set(),
        )
        gs.add_modifier(mod)
        emit("ON_MODIFIER_APPLIED", source=source, target=target,
             payload={"modifier_id": mod_id, "type": mod_type})(gs, ctx)
        return gs
    return _effect


def remove_modifier(mod_id: int) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        mod = gs.get_modifier(mod_id)
        if mod:
            emit("ON_MODIFIER_REMOVED", source=mod.source, target=mod.target,
                 payload={"modifier_id": mod_id, "type": mod.type})(gs, ctx)
            gs.remove_modifier(mod_id)
        return gs
    return _effect


def remove_modifier_type(eid: int, mod_type: str) -> Effect:
    """Remueve todos los modifiers de un tipo de una entity."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        to_remove = [m.id for m in gs.entity_modifiers(eid) if m.type == mod_type]
        for mid in to_remove:
            remove_modifier(mid)(gs, ctx)
        return gs
    return _effect


def refresh_modifier(mod_id: int) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        mod = gs.get_modifier(mod_id)
        if mod:
            mod.duration = mod.max_dur
        return gs
    return _effect


def add_stack(mod_id: int, amount: int = 1) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        mod = gs.get_modifier(mod_id)
        if mod:
            if mod.stacks_max is not None:
                mod.stacks = min(mod.stacks + amount, mod.stacks_max)
            else:
                mod.stacks += amount
        return gs
    return _effect


# ============================================================================
# 8.7. GATING
# ============================================================================

def gate(eid: int, action_types: set[ActionType], duration: int) -> Effect:
    """Bloquea categorías de acción por tiempo."""
    return apply_modifier(
        source=eid, target=eid, mod_type="GATE",
        duration=duration, gate=action_types,
        tags={"debuff"},
    )


def ungated(eid: int, action_type: ActionType) -> Effect:
    """Desbloquea una categoría removiendo el modifier de gate."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        for mod in gs.entity_modifiers(eid):
            if mod.type == "GATE" and action_type in mod.gate:
                mod.gate.discard(action_type)
                if not mod.gate:
                    gs.remove_modifier(mod.id)
        return gs
    return _effect


# ============================================================================
# 8.8. POSICIÓN
# ============================================================================

def set_pos(eid: int, x: int, y: int) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.position = (x, y)
        return gs
    return _effect


def move_to(eid: int, x: int, y: int) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.position = (x, y)
            emit("ON_MOVE", source=eid, payload={"x": x, "y": y})(gs, ctx)
        return gs
    return _effect


def teleport(eid: int, x: int, y: int) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        e = gs.get_entity(eid)
        if e:
            e.position = (x, y)
            emit("ON_TELEPORT", source=eid, payload={"x": x, "y": y})(gs, ctx)
        return gs
    return _effect


def distance(eid_a: int, eid_b: int) -> Effect:
    """Calcula Manhattan distance, retorna en ctx['result']."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        a = gs.get_entity(eid_a)
        b = gs.get_entity(eid_b)
        if a and b:
            ctx["result"] = abs(a.position[0] - b.position[0]) + abs(a.position[1] - b.position[1])
        else:
            ctx["result"] = 999999
        return gs
    return _effect


def in_range(source_eid: int, target_eid: int, rng: int) -> Effect:
    """Verifica si target está en rango de source. Retorna bool en ctx['result']."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        s = gs.get_entity(source_eid)
        t = gs.get_entity(target_eid)
        if s and t:
            dist = abs(s.position[0] - t.position[0]) + abs(s.position[1] - t.position[1])
            ctx["result"] = dist <= rng
        else:
            ctx["result"] = False
        return gs
    return _effect


# ============================================================================
# 8.9. I/O
# ============================================================================

def output(value: Any, type: str = "OUT_VALUE") -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        gs.add_output(type, value, ctx.get("target"))
        return gs
    return _effect


def output_char(char_code: int) -> Effect:
    return output(chr(char_code), "OUT_CHAR")


def output_string(s: str) -> Effect:
    return output(s, "OUT_STRING")


def output_number(n: int | float) -> Effect:
    return output(n, "OUT_NUMBER")


def output_newline() -> Effect:
    return output("\n", "OUT_CHAR")


# ============================================================================
# 8.10. VARIABLES
# ============================================================================

def set_var(name: str, value: Any) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        gs.vars[name] = value
        return gs
    return _effect


def get_var(name: str) -> Effect:
    """Lee variable, retorna en ctx['result']."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        ctx["result"] = gs.vars.get(name)
        return gs
    return _effect


def inc_var(name: str, delta: int = 1) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        gs.vars[name] = gs.vars.get(name, 0) + delta
        return gs
    return _effect


def dec_var(name: str, delta: int = 1) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        gs.vars[name] = gs.vars.get(name, 0) - delta
        return gs
    return _effect


def del_var(name: str) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        gs.vars.pop(name, None)
        return gs
    return _effect


def global_set(name: str, value: Any) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        gs.globals[name] = value
        return gs
    return _effect


def global_get(name: str) -> Effect:
    """Lee variable global, retorna en ctx['result']."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        ctx["result"] = gs.globals.get(name)
        return gs
    return _effect


def global_inc(name: str, delta: int = 1) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        gs.globals[name] = gs.globals.get(name, 0) + delta
        return gs
    return _effect


def global_dec(name: str, delta: int = 1) -> Effect:
    def _effect(gs: GameState, ctx: dict) -> GameState:
        gs.globals[name] = gs.globals.get(name, 0) - delta
        return gs
    return _effect


# ============================================================================
# COMPOSICIÓN
# ============================================================================

def seq(*effects: Effect) -> Effect:
    """Ejecuta effects en secuencia."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        for fx in effects:
            gs = fx(gs, ctx)
        return gs
    return _effect


def branch(condition: Callable[[GameState, dict], bool], then: Effect, else_: Effect | None = None) -> Effect:
    """If/else sobre effects."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        if condition(gs, ctx):
            gs = then(gs, ctx)
        elif else_:
            gs = else_(gs, ctx)
        return gs
    return _effect


def each_entity(filter_fn: Callable[[Entity], bool], effect: Effect) -> Effect:
    """Aplica effect a cada entity que cumple filtro."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        for e in gs.alive_entities():
            if filter_fn(e):
                ctx["target"] = e.id
                gs = effect(gs, ctx)
        return gs
    return _effect


def each_modifier(eid: int, mod_type: str, effect: Effect) -> Effect:
    """Aplica effect a cada modifier de un tipo en una entity."""
    def _effect(gs: GameState, ctx: dict) -> GameState:
        for mod in gs.entity_modifiers(eid):
            if mod.type == mod_type:
                ctx["modifier"] = mod
                gs = effect(gs, ctx)
        return gs
    return _effect
