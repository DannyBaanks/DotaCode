# DotaCode

Esolang experimental inspirado en Dota 2.

---

## ¿Qué es?

DotaCode es un lenguaje de programación esotérico que investiga si los
conceptos de Dota 2 — héroes, habilidades, items, buffs, debuffs,
cooldowns, posición, tiempo y eventos — pueden funcionar como
**primitivas computacionales**.

No es un clon de Dota 2. Es un experimento sobre programación reactiva,
estado mutable, y sistemas de eventos discretos.

---

## ¿Por qué Dota 2?

Dota 2 es un sistema complejo donde convergen:
- **Estado mutable** (HP, mana, posición, buffs)
- **Eventos discretos** (cast, hit, damage, death)
- **Tiempo** (cooldowns, duraciones, ticks)
- **Recursos** (HP, mana, gold, stacks, charges)
- **Acciones condicionales** (gating por stun/root/silence)
- **Efectos persistentes** (modifiers, auras)

La hipótesis de DotaCode es que estos conceptos forman un **modelo
computacional completo** sin necesidad de primitivas adicionales.

---

## Modelo de máquina

### Primitivas (7)

| Primitiva  | Descripción                                    |
|------------|------------------------------------------------|
| `Entity`   | Entidad con identidad, estado mutable, tags    |
| `State`    | Mapa clave→valor mutable por entity            |
| `Event`    | Ocurrencia discreta en un tick                  |
| `Effect`   | Función que muta GameState                      |
| `Trigger`  | Vínculo evento→condición→[effects]             |
| `Modifier` | Estado temporal con duración, stacks, gates     |
| `Time`     | Tick monótono + cola de eventos ordenada        |

### Semántica central

```
STATE + EVENT + CONDITIONS → EFFECT → NEW STATE
```

Todo en DotaCode se construye sobre esta máquina. Las 744 acciones
del catálogo se descomponen en composiciones de estas 7 primitivas.

---

## Entidades

```python
Entity = {
    id, type, state, triggers, modifiers,
    position, spawn_pos, tags, alive, owner
}
```

Las entity se crean con `spawn_entity()` y se destruyen con
`destroy_entity()`. Cada entity tiene un `state` mutable (HP, mana,
posición, etc.), triggers que responden a eventos, y modifiers
buff/debuff activos.

---

## Eventos

Los eventos son el motor del sistema. Cada tick, el runtime procesa
la cola de eventos FIFO:

```
ON_CAST → ON_DAMAGE → ON_DEATH → ON_MODIFIER_EXPIRED → ...
```

Los triggers escuchan eventos y ejecutan effects cuando la condición
se cumple.

---

## Estado

El `state` de una entity es un mapa `{key: value}`. Ejemplo:

```python
{"hp": 100, "hp_max": 100, "mana": 50, "damage": 25}
```

Las operaciones de estado: `set`, `inc`, `dec`, `clamp`, `get`.

---

## Recursos

Los recursos son state numérico con operaciones especializadas:

```python
spend(entity, "mana", 30)     # consume si tiene
gain(entity, "hp", 20)        # añade (respeta max)
set_resource(entity, "gold", 500)
```

Cada recurso puede tener `_max` (tope) y `_regen` (regeneración/tick).

---

## Tiempo

Un tick = una unidad de tiempo. Las duraciones se expresan en ticks:

```python
apply_modifier(source, target, "STUN", 3)  # 3 ticks de stun
periodic(effect, every=1)                   # cada tick
schedule(effect, tick_offset=5)             # en 5 ticks
```

---

## Posición

`Pos = (x, y)` enteros. Manhattan distance por defecto:

```python
distance(a, b)      # |ax-bx| + |ay-by|
in_range(a, b, 5)   # True si distance <= 5
```

---

## Habilidades

Una habilidad es un **Trigger** sobre `ON_CAST`:

```python
Trigger(
    on="ON_CAST",
    if=cooldown_ready AND mana >= cost AND not_silenced,
    then=[
        spend(mana, cost),
        start_cooldown(ability, 5),
        damage(target, 50),
    ]
)
```

---

## Items

Un item es un contenedor de **modifiers** y **triggers**:

```python
# Item pasivo: +regen
apply_modifier(source, hero, "ITEM_REGEN", -1, on_tick=regen_effect)

# Item activo: heal
Trigger(on="ON_ITEM_USE", if=item_ready, then=[heal(hero, 50)])
```

---

## Buffs / Debuffs

Los modifiers modelan buffs y debuffs:

```python
# Buff: +damage por 10 ticks
apply_modifier(source, hero, "DAMAGE_BUFF", 10, on_tick=damage_up)

# Debuff: stun que bloquea move y cast
apply_modifier(source, enemy, "STUN", 3,
               gate={ActionType.MOVE, ActionType.CAST})
```

El campo `gate` unifica stun/root/silence:
- `stun` → gate = {MOVE, CAST, ATTACK}
- `root` → gate = {MOVE}
- `silence` → gate = {CAST}

---

## Sintaxis

DotaCode actualmente se programa en **Python** usando la API del runtime.
El parser de sintaxis propia es un paso futuro (el modelo se investiga
antes que la sintaxis).

---

## Ejemplos

```python
from src import *

def setup(gs):
    hero = gs.spawn_entity("hero", {"mana": 100, "hp": 100})
    enemy = gs.spawn_entity("enemy", {"hp": 80})

    def on_cast(gs, ctx):
        e = gs.get_entity(ctx["target"])
        if e:
            e.state["hp"] -= 30
        return gs

    t = Trigger(id=gs.new_trigger_id(), on="ON_CAST", source=hero.id, then=[on_cast])
    gs.add_trigger(t)
    emit("ON_CAST", source=hero.id, target=enemy.id)(gs, {})

gs = run(seed=42, setup_fn=setup)
```

Ver `examples/examples_10.py` para los 10 ejemplos del megacompose.

---

## Tests

```bash
python tests/test_core.py
python examples/examples_10.py
```

**29 tests** de invariantes y funcionalidad.
**10 ejemplos** del megacompose verificados.

---

## Estructura

```
DotaCode/
├── README.md
├── MODEL_DISCOVERY.md    # Fase 1: descubrimiento del modelo
├── ACTIONS.md            # Catálogo de 744 acciones (29 ramas)
├── SPEC.md               # Especificación formal (semántica small-step)
├── src/
│   ├── __init__.py
│   ├── prng.py           # PRNG determinista (xorshift64)
│   ├── dtypes.py         # Entity, Modifier, Event, Trigger, EventQueue
│   ├── gamestate.py      # GameState (estado global del mundo)
│   ├── effects.py        # 10 primitivas de Effect + composición
│   ├── triggers.py       # Matching de triggers + gating
│   └── runtime.py        # run_loop (ciclo de ejecución)
├── tests/
│   └── test_core.py      # 29 tests de invariantes
├── examples/
│   └── examples_10.py    # 10 ejemplos del megacompose
├── traces/
└── docs/
```

---

## TESTURINGS

### Lo que SI esta demostrado

`minsky_dotacode.py` compila una maquina de contadores a **triggers de
DotaCode**. Python solo ensambla; el computo lo hace `run_loop` despachando
eventos y aplicando efectos del runtime (`inc_state`, `dec_state`, `emit`).

```
INC(r, j)        trigger ON STATE_i -> [inc_state(r), emit(STATE_j)]

JZDEC(r, j, k)   trigger ON STATE_i  si contador > 0
                     -> [dec_state(r), emit(STATE_j)]
                 trigger ON STATE_i  si contador == 0
                     -> [emit(STATE_k)]
```

La bifurcacion la decide el motor evaluando `if_cond`, no un `if` de Python.
Resultados medidos:

```
suma(7,5)       -> a = 12      (dos registros exactos)
multiplica(6,7) -> acc = 42
```

`tests/test_minsky_dotacode.py` incluye `test_el_motor_hace_el_trabajo`, que
compila el programa **sin** ejecutar el bucle y comprueba que no hay resultado;
solo tras `run_loop` aparece. Esa es la diferencia entre una reduccion y una
simulacion en Python.

**Alcance:** DotaCode expresa cualquier programa de maquina de contadores. Las
de dos registros son Turing-completas bajo una codificacion de la entrada
(Minsky, 1967). La afirmacion hereda esa condicion, ni una mas.

### Lo que NO esta demostrado

`tests/testurings.py` (Brainfuck, Rule 110, SKI, y las dos Minsky antiguas)
**no son reducciones.** Auditado el 2026-08-21: calculan en Python y guardan el
resultado en `gs.globals`, y luego afirman sobre el valor que ellos mismos
metieron:

```python
if instr[0] == "INC":
    e.state[reg] = e.state.get(reg, 0) + 1     # dict de Python, + 1 de Python
```

Se conservan como especificacion ejecutable de los modelos que se quiere
alcanzar, con una advertencia en la cabecera del modulo. No cuentan como
evidencia. Cuando alguno se implemente sobre el runtime, sube a la seccion de
arriba con su test.


## Limitaciones

- **Sin parser propio** — se programa vía API Python
- **Sin I/O de archivos** — solo stdin/stdout conceptual
- **Sin multiplayer** — mundo single-threaded
- **Sin gráficos** — solo trace estructurado
- **Sin mapa de Dota** — posición abstracta (x, y)
- **Sin stats oficiales** — valores son ejemplos, no balance

---

## Relación con otros esolangs

| Esolang    | Modelo                        |
|------------|-------------------------------|
| PokéCode   | ISA / operaciones              |
| DuelCode   | cartas / efectos / cadenas     |
| SpellCode  | hechizos / transformaciones    |
| DotaCode   | sistema dinámico de entidades, tiempo, recursos y eventos |

---

## IP / Publicación

**DESCARGO DE RESPONSABILIDAD / DISCLAIMER:**

DotaCode es un proyecto **experimental y no oficial**. No está afiliado,
patrocinado ni aprobado por Valve Corporation.

**Dota 2** es una marca registrada de **Valve Corporation**. Todos los
derechos de nombre, marcas, logotipos, sprites, artwork, música, código
propietario y assets de Dota 2 pertenecen exclusivamente a Valve Corporation.

DotaCode **no usa**:
- logos oficiales de Dota 2
- sprites o artwork de Dota 2
- música de Dota 2
- código propietario de Valve
- assets oficiales de Dota 2

DotaCode es un experimento de lenguajes de programación esotéricos que
se inspira en los **conceptos** de Dota 2 (héroes, habilidades, items,
buffs, debuffs, cooldowns, posición, tiempo, eventos) como primitivas
computacionales. El uso de estos conceptos es con fines educativos e
investigativos.

**Valve Corporation no respalda ni está afiliada a este proyecto.**

---

Evidence before narrative.
Never Guess.
