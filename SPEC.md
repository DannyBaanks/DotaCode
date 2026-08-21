# DotaCode — SPECIFICACIÓN

Especificación formal del runtime DotaCode.

Basado en MODEL_DISCOVERY.md (7 primitivas) y ACTIONS.md (744 acciones).

Semántica operacional **small-step**: cada transición lleva un GameState a otro.

---

## 1. Convenciones

- `σ` = GameState (estado del mundo)
- `e` = Entity
- `v` = Event
- `φ` = Effect
- `τ` = Trigger
- `μ` = Modifier
- `ω` = Tick (tiempo)
- `→` = transición de un paso
- `⇒` = transición completa (hasta estado estable)
- `∅` = vacío / nulo
- `¬` = negación lógica
- `∧` = conjunción
- `∨` = disyunción
- `∈` = pertenece a
- `∀` = para todo
- `∃` = existe

Dominios:
- `EntityId` = Nat (enteros naturales únicos)
- `ResourceId` = Symbol (hp | mana | gold | stacks:id | charges:id | cooldown:id)
- `ModifierId` = Nat
- `EventId` = Nat
- `Tick` = Nat
- `Pos` = (Int, Int)
- `Value` = Int | Float | Bool | Pos | String | List | Map | Null

---

## 2. GameState

El estado global del mundo en cualquier momento:

```
σ = {
    tick:        Tick
  , entities:    { EntityId → Entity }
  , events:      EventQueue                    # cola ordenada
  , rng:         PRNG                          # generador sembrado
  , vars:        { Symbol → Value }            # variables del programa
  , globals:     { Symbol → Value }            # variables globales
  , output:      [OutputEntry]                 # salida acumulada
  , seed:        Nat                           # semilla para reproducibilidad
  , paused:      Bool                          # pausa global
}
```

### Entity

```
Entity = {
    id:         EntityId
  , type:       Symbol
  , state:      { Symbol → Value }             # mutable
  , triggers:   [Trigger]
  , modifiers:  [ModifierId]                   # ids de modifiers activos
  , position:   Pos
  , spawn_pos:  Pos
  , tags:       { Symbol }
  , alive:      Bool
  , owner:      EntityId | Null
}
```

### Modifier

```
Modifier = {
    id:         ModifierId
  , source:     EntityId
  , target:     EntityId
  , type:       Symbol
  , duration:   Int                            # ticks restantes, -1 = infinito
  , max_dur:    Int                            # duración original (para refresh)
  , stacks:     Nat
  , stacks_max: Nat | Null
  , gate:       { ActionType }                 # acciones bloqueadas
  , severity:   basic | strong | hard
  , undispellable: Bool
  , on_tick:    Effect | Null                  # se ejecuta cada tick del modifier
  , on_event:   Effect | Null                  # se ejecuta ante eventos
  , tags:       { Symbol }                     # buff | debuff | ...
}
```

### Event

```
Event = {
    id:         EventId
  , tick:       Tick                           # tick en que se procesa
  , type:       Symbol                         # ON_CAST, ON_DAMAGE, etc.
  , source:     EntityId | Null
  , target:     EntityId | Null
  , payload:    { Symbol → Value }             # datos adicionales
  , consumed:   Bool                           # ya fue procesado
}
```

### EventQueue

```
EventQueue = [Event]                           # ordenada por (tick, insertion_order)
```

Regla: eventos con menor tick primero. Dentro del mismo tick, FIFO por orden de inserción.

### Trigger

```
Trigger = {
    id:        Symbol
  , on:        Symbol                          # tipo de evento que escucha
  , if:        Condition                       # predicado sobre σ + evento
  , then:      [Effect]                        # efectos a ejecutar
  , action_type: ActionType | Null             # categoría de acción (para gating)
  , source:    EntityId                        # entity dueña del trigger
}
```

### Effect

Un Effect es una función parcial:

```
Effect : GameState × Context → GameState
```

Donde `Context` contiene la entity, el evento que disparó, y datos auxiliares.

Un Effect puede:
1. Mutar `σ` directamente (set_state, gain, spend, etc.)
2. Encolar eventos nuevos (emit)
3. Programar efectos futuros (schedule)
4. Retornar un valor (en expresiones)

### Condition

```
Condition : GameState × Event → Bool
```

Evalúa sobre el estado actual y el evento que activó el trigger.

### ActionType

```
ActionType = { move, cast, attack, item_use, channel, summon, ... }
```

Usado por el sistema de gating (CONTROL §10 de ACTIONS.md).

### PRNG

```
PRNG = Nat → (Value, Nat)                      # función pura sembrada
```

Dada una semilla, retorna (valor, nueva_semilla). Reproducible.

---

## 3. Ciclo de ejecución

El runtime ejecuta un bucle que avanza ticks y procesa eventos.

### 3.1. Función principal `run`

```
run : (seed, program, initial_state, inputs?) → Trace

run(seed, program, σ₀, inputs?) =
    σ₁ = inject_inputs(σ₀, inputs?)
    σ₂ = inject_program_handlers(σ₁, program)
    run_loop(σ₂)
```

### 3.2. Bucle principal `run_loop`

```
run_loop(σ) =
    if σ.events.vacía AND σ.paused = false:
        return σ                              # estado estable, fin
    if σ.paused:
        σ' = advance(σ)                       # avanza tick sin procesar
        return run_loop(σ')
    σ' = process_next_event(σ)                # saca y procesa siguiente evento
    run_loop(σ')
```

### 3.3. Procesamiento de eventos `process_next_event`

```
process_next_event(σ) =
    (ev, σ') = dequeue(σ.events, σ.tick)

    # 1. Marcar como procesado
    σ' = record_event(σ', ev)

    # 2. Para cada trigger que matchee el evento:
    for τ in all_triggers(σ'):
        if matches(τ.on, ev) AND eval(τ.if, σ', ev):
            if τ.source.alive AND not is_gated(τ.source, τ.action_type, σ'):
                σ' = run_effects(τ.then, σ', ev)
            else:
                σ' = emit(σ', ON_ACTION_BLOCKED, τ.source, ev)

    # 3. Procesar modifiers periódicos (on_tick)
    for μ in active_modifiers(σ'):
        if μ.on_tick ≠ Null AND μ.duration ≠ 0:
            σ' = run_effect(μ.on_tick, σ', μ.context)
            σ' = tick_modifier(μ, σ')

    # 4. Decrementar cooldowns
    for (e, ability) in active_cooldowns(σ'):
        σ' = decrement_cooldown(e, ability, σ')

    # 5. Aplicar regeneración de recursos
    for e in alive_entities(σ'):
        for (res, rate) in regen_rates(e):
            σ' = gain(e, res, rate, σ')

    # 6. Avanzar tiempo de modifiers
    for μ in active_modifiers(σ'):
        σ' = tick_modifier(μ, σ')

    return σ'
```

### 3.4. Decremento de tiempo `tick_modifier`

```
tick_modifier(μ, σ) =
    if μ.duration > 0:
        μ.duration = μ.duration - 1
        if μ.duration = 0:
            σ = remove_modifier(μ, σ)
            σ = emit(σ, ON_MODIFIER_EXPIRED, μ.target, μ)
    return σ
```

---

## 4. Dequeue — selección del siguiente evento

```
dequeue(queue, current_tick) =
    # Preferencia: eventos del tick actual primero
    for ev in queue:
        if ev.tick <= current_tick AND ev.consumed = false:
            remove ev from queue
            return (ev, σ)

    # Si no hay eventos pendientes de este tick, avanzar
    σ.tick = σ.tick + 1
    return dequeue(queue, σ.tick)
```

Dentro del mismo tick: **FIFO por orden de inserción** (determinismo).

---

## 5. Matching de triggers

```
matches(τ.on, ev) =
    τ.on = ev.type                               # match exacto
    OR τ.on = _                                  # wildcard (cualquier tipo)
    OR τ.on ∈ ev.type_parents(ev.type)           # herencia de tipos
```

Herencia de tipos de evento (ejemplo):
```
ON_MELEE_HIT → ON_HIT → ON_DAMAGE
ON_SPELL_HIT → ON_HIT → ON_DAMAGE
ON_AUTO_ATTACK → ON_ATTACK → ON_DAMAGE
```

Definida como parte del programa. Si no hay herencia, solo match exacto.

---

## 6. Evaluación de condiciones

```
eval(cond, σ, ev) → Bool
```

Las condiciones son expresiones sobre el estado y el evento. Ejemplos:

```
eval(resource ≥ cost, σ, ev)
    → σ.entities[ev.source].state.mana ≥ 30

eval(hp ≤ 0, σ, ev)
    → σ.entities[ev.target].state.hp ≤ 0

eval(in_range(σ, ev.source, ev.target, r), σ, ev)
    → distance(get_pos(σ, ev.source), get_pos(σ, ev.target)) ≤ r
```

Las condiciones son **puras**: no mutan σ, solo lo leen.

---

## 7. Ejecución de effects

```
run_effects([φ₁, φ₂, ..., φₙ], σ, ev) =
    σ' = σ
    for φ in [φ₁, ..., φₙ]:
        σ' = run_effect(φ, σ', ev)
    return σ'
```

```
run_effect(φ, σ, ev) → σ'
```

Cada Effect tiene una semántica definida. La función `run_effect` casea sobre el
tipo de Effect y aplica la mutación correspondiente.

---

## 8. Primitivas del runtime — efectos elementales

Estos son los efectos que el runtime implementa directamente.
Todas las 744 acciones de ACTIONS.md se construyen como composiciones de estos.

### 8.1. Entity

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `spawn(type, state, pos, tags)` | Crear entity | σ.entities[id] = Entity{nuevoid, ...} |
| `destroy(e)` | Destruir entity | emit(ON_DESTROY); remove σ.entities[e] |
| `set_alive(e, b)` | Cambiar vivo/muerto | e.alive = b |
| `set_owner(e, owner)` | Cambiar dueño | e.owner = owner |
| `add_tag(e, tag)` | Añadir tag | e.tags = e.tags ∪ {tag} |
| `remove_tag(e, tag)` | Quitar tag | e.tags = e.tags \ {tag} |

### 8.2. State

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `set(e, k, v)` | Asignar | e.state[k] = v |
| `inc(e, k, δ)` | Incrementar | e.state[k] = e.state[k] + δ |
| `dec(e, k, δ)` | Decrementar | e.state[k] = e.state[k] - δ |
| `mul(e, k, f)` | Multiplicar | e.state[k] = e.state[k] × f |
| `clamp(e, k, lo, hi)` | Limitar | e.state[k] = clamp(e.state[k], lo, hi) |
| `clear(e, k)` | Borrar | remove e.state[k] |
| `get(e, k)` → v | Leer | return e.state[k] |

### 8.3. Resource

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `spend(e, r, x)` → b | Consume si ≥ | if e.state[r] ≥ x: e.state[r] -= x; return True else: return False |
| `force_spend(e, r, x)` → b | Consume siempre | e.state[r] -= x; return True |
| `gain(e, r, x)` | Añade (respeta max) | e.state[r] = min(e.state[r]+x, e.state.get(r+'_max', ∞)) |
| `force_gain(e, r, x)` | Añade sin max | e.state[r] = e.state[r] + x |
| `set_resource(e, r, v)` | Fija | e.state[r] = v |
| `spend_pct(e, r, p)` → b | Porcentaje del actual | spend(e, r, e.state[r] × p) |
| `gain_pct(e, r, p)` | % del max | gain(e, r, e.state[r+'_max'] × p) |

### 8.4. Time

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `schedule(φ, tick)` | Programar futuro | enqueue(Event{tick, ON_SCHEDULE, φ}) |
| `cancel(id)` | Cancelar | mark consumed en events[id] |
| `periodic(φ, every, n?)` | Repetir | schedule(φ); en φ: if n>0: schedule(self, now+every) |

### 8.5. Event

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `emit(type, src, tgt, payload)` | Crear evento | enqueue(Event{tick_now, type, src, tgt, payload}) |
| `emit_delayed(type, d, ...)` | Futuro | enqueue(Event{tick_now+d, ...}) |
| `forward(ev, new_tgt)` | Redirigir | ev.target = new_tgt; enqueue(ev) |
| `broadcast(type, src, payload)` | Todos | for e in alive: emit(type, src, e, payload) |
| `block(type, e?)` | Bloquear | add to σ.blocked_events |
| `consume(ev)` | Marcar | ev.consumed = True |

### 8.6. Modifier

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `apply(src, tgt, type, dur, stacks, gate, ...)` | Crear | σ.modifiers[id] = Modifier{...}; add id a tgt.modifiers |
| `remove(μ)` | Destruir | remove de target.modifiers; remove de σ.modifiers |
| `refresh(μ)` | Reiniciar duración | μ.duration = μ.max_dur |
| `extend(μ, x)` | Extender | μ.duration += x |
| `reduce(μ, x)` | Reducir | μ.duration = max(0, μ.duration - x) |
| `add_stack(μ, n?)` | Apilar | μ.stacks += n (default 1) |
| `transfer(μ, new_tgt)` | Mover | remove de viejo target; add al nuevo |

### 8.7. Gating

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `is_gated(e, action, σ)` → b | Verificar | ∀μ ∈ e.modifiers: action ∈ μ.gate → return True |
| `gate(e, actions, dur)` | Bloquear | apply modifier con gate=actions |
| `ungated(e, action)` | Desbloquear | remove gate para action de modifiers activos |

### 8.8. Posición

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `set_pos(e, x, y)` | Asignar | e.position = (x, y) |
| `move_to(e, x, y)` | Mover instantáneo | e.position = (x, y); emit(ON_MOVE) |
| `move_by(e, dx, dy)` | Desplazar | e.position = (e.x+dx, e.y+dy) |
| `teleport(e, x, y)` | Instantáneo | e.position = (x, y); emit(ON_TELEPORT) |
| `distance(a, b)` → n | Consulta | return |a.pos - b.pos| |
| `in_range(a, b, r)` → b | Consulta | return distance(a,b) ≤ r |

### 8.9. I/O

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `output(v)` | Escribir | σ.output.append(v) |
| `input_wait()` → v | Leer | v = σ.inputs[0]; remove σ.inputs[0] |

### 8.10. Variables

| Efecto | Descripción | Semántica |
|--------|-------------|-----------|
| `set_var(k, v)` | Asignar | σ.vars[k] = v |
| `get_var(k)` → v | Leer | return σ.vars[k] |
| `inc_var(k, δ)` | Incrementar | σ.vars[k] += δ |
| `del_var(k)` | Borrar | remove σ.vars[k] |
| `global_set(k, v)` | Global | σ.globals[k] = v |
| `global_get(k)` → v | Global | return σ.globals[k] |

---

## 9. Composición de acciones sobre primitivas

Cada una de las 744 acciones de ACTIONS.md se descompone en primitivas.
Aquí se muestran las descomposiciones de mayor complejidad:

### 9.1. STUN

```
stun(target, dur) =
    apply_modifier(
        source = ev.source
      , target = target
      , type = STUN
      , duration = dur
      , gate = {move, cast, attack, item_use, channel}
      , severity = basic
      , tags = {debuff}
      , on_tick = Null
      , on_event = Null
    )
```

### 9.2. DAMAGE

```
damage(target, raw, type?) =
    amt = raw
    # Aplicar mitigación
    for μ in target.modifiers:
        if μ.type = ARMOR AND type = PHYSICAL:
            amt = amt × (1 - μ.stacks × 0.05)    # ejemplo: 5% por armor
        if μ.type = MAGIC_RESIST AND type = MAGIC:
            amt = amt × (1 - μ.stacks × 0.01)    # 1% por punto
        if μ.type = DAMAGE_REDUCTION:
            amt = amt × (1 - μ.stacks × 0.01)
    # Aplicar amplificación
    for μ in target.modifiers:
        if μ.type = AMPLIFY_DAMAGE:
            amt = amt × (1 + μ.stacks × 0.01)
    # Aplicar daño
    before = target.state.hp
    target.state.hp = max(0, target.state.hp - amt)
    emit(ON_DAMAGE, ev.source, target, {amount: amt, type: type})
    emit(ON_RESOURCE_CHANGE, target, hp, before, target.state.hp)
    # Lifesteal
    for μ in ev.source.modifiers:
        if μ.type = LIFESTEAL:
            heal(ev.source, amt × μ.stacks × 0.01)
    # Verificar muerte
    if target.state.hp ≤ 0 AND target.alive:
        trigger_death(target, ev.source)
    return amt
```

### 9.3. HEAL

```
heal(target, amount) =
    before = target.state.hp
    max = target.state.get(hp_max, target.state.hp)
    target.state.hp = min(target.state.hp + amount, max)
    emit(ON_HEAL, ev.source, target, {amount: target.state.hp - before})
    emit(ON_RESOURCE_CHANGE, target, hp, before, target.state.hp)
    return target.state.hp - before
```

### 9.4. KILL → DEATH → RESPAWN

```
kill(target, source?) =
    if NOT target.alive: return
    before = target.state.hp
    target.state.hp = 0
    target.alive = False
    emit(ON_DAMAGE, source, target, {amount: before, lethal: True})
    emit(ON_DEATH, source, target, {cause: ev.type})
    emit(ON_RESOURCE_CHANGE, target, hp, before, 0)
    # Remover modifiers que se remueven en muerte
    for μ in target.modifiers:
        if μ.tags ∩ {death_purge} ≠ ∅:
            remove(μ)
    # Programar respawn
    delay = target.state.get(respawn_time, 5)
    schedule(respawn_effect(target), at = σ.tick + delay)

respawn_effect(target) =
    φ = [
        set_alive(target, True)
      , set(target, hp, target.state.get(hp_max, 100))
      , set(target, mana, target.state.get(mana_max, 100))
      , teleport(target, target.spawn_pos.x, target.spawn_pos.y)
      , emit(ON_SPAWN, target, Null, {})
    ]
```

### 9.5. CAST pipeline

```
cast(ability, source, target?) =
    # 1. Verificar condiciones
    if is_gated(source, CAST): return
    if has_modifier(source, SILENCE): return
    if cooldown_remaining(source, ability) > 0: return
    if source.state.mana < ability.cost: return

    # 2. Consumir recursos
    spend(source, MANA, ability.cost)

    # 3. Iniciar cooldown
    start_cooldown(source, ability, ability.cooldown)

    # 4. Emitir evento de casteo
    emit(ON_CAST, source, target, {ability: ability.id})

    # 5. Ejecutar efectos de la habilidad
    run_effects(ability.effects, σ, ev)

    # 6. Si tiene canal
    if ability.channel_dur > 0:
        apply_modifier(source, source, CHANNELING, ability.channel_dur,
            gate = {cast, move, attack})
        periodic(ability.channel_tick, every = 1, times = ability.channel_dur)
```

### 9.6. PROJECTILE

```
spawn_projectile(source, target, speed, payload) =
    proj = spawn(
        type = PROJECTILE
      , state = {target: target.id, speed: speed, payload: payload}
      , pos = source.position
      , tags = {projectile}
    )
    # Movimiento periódico
    periodic(
        φ = move_toward(proj, target.pos, speed)
           ; if distance(proj, target) ≤ speed:
                run_effects(proj.state.payload, σ, {target: target})
                emit(ON_HIT, proj, target, {})
                destroy(proj)
           else:
                schedule(self, now + 1)
      , every = 1
    )
```

### 9.7. AURA

```
create_aura(source, type, radius, effect) =
    aura_mod = apply_modifier(source, source, type + _AURA, -1,
        gate = ∅, tags = {aura, undispellable})
    periodic(
        φ = for e in alive_entities(σ):
                if e ≠ source AND distance(source, e) ≤ radius:
                    if NOT has_modifier(e, type):
                        apply_modifier(source, e, type, 1, gate = ...)
                    # Refrescar duración
                    for μ in e.modifiers:
                        if μ.type = type AND μ.source = source.id:
                            μ.duration = μ.max_dur
                else:
                    # Fuera de aura: remover
                    for μ in e.modifiers:
                        if μ.type = type AND μ.source = source.id:
                            remove(μ)
      , every = 1
    )
```

### 9.8. DISPEL

```
dispel_basic(target) =
    for μ in target.modifiers:
        if μ.severity = basic AND μ.undispellable = False:
            remove(μ)
            emit(ON_MODIFIER_REMOVED, target, μ, {cause: dispel})

dispel_strong(target) =
    for μ in target.modifiers:
        if μ.severity ∈ {basic, strong} AND μ.undispellable = False:
            remove(μ)

dispel_hard(target) =
    for μ in target.modifiers:
        if μ.undispellable = False:
            remove(μ)
```

### 9.9. COMBO de habilidades

```
# Ejemplo: chain_stun(source, target, ability_a, ability_b)
cast(ability_a, source, target)        # primer stun
wait(ability_a.channel_dur)            # esperar
cast(ability_b, source, target)        # segundo stun
# El primero aplica STUN(target, dur_a)
# El segundo aplica STUN(target, dur_b) encima
# Ambos modifiers coexisten en target.modifiers
# Al expirar el primero, STUN sigue activo por el segundo
```

### 9.10. SIMULACIÓN completa (ejemplo)

```
# Kill counter
global_set(kills_a, 0)
global_set(kills_b, 0)

on(ON_DEATH, φ =
    if ev.source.tags ∩ {hero} ≠ ∅:
        if ev.target.tags ∩ {hero} ≠ ∅:
            if ev.source.owner ≠ ev.target.owner:
                global_inc(kills_a) if ev.source.owner = team_a
                global_inc(kills_b) if ev.source.owner = team_b
    emit(ON_KILL_COUNTED, ev.source, ev.target,
        {total_a: global_get(kills_a), total_b: global_get(kills_b)})
)
```

---

## 10. Determinismo

**Teorema (propuesto):** Para cualquier `(seed, program, σ₀)` fijos, `run` produce
exactamente el mismo `Trace`.

**Condiciones necesarias:**
1. El PRNG es función pura: `PRNG(seed)` siempre retorna el mismo valor.
2. La cola de eventos procesa FIFO dentro del mismo tick.
3. No existe acceso a tiempo externo, red, ni I/O no determinista.
4. Las condiciones son puras (no mutan σ).
5. Los efectos se ejecutan en orden secuencial dentro de un trigger.

**Evidencia:** pendiente de verificación con tests.

---

## 11. Trace

El trace registra cada transición:

```
TraceEntry = {
    tick:        Tick
  , event_id:    EventId
  , event_type:  Symbol
  , source:      EntityId | Null
  , target:      EntityId | Null
  , entity:      EntityId                    # entity más afectada
  , state_before: { Symbol → Value }         # estado antes
  , effect:      Symbol                      # nombre del efecto aplicado
  , state_after: { Symbol → Value }          # estado después
  , metadata:    { Symbol → Value }          # datos adicionales
}
```

**Trace** = `[TraceEntry]`

El trace permite responder:
- Qué ocurrió (event_type, effect)
- Por qué ocurrió (source, trigger que lo disparó)
- Qué cambió (state_before → state_after)
- Qué evento lo causó (event_id)

---

## 12. I/O

### 12.1. INPUT

Inputs se inyectan como eventos programados:

```
inputs = [
    { tick: 0, type: ON_CAST, source: hero_a, target: hero_b, payload: {ability: "fireball"} }
  , { tick: 1, type: ON_MOVE, source: hero_b, target: Null, payload: {x: 5, y: 3} }
  , ...
]
```

Se insertan en la cola de eventos antes de开始 el bucle.

### 12.2. OUTPUT

Output se acumula en `σ.output`:

```
OutputEntry = {
    tick:    Tick
  , type:    Symbol                          # OUT_CHAR | OUT_NUMBER | OUT_STATE | ...
  , value:   Value
  , entity:  EntityId | Null
}
```

El trace final contiene tanto las transiciones como la salida.

---

## 13. Preguntas abiertas (resueltas en SPEC)

### 13.1. Distancia: Manhattan vs Euclidiana

**Decisión:** Manhattan por defecto. Euclidiana disponible como `euclidean()`.
Razón: enteros + Manhattan = cálculo exacto sin floating point. AoE circular
usará euclidiana internamente.

**Estado:** PROPOSED — verificar con tests de AoE.

### 13.2. Orden intra-tick

**Decisión:** FIFO por orden de inserción dentro del mismo tick.
Razón: más simple, determinista, predecible.

**Estado:** PROPOSED — verificar que cascadas ON_DAMAGE→ON_DEATH funcionan.

### 13.3. Call stack

**Decisión:** Sin call stack explícito. `call()` = composición inline de Effects.
`return()` = salida del handler actual. No hay recursion verdadera en el runtime.
Si se necesita recursion, se modela como loop con pila explícita en vars.

**Estado:** PROPOSED — verificar con ejemplos recursivos.

### 13.4. Control de flujo literal

**Decisión:** Las acciones de FLOW son **azúcar sintáctico** que se descomponen
en Effects + Schedule. No necesitan primitivas del runtime.

- `if(c, t, e)` → Effect que evalúa c y ejecuta t o e
- `loop(b)` → `periodic(b, 1)` con break interno
- `wait(n)` → `schedule(continuación, now+n)`

**Estado:** PROPOSED — verificar con ejemplos.

### 13.5. Posición entera vs real

**Decisión:** Enteros. `Pos = (Int, Int)`. Movimiento continua se modela
con ticks sucesivos (cada tick = 1 unidad de distancia a velocidad 1).
Velocidad > 1 = salta varias unidades por tick.

**Estado:** PROPOSED — verificar con movimiento continuo.

### 13.6. Modo de I/O

**Decisión:** Ambos. Input como eventos programados. Output como
`OutputEntry` en `σ.output` + TraceEntry en trace.

**Estado:** PROPOSED.

### 13.7. Stacks en Modifier

**Decisión:** Campo `stacks` del Modifier. Una acción `add_stack` incrementa.
Los efectos que dependen de stacks leen `μ.stacks`. Ejemplo:
`bleed` dota `damage_per_stack × stacks` cada tick.

**Estado:** PROPOSED.

### 13.8. Turing-completeness

**Decisión:** No asumir. Tras implementar el runtime, intentar construir:
1. Un contador de 2 estados (Minsky) usando `vars` + `while`
2. Un recognizer de Brainfuck simple usando I/O + vars + loop

Si se logra: TESTURINGS = VERIFIED.
Si no: documentar el límite.

**Estado:** UNVERIFIED — requiere runtime implementado.

---

## 14. Mapa de 744 acciones → primitivas

Cada acción de ACTIONS.md se traduce a una o más primitivas de la §8.

Patrones comunes:

```
Acción de recurso    → gain / spend / set_resource
Acción de estado     → set / inc / dec / get
Acción de posición   → set_pos / move_to / teleport / distance
Acción de tiempo     → schedule / periodic / cancel
Acción de evento     → emit / on / off / consume
Acción de modifier   → apply_modifier / remove / refresh / add_stack
Acción de gating     → gate / ungated / is_gated
Acción de daño       → damage (con mitigación) / heal
Acción de muerte     → kill (→ trigger_death)
Acción de respawn    → respawn_effect
Acción de cast       → cast pipeline
Acción de projectile → spawn_projectile + periodic
Acción de aura       → create_aura + periodic
Acción de summon     → spawn + periodic
Acción de inventory  → add_item / remove_item / use_item
Acción de flow       → if / loop / wait / call
Acción de math       → add / sub / mul / div / ...
Acción de logic      → and / or / not / ...
Acción de random     → PRNG(rng) → value
Acción de I/O        → output / input_wait
Acción de trace      → trace_event / dump_trace
```

---

## 15. Invariantes del sistema

1. **HP ≤ max_hp** siempre (post-invariante de cada mutación de hp).
2. **mana ≤ max_mana** idem.
3. **tick_now es monótonamente creciente** (nunca retrocede).
4. **Un evento no se procesa dos veces** (consumed = True tras procesar).
5. **Un modifier vivo existe en σ.modifiers Y en target.modifiers**.
6. **Un modifier expirado se remueve de ambos**.
7. **Entity alive=False no procesa triggers propios** (pero sí recibe efectos).
8. **La cola de eventos nunca tiene eventos con tick < tick_now** (se procesan al avance).
9. **El PRNG es determinista**: misma semilla → misma secuencia.

---

## 16. Estados de verificación

Cada sección de esta SPEC se marca con:

| Estado | Significado |
|--------|-------------|
| VERIFIED | Demostrado por tests |
| PROPOSED | Diseñado, no implementado |
| UNVERIFIED | Hipótesis sin diseño |
| FAILED | Refutado por implementación |

**Estado global de SPEC:** PROPOSED.
Todo está diseñado pero no implementado. Los tests de la §15 se crearán
durante la fase de implementación.

---

## 17. Siguiente paso

1. Crear estructura del proyecto: `src/`, `tests/`, `examples/`, `traces/`, `docs/`.
2. Implementar `vm.py` con GameState, step function, event queue.
3. Implementar primitivas de la §8.
4. Tests unitarios de §15 (invariantes).
5. Ejemplos del megacompose: kill counter, cooldown, stun temporal, buff con duración, projectile, AoE, resource loop, combo, item+ability, simulación pequeña.
6. TESTURINGS después de MVP.

---

Evidence before narrative.
Never Guess.
