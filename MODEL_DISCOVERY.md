# DotaCode — MODEL_DISCOVERY

Fase 1. Documento de descubrimiento de modelo. **No es una especificación.**

El objetivo no es definir sintaxis ni implementar. Es descubrir el modelo
computacional mínimo que explique bien el sistema de Dota 2, y marcar cada
afirmación con su nivel de evidencia.

---

## Propósito

DotaCode es un esolang experimental que investiga si los conceptos de
Dota 2 — héroes, habilidades, objetos, recursos, buffs, debuffs,
cooldowns, posición, tiempo y eventos — pueden funcionar como
**primitivas computacionales**.

La ruta es:

    Dota 2  →  comportamiento  →  modelo computacional  →  lenguaje  →  formalización

Este documento cubre la transición `comportamiento → modelo`.
Todo lo que sigue son hipótesis sujetas a verificación por implementación.

---

## Método

1. **OBSERVATION** — qué hace Dota 2 con el concepto (comportamiento conocido).
2. **HYPOTHESIS** — a qué primitiva computacional podría mapearse.
3. **DESIGN** — propuesta concreta de representación.
4. **TEST** — qué verificación derivaría el modelo de la intuición.
5. **STATUS** — nivel de evidencia.

Formalmente reusamos el ciclo:

    OBSERVATION → HYPOTHESIS → DESIGN → IMPLEMENTATION → TEST → RESULT → CONCLUSION

Aquí sólo llegamos hasta DESIGN. Implementation/Test/Result vendrán en fases
posteriores. Las conclusiones aquí son **PROPUESTAS** salvo que se indique lo
contrario.

---

## Leyenda de estados

| Estado       | Significado                                                        |
|--------------|--------------------------------------------------------------------|
| VERIFIED     | Demostrado por tests que corren y pasan.                           |
| PROPOSED     | Hipótesis con diseño concreto, sin implementar aún.                |
| UNVERIFIED   | Afirmación intuitiva sin diseño ni test.                            |
| FAILED       | Hipótesis probada y refutada por implementación/tests.             |
| UNSUPPORTED  | Fuera del alcance del modelo mínimo, no se investigará ahora.       |

Nada en este documento es VERIFIED todavía. Todo es PROPOSED o UNVERIFIED.

---

## Hipótesis central de trabajo

Dota 2 es, computacionalmente, un **sistema reactivo discreto y determinista**
sujeto a tiempo monótono y estado mutable.

La semántica candidata:

    STATE + EVENT + CONDITIONS → EFFECT → NEW STATE

Y, cuando intervienen recursos y tiempo:

    STATE + EVENT + RESOURCE + TIME + POSITION + ACTIVE_EFFECTS
        → RESOLUTION → NEW STATE

Esto es lo mínimo que necesitamos explicar.
Todo lo demás (héroes, items, habilidades, buffs, muerte, respawn) son
**patrones** construidos sobre este núcleo, no primitivas nuevas.

> STATUS: PROPOSED. Verificable implementando un runtime de tick discreto
> con cola de eventos y observando que los casos del spec se construyen
> sin primitivas adicionales.

---

## Análisis concepto por concepto

Cada sección sigue el método. Nada se asume definitivo.

---

### 1. Héroe

**OBSERVATION**
En Dota un héroe es una entidad controlable con identidad, kit de habilidades,
HP, mana, oro, nivel, posición, inventario y ciclo de vida
(vivo / muerto / reapareciendo). Varios pueden coexistir y son distinguibles.

**HYPOTHESIS**
Un héroe es un **Entity** con:
- identidad estable,
- estado mutable tipado,
- un conjunto de triggers (habilidades) y modificadores (items/buffs),
- un ciclo de vida modelado como transición entre estados,
- posición opcional (ver §9).

No es primitiva: es un *perfil* de Entity.

**DESIGN (PROPOSED)**
```
Entity = {
  id:       EntityId
  state:    { [key]: Value }          # hp, mana, gold, level, alive, ...
  triggers: [Trigger]                  # habilidades/acciones
  modifiers:[Modifier]                 # buffs/debuffs/items activos
  position: Pos?                       # ver §9
  tags:    { hero, creep, projectile, ... }
}
```

**TEST**
Construir 2 entidades hero, mutar HP/mana de una sin afectar la otra,
verificar identidad preservada. Verificar que ciclo de vida
(alive→dead→respawn) es secuencia de transiciones de `state.alive` + eventos.

**STATUS: PROPOSED**

---

### 2. Habilidad (ability)

**OBSERVATION**
Una habilidad: el jugador la lanza contra un target, consume mana, inicia
cooldown, produce efectos (daño, buff, proyectil, etc.) y puede estar
bloqueada por silence o por cooldown activo.

**HYPOTHESIS**
Una habilidad es un **Trigger** ligado a un patrón de evento ON_CAST,
sometido a condiciones (cooldown listo, recurso suficiente, no silenciado),
que al dispararse:
- consume un recurso (Effect),
- programa un cooldown (Effect retardado sobre un contador),
- emite eventos (ON_DAMAGE, ON_HIT, ...),
- aplica modifiers.

O sea: `Trigger = { on: EventPattern, if: Condition, then: [Effect] }`.

**DESIGN (PROPOSED)**
```
Ability = Trigger {
  on:    ON_CAST(ability_id, source, target)
  if:    cooldown_ready(ability_id) AND mana>=cost AND not_silenced(source)
  then:  [ SpendMana(cost)
         , StartCooldown(ability_id, cd_ticks)
         , Emit(ON_CAST_RESOLVED, source, target, ability_id)
         , <ability-specific effects> ]
}
```

**TEST**
Cast con mana justo → resuelve. Cast sin mana → no resuelve, sin gasto.
Re-cast durante cooldown → bloqueado. Cast bajo silence → bloqueado.

**STATUS: PROPOSED**

---

### 3. Item

**OBSERVATION**
Un item otorga modificadores pasivos (regen, reducción de cd, +daño) y/o
una habilidad activa. Existe en el inventario del héroe.

**HYPOTHESIS**
Un item es un **contenedor de modifiers y triggers** adjunto a un Entity.
No introduce una nueva primitiva: reusa Modifier y Trigger. El "inventario"
es sólo una lista de items, cada uno aportando sus modifiers/triggers al
estado del portador.

**DESIGN (PROPOSED)**
```
Item = {
  id:        ItemId
  modifiers: [Modifier]   # pasivos: regen, cd_reduction, damage_bonus...
  triggers:  [Trigger]    # activos: ON_USE → Effect
}
# addToInventory(hero, item): añade modifiers a hero.modifiers
#                            añade triggers   a hero.triggers
```

**TEST**
Item de +regen → mana recarga más rápido por tick. Item de cd_reduction →
la misma habilidad entra en cooldown por menos ticks. Item activo →
lanzar ON_USE dispara su trigger.

**STATUS: PROPOSED**

---

### 4. Buff / Debuff

**OBSERVATION**
Un buff/debuff: alguien lo aplica a alguien, tiene duración, puede apilar
stacks, y mientras actiúa modifica el comportamiento (stun impide moverse,
slow reduce velocidad, +armor reduce daño recibido).

**HYPOTHESIS**
Un buff/debuff es un **Modifier**:
- `source`, `target` (Entity refs),
- `type` (stun, slow, armor, ...),
- `duration_ticks` ( expiry ),
- `stacks` (contador opcional),
- `apply(state) → state` (transformación por tick o por evento).

LosModifiers viven en `entity.modifiers` y son consultados por las
condiciones/effects cuando se resuelven acciones.

**DESIGN (PROPOSED)**
```
Modifier = {
  id:       ModifierId
  source:   EntityId
  target:   EntityId
  type:     ModifierType              # stun | slow | silence | dot | armor | ...
  duration: Ticks                      # -1 = permanente hasta dispel
  stacks:   Nat (default 1)
  on_tick:  (state) -> state           # opcional: dot, regen
  on_event:(event, state) -> state?    # opcional: reactivo
  gate:    Set<ActionType>             # acciones que bloquea (stun→{move,cast}, ...)
}
```

El `gate` unifica stun/root/silence (ver §11): no son primitivas, son
modifiers cuyo `gate` restringe categorías de acción.

**TEST**
Aplicar STUN(target, 2s) → durante 2s ON_CAST y ON_MOVE del target se
ignoran. Tras expiry → vuelven a procesarse. Apilar 3 stacks de dot →
daño por tick = 3×base.

**STATUS: PROPOSED**

---

### 5. Cooldown

**OBSERVATION**
Tras usar una habilidad/item, no puede usarse otra vez hasta que pase su
cooldown. Es un **gate temporal por habilidad**.

**HYPOTHESIS**
Cooldown es un **contador temporal por clave**, no una primitiva. Se_modela
como un Resource escalar por `(entity, ability_id)`: el recurso es
"ticks restantes hasta ready". Cada tick decrementa; al llegar a 0 se emite
ON_COOLDOWN_READY y se desbloquea el trigger.

**DESIGN (PROPOSED)**
```
cooldown_state[entity][ability] = Ticks    # 0 = listo

StartCooldown(entity, ability, cd):
  cooldown_state[entity][ability] = cd
  # el loop de tick se encarga de decrementar y emitir ON_COOLDOWN_READY

tick():
  for (e, a) in cooldown_state:
    if cooldown_state[e][a] > 0:
      cooldown_state[e][a] -= 1
      if cooldown_state[e][a] == 0:
        emit(ON_COOLDOWN_READY, e, a)
```

Reducción de cooldown (items/talents) se modela como Modifier que escala
`StartCooldown`' (altera el parámetro `cd` en el Effect).

**TEST**
Cast → cd=5 → ticks 1..4 bloquea re-cast → tick 5 emite ON_COOLDOWN_READY
→ cast permitido. Con item -20% cd → mismo cast deja cd=4.

**STATUS: PROPOSED**

---

### 6. HP

**OBSERVATION**
HP es un entero que baja con daño y sube con curación. Llega a 0 → muerte.

**HYPOTHESIS**
HP es un **Resource escalar** con cambio → evento **ON_RESOURCE_CHANGE**
y queda en `entity.state.hp`. No es primitiva: es State numérico con
invariante `hp <= max_hp` y transición especial en `hp <= 0`.

**DESIGN (PROPOSED)**
```
state.hp   : Int (0..max_hp)
state.max_hp: Int

ApplyDamage(entity, amount):
  before = state.hp
  state.hp = max(0, state.hp - amount)
  emit(ON_DAMAGE, source, entity, amount)
  emit(ON_RESOURCE_CHANGE, entity, hp, before, state.hp)
  if state.hp == 0 and alive:
    trigger_death(entity)
```

Mitigación (armor) es un Modifier que altera `amount` antes de restar.

**TEST**
Daño igual a HP → hp=0, ON_DEATH emitido, `alive=false`. Curación encima
de max_hp → topea en max_hp. ON_RESOURCE_CHANGE emite la delta correcta.

**STATUS: PROPOSED**

---

### 7. Mana / Recursos

**OBSERVATION**
Mana se gasta al castear y se regenera por tick. Oro se gana en eventos
(kills, pasivos) y se gasta en items. Stacks/charges son contadores con
significado contextual.

**HYPOTHESIS**
Todos son **State numérico** con dos operaciones universales:
`spend(x)` y `gain(x)`, más opcional `regen_per_tick`. Se unifican bajo
un único modelo de **Resource**:

```
Resource = {
  key:    Symbol                       # hp | mana | gold | stacks[id] | charges[id]
  value:  Int
  max:    Int?
  regen:  Int (default 0)             # por tick
}
spend(r, x): if r.value >= x: r.value -= x; emit(ON_RESOURCE_CHANGE); return true
                       else: return false   # insuficiente
gain(r, x): r.value = min(r.max ?? r.value+x, r.value + x); emit(...)
```

No hay 5 primitivas (HP, MANA, GOLD, STACKS, CHARGES): hay **una** primitiva
`Resource` instanciada por clave. Esto reduce el modelo.

**TEST**
Definir `Resource(mana, 100, regen=2)`. Tras 10 ticks sin cast → mana=100.
Tras cast cost=30 → mana=70 → 1 tick → 72. Stack funcionar igual con
`key=stacks[ability]`.

**STATUS: PROPOSED**

---

### 8. Posición

**OBSERVATION**
Héroes y proyectiles están en un plano. Importan: distancia, rango de
habilidad, área de efecto, colisión, movimiento.

**HYPOTHESIS**
Posición es un **State de tipo Vec2** (x, y). Distancia/rango/AoE/colisión
son **funciones puras** derivadas, no primitivas. Movimiento es un
Effect que actualiza posición a lo largo de ticks.

**DESIGN (PROPOSED)**
```
Pos = (x: Int, y: Int)            # enteros para mantener determinismo fácil

dist(a, b) = |a.x-b.x| + |a.y-b.y|   # Manhattan, o euclidiana si se justifica
in_range(source, target, r) = dist(source.pos, target.pos) <= r
in_area(center, radius, point)  = dist(center, point) <= radius

MoveTo(entity, dst, speed):
  programar Effect por tick que mueva `entity.pos` hacia `dst`
  hasta llegar; emite ON_MOVE por tick.
```

No se implementa un mapa de Dota. Sólo el modelo espacial mínimo.

**TEST**
Dos entidades a distancia 3 → rango 3 las incluye, rango 2 no. AoE radio
2 desde (0,0) incluye (1,1), (2,0), no (3,0). MoveFrom (0,0)→(3,0) speed=1
→ 3 ticks, pos=3.

**STATUS: PROPOSED** — la elección de Manhattan/euclidiana está
**UNVERIFIED** hasta decidir sus implicaciones en AoE circular.

---

### 9. Proyectil (projectile)

**OBSERVATION**
Muchas habilidades crean un proyectil que viaja desde el caster hasta el
target; al impactar aplica su efecto. El target puede moverse; el
proyectil puede fallar si el target muere o se va fuera de rango.

**HYPOTHESIS**
Un proyectil es un **Entity** con tag `projectile`, con posición, destino,
velocidad y un payload de Effects. En cada tick se mueve; al llegar
(dist <= 0) emite ON_HIT y aplica el payload; si el target ya no es válido
(cancelado/muerto), emite ON_MISS y se destruye.

**DESIGN (PROPOSED)**
```
Projectile = Entity {
  tags: { projectile }
  state: { pos: Pos, target: EntityId, speed: Int, payload: [Effect] }
  triggers: [
    Trigger(on=ON_TICK, if=dist(pos,target.pos)<=0,
            then=[ Apply(payload, target); Destroy(self); emit(ON_HIT) ])
  ]
}
# si target muere: handler de ON_DEATH invalida el proyectil
```

Reusa Entity + Trigger + Effect. No introduce primitiva.

**TEST**
Projectile speed=1 desde (0,0) hacia target en (3,0) → tras 3 ticks
emite ON_HIT y aplica daño. Si target muere en tick 2 → tick 3 emite
ON_MISS, no aplica efecto.

**STATUS: PROPOSED**

---

### 10. Stun / Root / Silence

**OBSERVATION**
- Stun: impide moverse y castear.
- Root: impide moverse, permite castear.
- Silence: impide castear, permite moverse.

**HYPOTHESIS**
No son tres primitivas. Son **Modifiers con un campo `gate`** que es un
subconjunto de `{move, cast, attack, ...}`:
- stun   → gate = {move, cast, attack}
- root   → gate = {move}
- silence→ gate = {cast}

Un trigger, antes de resolver, consulta todos los modifiers activos del
actor y aborta si alguno gatea la categoría de acción correspondiente.

**DESIGN (PROPOSED)**
```
ActionType = { move, cast, attack, item_use, ... }

check_gated(entity, action):
  for m in entity.modifiers:
    if action in m.gate:
      emit(ON_ACTION_BLOCKED, entity, action, m.id)
      return true
  return false

Trigger.if añade: AND not check_gated(source, action_type_of(trigger))
```

**TEST**
STUN(hero, 2s) → durante 2 ticks: ON_CAST y ON_MOVE bloqueados,
ON_ITEM_USE bloqueado. Tras expiry → todos permiten. ROOT(hero) →
ON_CAST permitido, ON_MOVE bloqueado. SILENCE → al revés.

**STATUS: PROPOSED**

---

### 11. Daño (damage)

**OBSERVATION**
El daño reduce HP, puede ser de varios tipos (mágico/físico/puro), mitigado
por armor/resistencia, y puede ser letal o no letal.

**HYPOTHESIS**
Daño es un **Effect** `ApplyDamage(target, amount, type)` que:
1. consulta modifiers de mitigación del target (armor, magic_resist),
2. ajusta `amount`,
3. decrementa `state.hp`,
4. emite ON_DAMAGE y ON_RESOURCE_CHANGE,
5. dispara death si `hp == 0`.

No es primitiva: es Effect sobre Resource HP.

**DESIGN (PROPOSED)**
```
ApplyDamage(target, raw, type):
  amt = raw
  for m in target.modifiers:
    amt = m.on_damage_received(amt, type) if m handles type
  apply_to_hp(target, -amt)
```

AoE es un Effect que itera entidades en rango y aplica ApplyDamage a cada una.

**TEST**
Daño 100 a hero hp=100 sin mitigación → hp=0, ON_DEATH. Con armor 25%
→ hp=25, no death. Daño mágico con magic_resist 0 → aplica íntegro.

**STATUS: PROPOSED**

---

### 12. Muerte (death)

**OBSERVATION**
Cuando HP llega a 0 el héroe muere: deja de actuar, suelda oro al
asesino, drop de estados, y se programa un respawn.

**HYPOTHESIS**
Muerte es una **transición de estado** disparada por la condición
`hp <= 0 AND alive`, que:
- pone `alive=false`,
- emite ON_DEATH (source=killer, target=víctima),
- retira/dispara modifiers dependientes,
- programa Effect retardado `Respawn(entity, delay)`.

No es primitiva: es Trigger sobre ON_DAMAGE con condición de hp.

**DESIGN (PROPOSED)**
```
Trigger (on=ON_DAMAGE, if=target.alive AND target.hp==0,
         then=[ set_alive(target,false)
              , emit(ON_DEATH, source, target)
              , schedule(Respawn(target, respawn_ticks), at=now+respawn_ticks)
              , remove_modifiers(target, on_death) ])
```

**TEST**
Bajar hp a 0 exactamente → ON_DEATH emitido una sola vez, alive=false.
Bajar a -5 (sobra daño) → idem, no doble muerte. Matar un ya-muerto →
no emite nada.

**STATUS: PROPOSED**

---

### 13. Respawn

**OBSERVATION**
Tras respawn_timeout el héroe reaparece en base con HP/mana llenos.

**HYPOTHESIS**
Respawn es un **Effect retardado** (delayed event) que:
- restaura hp= max_hp, mana= max_mana,
- mueve pos a spawn_point,
- set `alive=true`,
- emite ON_SPAWN.

No es primitiva: es Effect programado por el Trigger de muerte.

**DESIGN (PROPOSED)**
```
Respawn(entity, delay):
  schedule(at=tick_now+delay, effect=
    [ set_state(entity, hp=max_hp, mana=max_mana)
    , set_pos(entity, spawn_point)
    , set_alive(entity, true)
    , emit(ON_SPAWN, entity) ])
```

**TEST**
Muerte con delay=5 → ticks 1..4 alive=false, en tick 5 ON_SPAWN y
alive=true, hp=max_hp, pos=spawn. Muerte de ya-muerto no reprograma.

**STATUS: PROPOSED**

---

### 14. Eventos

**OBSERVATION**
Dota está impulsado por eventos discretos: cast, hit, damage, death,
spawn, move, cd_ready, resource_change. Cada uno puede tener handlers
cascade que producen otros eventos.

**HYPOTHESIS**
Evento = { tick, type, source?, target?, payload }. El runtime mantiene
una **cola de eventos ordenada por tick**. Cada turno del loop:
1. saca todos los eventos del tick actual,
2. para cada uno, recorre triggers que matcheen el patrón,
3. evalúa condiciones,
4. si pasa, ejecuta effects (que pueden encolar nuevos eventos, en
   este tick si son instantáneos o en ticks futuros si son retardados).

Esto es **event-driven programming + state machine** combinados.

**DESIGN (PROPOSED)**
```
Event    = { tick, type, source?, target?, payload }
EventQueue = prioridad por (tick,插入_order)        # FIFO dentro del tick

emit(ev):   queue.push(ev)                          # tick = tick_now
schedule(ev, at): queue.push(ev with tick=at)

run():
  while queue not empty:
    ev = queue.pop_min()
    tick_now = ev.tick
    for trigger in all_triggers:
      if trigger.matches(ev) and eval(trigger.if):
        run_effects(trigger.then, ev)
```

Eventos del mismo tick se procesan en orden de inserción (determinismo).
Triggers pueden encolar eventos en `tick_now` (efecto inmediato,
procesado en siguiente iteración del loop) o en `tick_now+d` (retardado).

**TEST**
ON_CAST → ON_DAMAGE → ON_DEATH encadenados: los tres eventos aparecen en
el trace en ese orden, mismo tick si son inmediatos, distintos si
retardados. La cola nunca procesa un tick futuro antes de vaciar el actual.

**STATUS: PROPOSED** — el orden exacto intra-tick (FIFO vs prioridad de
tipo) está **UNVERIFIED**. Es decisión de diseño que afecta semántica y
deberá fijarse tras implementación.

---

## Preocupaciones transversales

---

### T1. Tiempo

**OBSERVATION**
Dota tiene: tick (servidor 30 Hz), duraciones de buff, cooldowns,
eventos retardados, eventos periódicos, expiries.

**HYPOTHESIS**
Un único reloj discreto `tick_now: Nat` que avanza en +1. Toda duración
se expresa en ticks. Periodicidad = Effect que se reprograma a sí mismo.
Expiry = Modifier que en `on_tick` decrementa `duration` y se retira al
llegar a 0.

**DESIGN (PROPOSED)**
```
tick_now: Nat
advance(): tick_now += 1; process scheduled events with tick == tick_now
Periodic(ev, every=d): schedule(ev); efecto interno re-schedulea en +d
ExpireModifier: on_tick(state){ state.duration-=1; if 0: self-remove }
```

**STATUS: PROPOSED**

---

### T2. Determinismo

**OBSERVATION**
Un mismo partido con mismas acciones no se repite por RNG latente, pero
el motor es determinista dada una seed.

**HYPOTHESIS**
El runtime es función pura de `(seed, program, initial_state)` y produce
**exactamente el mismo trace** siempre. Cualquier aleatoriedad debe
atravesar un PRNG sembrado único y global; nunca `random()` del lenguaje
host directa.

**DESIGN (PROPOSED)**
```
Runtime = (seed, program, initial_state)
rng = PRNG(seed)                # único punto de no-determinismo controlado
run(...) -> Trace               # reproducible
```

**TEST**
Dos runs con misma seed+programa+initial_state → traces byte-idénticos.
Dos runs con seed distinta → traces difieren sólo donde pidió rng.

**STATUS: PROPOSED**

---

### T3. Memoria / I/O

**OBSERVATION**
Necesitamos: variables del programa, estado de entidades, cola de
eventos, y comunicación con el exterior (input inicial, output final).

**HYPOTHESIS**
- **Memoria local** : `vars: { [name]: Value }` por programa.
- **Memoria entity**: `entity.state`, ya cubierta.
- **Memoria runtime**: `event_queue`, `tick_now`, `rng`.
- **INPUT**: secuencia de events externos inyectados al inicio
  (ej.  `ON_CAST(hero_a, ability_x, hero_b)` programados en tick=0,1,2,...).
- **OUTPUT**: el trace mismo, o un conjunto de `OUT(symbol, value)`
  emitidos como eventos `ON_OUT` que el runtime vuelca al final.

**DESIGN (PROPOSED)**
```
INPUT  = lista de Event (tick, type, payload) inyectados en la cola
OUTPUT = filtrar trace por events type==ON_OUT, o state final de vars
```

**TEST**
Programa `emit(ON_OUT, "A")` con input vacío → output=`["A"]`. Programa
que lee `IN` → output depende del input provisto. Mismo input → mismo
output.

**STATUS: PROPOSED** — el modo exacto de I/O (evento ON_OUT vs volcado
de state) está **UNVERIFIED**; se decide en SPEC posterior.

---

### T4. Control de flujo

**OBSERVATION**
Necesitamos IF/ELSE, LOOP, BREAK, CONTINUE, CALL, RETURN, WAIT, DELAY.

**HYPOTHESIS**
Para mantener el modelo reactivo, el control de flujo **NO** se introduce
como sintaxis tradicional. En su lugar:
- `IF/ELSE`     = branching entre Effects según Condition.
- `LOOP`        = Effect periódico que se reagenda hasta BREAK.
- `BREAK`       = desagenda el loop padre.
- `WAIT/DELAY`  = `schedule(effect, at=tick_now + d)`.
- `CALL/RETURN` = macros de composición de Effects (sin call stack
  explícito en el runtime, sólo toys de programación).

Puede emerger del sistema de eventos sin instrucciones literales. La
sintaxis, si aparece, es café de fase posterior.

**DESIGN (PROPOSED)**
```
If(cond, then, else):= if cond then then() else else()
Loop(body, every=d):  schedule(body; Loop(body, every=d), at=now+d)
Wait(d, body):        schedule(body, at=now+d)
```

**STATUS: PROPOSED** — la hipótesis de que el control de flujo no
necesita estructuras literales es **UNVERIFIED**; podrían aparecer
casos patológicos que lo exijan. Se revisita en SPEC.

---

## Modelo mínimo propuesto (consolidado)

Tras el análisis, las primitivas que parecen suficientes son:

```
PRIMITIVAS (7):
  Entity      = { id, state, triggers, modifiers, position?, tags }
  State       = (clave → Valor)              # tipado laxo (Int, Bool, Vec2)
  Event       = { tick, type, source?, target?, payload }
  Effect      = (ctx) -> StateChange / NuevoEvent
  Trigger     = { on: EventPattern, if: Condition, then: [Effect] }
  Modifier    = { source, target, type, duration, stacks, gate?, on_tick?, ... }
  Time        = tick_now: Nat   (avanza +1; cola ordenada)

DERIVADOS (no primitivas):
  Resource   = State numérico con spend/gain/regen      # hp, mana, gold, stacks
  Position   = State Vec2 + funciones puras              # dist, range, aoe
  Cooldown   = Resource contador por (entity, ability)
  Buff/Debuff= Modifier
  Stun/Root/Silence = Modifier con gate
  Ability    = Trigger sobre ON_CAST
  Item       = contenedor de Modifier + Trigger
  Projectile = Entity con triggers ON_TICK que mueven y aplican payload
  Damage     = Effect sobre Resource HP
  Death      = Trigger sobre ON_DAMAGE con condición hp==0
  Respawn    = Effect retardado por schedule
  IF/LOOP/WAIT = composiciones de Effect/schedule, no instrucciones literales (hipótesis)
```

Invariante central (la "máquina"):

```
STATE + EVENT + CONDITIONS + (RESOURCE / TIME / POSITION / ACTIVE_EFFECTS)
   → RESOLUTION (Trigger matching + Effect execution)
   → NEW STATE + (nuevos EVENTs encolados)
```

> STATUS global del modelo mínimo: **PROPOSED**.
> No es VERIFIED hasta implementar el runtime y construir con esas
> primitivas todos los ejemplos del spec (kill counter, cooldown, stun
> temporal, buff con duración, projectile, AoE, resource loop, combo de
> habilidades, item + ability, simulación pequeña).

Si la implementación fuerza añadir más primitivas, este documento se
actualiza y la primitiva extra se marca con su razón.

---

## Preguntas abiertas

1. **Distancia: Manhattan vs euclidiana.** Manhattan simplifica AoE
   cuadrada; AoE circular es más fiel a Dota. Decidir tras ver ejemplos
   de AoE. (UNVERIFIED)
2. **Orden intra-tick.** FIFO de inserción vs prioridad por tipo de
   evento. Afecta a cascadas (ON_DAMAGE→ON_DEATH). (UNVERIFIED)
3. **¿Necesitamos call stack real?** Si CALL/RETURN emerge de macros
   de composición de Effects, basta. Hay que comprobarlo con recursion
   en ejemplos. (UNVERIFIED)
4. **¿Control de flujo literal imprescindible?** La hipótesis es que
   emerge de Triggers + schedule. LOOP infinito o BREAK condicional
   podrían romperla. (UNVERIFIED)
5. **Stacks: ¿son un Resource por modifier o un campo del Modifier?**
   Ambas opciones existen. Decidir en SPEC según simplicidad. (UNVERIFIED)
6. **Posición entera vs real.** Enteros ayudan al determinismo; reales
   son más naturales para movimiento. Probar enteros primero. (UNVERIFIED)
7. **¿ON_OUT como evento o como snapshot de state al final?** Modo de
   I/O a fijar en SPEC. (UNVERIFIED)
8. **Turing-completeness.** No asumir. Tras implementar, elegir prueba
   adecuada (Brainfuck / Minsky 2-counter / Rule 110 / SKI / UTM) y
   ejecutar la que mejor encaje. Documentar límite si no se logra. (UNVERIFIED)

---

## Siguiente investigación

1. Decidir las 4–5 preguntas abiertas más críticas (distancia, orden
   intra-tick, control de flujo, I/O) escribiendo *bench examples*
   mínimos que las discriminen — **antes** de SPEC.md.
2. Una vez fijadas, escribir **SPEC.md** con semántica operacional
   formal (`small-step`) sobre las 7 primitivas.
3. Implementar runtime mínimo en Python (siguiendo la convención de los
   esolangs vecinos del laboratorio: Pokecode, DuelCode, SpellCode), con
   `vm.py`, `events.py`, `entities.py`.
4. Tests de estado/recursos/movimiento/eventos/cooldowns/buffs/damage
   /death/respawn/IO, uno por concepto de este documento.
5. Ejemplos los 10 del spec; revisión de TESTURINGS sólo tras MVP.

---

## Estado del documento

- Todo lo aquí descrito es **PROPOSED** o **UNVERIFIED**.
- Nada es VERIFIED todavía.
- Nada es FAILED todavía (no se ha probado nada).
- Nada es UNSUPPORTED excepto explícitamente (mapa 3D, multiplayer, UI,
  gráficos, red, bots, simulador completo).

Evidence before narrative.
Never Guess.
