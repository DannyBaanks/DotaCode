# DotaCode — ACTIONS — Catálogo completo

Catálogo de **todas** las acciones posibles del lenguaje.
Cada acción es un **Effect** o composición de Effects sobre las 7 primitivas:

    Entity | State | Event | Effect | Trigger | Modifier | Time

---

## Árbol global — ramas y subramas

```
ACTIONS
│
├─[A] ENTIDAD & ESTADO
│   ├─1. ENTITY          — ciclo de vida, identidad, clonación
│   ├─2. STATE           — lectura/escritura de estado mutable
│   ├─3. MEMORY          — variables, pilas, colecciones
│   └─4. RESOURCE        — HP, mana, gold, stacks, charges
│
├─[B] ESPACIO-TIEMPO & EVENTOS
│   ├─5. SPACE           — posición, distancia, movimiento, AoE
│   ├─6. TIME            — scheduling, duration, periódicos
│   ├─7. EVENT           — emisión, suscripción, consumo, routing
│   └─8. PROJECTILE      — entidades viajeras
│
├─[C] MODIFICACIÓN & CONTROL
│   ├─9. MODIFIER        — ciclo de vida de buffs/debuffs
│   ├─10. CONTROL        — gating de acciones (stun/root/silence)
│   ├─11. DISPEL         — remoción de modifiers
│   ├─12. AURA           — modificadores persistentes de área
│   ├─13. SHIELD         — capas de absorción
│   ├─14. REFLECT        — redirección de daño/eventos
│   └─15. VISION         — revelar/ocultar
│
├─[D] COMBATE & DAÑO
│   ├─16. DAMAGE         — reducción de HP con mitigación
│   ├─17. HEAL           — restauración de HP
│   ├─18. DEATH          — terminal lifecycle
│   ├─19. RESPAWN        — revivir
│   ├─20. CAST           — pipeline de invocación de habilidad
│   ├─21. TARGET         — resolución de objetivo
│   ├─22. SUMMON         — entidades derivadas
│   └─23. INVENTORY      — gestión de items
│
└─[E] LINGÜÍSTICA & META
    ├─24. FLOW           — control de flujo
    ├─25. MATH           — aritmética
    ├─26. LOGIC          — booleanos/predicados
    ├─27. RANDOM         — RNG sembrado
    ├─28. IO             — entrada/salida
    └─29. TRACE          — observabilidad/debug
```

**Leyenda FIRMA:**
`NOMBRE(params) → retorno` — una línea por acción.
Columnas: **#** | **NOMBRE** | **FIRMA** | **RETORNO** | **DESCRIPCIÓN**

Primitivas reutilizadas: **E**=Entity, **S**=State, **V**=Event, **F**=Effect, **T**=Trigger, **M**=Modifier, **W**=Time

---

## [A] ENTIDAD & ESTADO

---

### 1. ENTITY — ciclo de vida, identidad, clonación

**1a. Creación / destrucción**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 1 | spawn_entity | (type, state, position?, tags) | EntityId | Crea entity con identidad única |
| 2 | destroy_entity | (entity) | — | Retira entity, emite ON_DESTROY |
| 3 | exists | (entity) | Bool | Verdadero si entity está viva |
| 4 | spawn_at | (type, state, position, tags) | EntityId | Crea en posición específica |
| 5 | spawn_copy | (entity, overrides?) | EntityId | Copia con mismo state + overrides |

**1b. Transformación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 6 | morph_into | (entity, new_type, dur) | — | Transforma temporalmente en otro tipo |
| 7 | morph_back | (entity) | — | Revierte morph |
| 8 | shapeshift | (entity, new_state, dur) | — | Cambia forma sin cambiar identity |

**1c. Consulta**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 9 | get_entity | (entity_id) | Entity? | Recupera por id |
| 10 | get_type | (entity) | Type | Tipo de entity |
| 11 | get_owner | (entity) | EntityId | Dueño (null para neutrals) |
| 12 | is_alive | (entity) | Bool | alive == true |
| 13 | has_tag | (entity, tag) | Bool | Verifica tag |
| 14 | count_entities | (filter?) | Nat | Cuenta entities con filtro |

**1d. Propiedad**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 15 | set_owner | (entity, new_owner) | — | Cambia dueño |
| 16 | is_owned_by | (entity, owner) | Bool | Verifica propiedad |
| 17 | transfer_ownership | (entity, from, to) | — | Transfiere solo si coincide |

---

### 2. STATE — lectura/escritura de estado mutable

**2a. Escritura**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 18 | set_state | (entity, key, value) | — | Asigna valor |
| 19 | set_state_if | (entity, key, value, cond) | — | Asigna solo si condición se cumple |
| 20 | set_multi | (entity, {key: value, ...}) | — | Asigna múltiples claves |
| 21 | init_state | (entity, key, value) | — | Asigna solo si clave no existía |

**2b. Lectura**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 22 | get_state | (entity, key) | Value | Lee valor del state |
| 23 | get_state_default | (entity, key, default) | Value | Lee con default si no existe |
| 24 | has_state | (entity, key) | Bool | Verifica existencia de clave |
| 25 | state_equals | (entity, key, value) | Bool | Verifica igualdad exacta |

**2c. Mutación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 26 | inc_state | (entity, key, delta?) | — | Incrementa (delta=1 por defecto) |
| 27 | dec_state | (entity, key, delta?) | — | Decrementa |
| 28 | mul_state | (entity, key, factor) | — | Multiplica |
| 29 | clamp_state | (entity, key, min, max) | — | Limita al rango [min, max] |

**2d. Comparación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 30 | state_gt | (entity, key, value) | Bool | state > value |
| 31 | state_gte | (entity, key, value) | Bool | state >= value |
| 32 | state_lt | (entity, key, value) | Bool | state < value |
| 33 | state_lte | (entity, key, value) | Bool | state <= value |
| 34 | state_eq | (entity, key, value) | Bool | state == value |
| 35 | state_neq | (entity, key, value) | Bool | state != value |
| 36 | state_between | (entity, key, lo, hi) | Bool | lo <= state <= hi |

**2e. Borrado**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 37 | clear_state | (entity, key) | — | Elimina una clave |
| 38 | clear_all_state | (entity) | — | Todo el state (conserva id) |
| 39 | reset_state | (entity, key, default) | — | Restaura a valor por defecto |

---

### 3. MEMORY — variables, pilas, colecciones

**3a. Variables simples**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 40 | set_var | (name, value) | — | Variable del programa |
| 41 | get_var | (name) | Value | Lee variable |
| 42 | del_var | (name) | — | Elimina variable |
| 43 | var_exists | (name) | Bool | Verifica existencia |
| 44 | inc_var | (name, delta?) | — | Incrementa numérica |
| 45 | dec_var | (name, delta?) | — | Decrementa numérica |

**3b. Pilas (stack)**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 46 | stack_push | (name, value) | — | Apila valor |
| 47 | stack_pop | (name) | Value | Desapila y retorna |
| 48 | stack_peek | (name) | Value | Lee tope sin desapilar |
| 49 | stack_size | (name) | Nat | Tamaño de la pila |
| 50 | stack_clear | (name) | — | Vacía la pila |

**3c. Colas (queue)**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 51 | queue_push | (name, value) | — | Encola al final |
| 52 | queue_pop | (name) | Value | Desencola del frente |
| 53 | queue_peek | (name) | Value | Lee frente |
| 54 | queue_size | (name) | Nat | Tamaño de la cola |

**3d. Listas**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 55 | list_create | (name) | — | Crea lista vacía |
| 56 | list_append | (name, value) | — | Agrega al final |
| 57 | list_prepend | (name, value) | — | Agrega al inicio |
| 58 | list_get | (name, index) | Value | Por índice |
| 59 | list_set | (name, index, value) | — | Asigna por índice |
| 60 | list_remove | (name, index) | — | Elimina por índice |
| 61 | list_contains | (name, value) | Bool | Verifica pertenencia |
| 62 | list_size | (name) | Nat | Longitud |
| 63 | list_clear | (name) | — | Vacía la lista |
| 64 | list_find | (name, value) | Int? | Índice o null |
| 65 | list_sort | (name, comparator?) | — | Ordena in-place |
| 66 | list_reverse | (name) | — | Invierte in-place |
| 67 | list_slice | (name, start, end) | List | Sublista |
| 68 | list_concat | (a, b) | List | Concatena dos listas |
| 69 | list_map | (name, transform) | — | Aplica transform |
| 70 | list_filter | (name, predicate) | — | Filtra por predicado |
| 71 | list_reduce | (name, accumulator, init) | Value | Reduce a un valor |

**3e. Mapas**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 72 | map_create | (name) | — | Crea mapa vacío |
| 73 | map_set | (name, key, value) | — | Asigna par clave-valor |
| 74 | map_get | (name, key) | Value? | Por clave |
| 75 | map_has | (name, key) | Bool | Verifica clave |
| 76 | map_remove | (name, key) | — | Elimina par |
| 77 | map_keys | (name) | List | Todas las claves |
| 78 | map_values | (name) | List | Todos los valores |
| 79 | map_size | (name) | Nat | Cantidad de pares |
| 80 | map_clear | (name) | — | Vacía el mapa |

**3f. Variables globales**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 81 | global_set | (name, value) | — | Accesible por todas las entities |
| 82 | global_get | (name) | Value | Lee global |
| 83 | global_inc | (name, delta?) | — | Incrementa global |
| 84 | global_dec | (name, delta?) | — | Decrementa global |

---

### 4. RESOURCE — HP, mana, gold, stacks, charges

**4a. Operaciones básicas**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 85 | spend | (entity, resource, amount) | Bool | Consume; false si insuficiente |
| 86 | force_spend | (entity, resource, amount) | Bool | Consume aunque quede negativo |
| 87 | gain | (entity, resource, amount) | — | Añade (respeta max) |
| 88 | force_gain | (entity, resource, amount) | — | Añade ignorando max |
| 89 | set_resource | (entity, resource, value) | — | Asigna valor exacto |
| 90 | init_resource | (entity, resource, value) | — | Solo si no existía |
| 91 | spend_pct | (entity, resource, pct) | Bool | Consume porcentaje del actual |
| 92 | gain_pct | (entity, resource, pct) | — | Añade porcentaje del max |

**4b. Regeneración**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 93 | set_regen | (entity, resource, rate_per_tick) | — | Fija regeneración/tick |
| 94 | add_regen | (entity, resource, extra_rate) | — | Añade regen temporal |
| 95 | remove_regen | (entity, resource, extra_rate) | — | Quita regen temporal |
| 96 | regen_now | (entity, resource) | — | Fuerza regen instantánea |
| 97 | drain_regen | (entity, resource, dur) | — | Niega regen por duración |

**4c. Transferencia / conversión**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 98 | transfer | (from, to, resource, amount) | — | Transfiere recurso |
| 99 | transfer_pct | (from, to, resource, pct) | — | Transfiere porcentaje |
| 100 | convert | (entity, from_res, to_res, rate) | — | Convierte un recurso a otro |
| 101 | share_resource | (entity, resource, allies, pct) | — | Distribuye entre aliados |

**4d. Consulta**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 102 | get_resource | (entity, resource) | Int | Valor actual |
| 103 | get_resource_max | (entity, resource) | Int | Máximo |
| 104 | get_resource_pct | (entity, resource) | Float | Porcentaje actual/max |
| 105 | get_regen | (entity, resource) | Int | Tasa regeneración/tick |
| 106 | has_enough | (entity, resource, amount) | Bool | Verifica suficiente |
| 107 | is_empty | (entity, resource) | Bool | Recurso == 0 |
| 108 | is_full | (entity, resource) | Bool | Recurso == max |

**4e. Límites**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 109 | set_max | (entity, resource, max) | — | Fija el máximo |
| 110 | add_max | (entity, resource, delta) | — | Modifica el máximo |
| 111 | clamp_resource | (entity, resource, min, max) | — | Limita al rango |
| 112 | overflow | (entity, resource) | Int | Cuánto excede el máximo |

---

## [B] ESPACIO-TIEMPO & EVENTOS

---

### 5. SPACE — posición, distancia, movimiento, AoE

**5a. Posición**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 113 | set_pos | (entity, x, y) | — | Asigna posición |
| 114 | get_pos | (entity) | Pos | Obtiene posición (x, y) |
| 115 | get_x | (entity) | Int | Componente x |
| 116 | get_y | (entity) | Int | Componente y |
| 117 | get_spawn_pos | (entity) | Pos | Posición de spawn |
| 118 | set_spawn_pos | (entity, x, y) | — | Cambia punto de respawn |
| 119 | pos_eq | (a, b) | Bool | Misma posición exacta |

**5b. Movimiento discreto**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 120 | move_to | (entity, x, y) | — | Mueve instantáneamente |
| 121 | move_by | (entity, dx, dy) | — | Desplazamiento relativo |
| 122 | move_toward | (entity, target, steps) | Bool | Avanza; retorna si llegó |
| 123 | move_away | (entity, threat, steps) | — | Se aleja |
| 124 | teleport | (entity, x, y) | — | Instantáneo sin trayectoria |
| 125 | swap_pos | (a, b) | — | Intercambia posiciones |
| 126 | face | (entity, target) | — | Orientación hacia target |

**5c. Movimiento continuo / programado**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 127 | dash | (entity, x, y, speed) | — | Rápido hacia punto |
| 128 | dash_entity | (entity, target, speed) | — | Dash hacia entity |
| 129 | dash_dir | (entity, dx, dy, dist, speed) | — | Dash en dirección relativa |
| 130 | knockback | (target, from, dist, speed?) | — | Empuje away de origen |
| 131 | pull_to | (target, to, dist, speed?) | — | Atracción hacia punto |
| 132 | push_from | (target, source, dist, speed?) | — | Repulsión desde punto |
| 133 | fling | (target, from, dist, dir) | — | Empuje violento |
| 134 | chain_link | (a, b, max_dist, dur) | — | Mantiene a distancia máxima |
| 135 | leash | (target, anchor, max_dist, dur) | — | No puede alejarse |
| 136 | stop_move | (entity) | — | Detiene movimiento |
| 137 | set_speed | (entity, speed) | — | Modifica velocidad |
| 138 | get_speed | (entity) | Float | Velocidad actual |
| 139 | freeze_pos | (entity, dur) | — | Impide cambio de posición |
| 140 | unfreeze_pos | (entity) | — | Permite movimiento |

**5d. Distancia / rango**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 141 | distance | (a, b) | Int | Manhattan/euclidiana (decidir) |
| 142 | distance_x | (a, b) | Int | Distancia en eje x |
| 143 | distance_y | (a, b) | Int | Distancia en eje y |
| 144 | in_range | (source, target, range) | Bool | Distancia <= range |
| 145 | in_range_of_point | (entity, x, y, range) | Bool | Dentro de rango de punto |
| 146 | out_of_range | (source, target, range) | Bool | Distancia > range |
| 147 | get_direction | (source, target) | (dx,dy) | Vector normalizado |
| 148 | manhattan | (a, b) | Int | Distancia Manhattan |
| 149 | euclidean | (a, b) | Float | Distancia euclidiana |

**5e. Áreas (AoE)**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 150 | in_area | (center, radius, point) | Bool | Punto dentro de área circular |
| 151 | in_rect | (center, w, h, point) | Bool | Dentro de rectángulo |
| 152 | in_cone | (origin, dir, angle, range, point) | Bool | Dentro de cono |
| 153 | in_line | (p1, p2, width, point) | Bool | Dentro de línea con grosor |
| 154 | in_diamond | (center, radius, point) | Bool | Dentro de rombo |

**5f. Formas de área**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 155 | area_circle | (center, radius) | Area | Define circular |
| 156 | area_rect | (x, y, w, h) | Area | Define rectángulo |
| 157 | area_cone | (origin, dir, angle, range) | Area | Define cono |
| 158 | area_line | (p1, p2, width) | Area | Define línea con grosor |
| 159 | area_diamond | (center, radius) | Area | Define rombo |
| 160 | area_union | (a, b) | Area | Unión |
| 161 | area_intersect | (a, b) | Area | Intersección |
| 162 | area_difference | (a, b) | Area | Resta |
| 163 | area_inverse | (area, bounds) | Area | Inversión |

**5g. Colisión / rayo**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 164 | line_cast | (from, to, filter?) | Entity? | Primera entity en línea |
| 165 | ray_cast | (from, dir, max_dist, filter?) | Entity? | Rayo hasta max_dist |
| 166 | area_cast | (center, radius, filter?) | [Entity] | Todas en área |
| 167 | cone_cast | (origin, dir, angle, range, filter?) | [Entity] | Todas en cono |
| 168 | overlap | (entity, area) | Bool | Hitbox toca el área |

**5h. Detección espacial**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 169 | nearest | (origin, filter?) | Entity? | Más cercana con filtro |
| 170 | furthest | (origin, filter?) | Entity? | Más lejana con filtro |
| 171 | nearest_enemy | (entity) | Entity? | Enemigo más cercano |
| 172 | nearest_ally | (entity) | Entity? | Aliado más cercano |
| 173 | lowest_hp | (origin, filter?) | Entity? | Menor HP en área |
| 174 | highest_hp | (origin, filter?) | Entity? | Mayor HP en área |
| 175 | random_enemy | (entity) | Entity? | Enemigo aleatorio |
| 176 | random_point_in | (area) | Pos | Punto aleatorio en área |

---

### 6. TIME — scheduling, duration, periódicos

**6a. Scheduling**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 177 | schedule | (effect, tick) | EventId | Programa en tick futuro |
| 178 | schedule_entity | (entity, effect, tick) | EventId | Efecto de entity en tick |
| 179 | cancel_schedule | (event_id) | — | Cancela programado |
| 180 | reschedule | (event_id, new_tick) | — | Reprograma |
| 181 | now | — | Nat | Tick actual |

**6b. Duración**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 182 | set_duration | (modifier, ticks) | — | Fija duración |
| 183 | get_remaining | (modifier) | Int | Ticks restantes (-1=infinito) |
| 184 | extend | (modifier, extra) | — | Extiende |
| 185 | reduce | (modifier, less) | — | Reduce (mínimo 0) |
| 186 | expire_now | (modifier) | — | Expira inmediatamente |
| 187 | is_expired | (modifier) | Bool | Verifica expiración |

**6c. Periódicos**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 188 | periodic | (effect, every, times?) | EventId | Repite cada N ticks |
| 189 | periodic_entity | (entity, effect, every, times?) | EventId | Periódico ligado a entity |
| 190 | cancel_periodic | (event_id) | — | Detiene periódico |
| 191 | times_remaining | (periodic_id) | Nat? | Repeticiones restantes |

**6d. Control de tiempo**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 192 | advance | — | — | Avanza reloj +1 |
| 193 | pause_global | — | — | Pausa todo |
| 194 | resume_global | — | — | Reanuda |
| 195 | freeze_entity_time | (entity) | — | Congela entity |
| 196 | unfreeze_entity_time | (entity) | — | Descongela |
| 197 | set_timescale | (entity, factor) | — | Acelera/desacelera |
| 198 | time_elapsed | (entity, modifier?) | Nat | Tiempo activo de modifier |
| 199 | ticks_since | (event_id) | Nat | Ticks desde evento |

---

### 7. EVENT — emisión, suscripción, consumo, routing

**7a. Emisión**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 200 | emit | (type, source?, target?, payload) | EventId | Emite evento |
| 201 | emit_delayed | (type, ticks, source?, target?, payload) | EventId | Emite tras N ticks |
| 202 | emit_periodic | (type, every, source?, target?, payload) | EventId | Emite periódicamente |
| 203 | reemit | (original_event, overrides?) | EventId | Reemite con modificaciones |

**7b. Suscripción**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 204 | on | (event_type, effect, condition?) | — | Registra handler |
| 205 | on_entity | (entity, event_type, effect, cond?) | — | Handler de entity |
| 206 | on_once | (event_type, effect, cond?) | — | Handler que se consume |
| 207 | off | (event_type, handler_id) | — | Remueve handler |
| 208 | off_all | (event_type) | — | Remueve todos de un tipo |
| 209 | off_entity | (entity) | — | Remueve todos de una entity |

**7c. Consumo**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 210 | consume_event | (event) | — | Marca como manejado |
| 211 | is_consumed | (event) | Bool | Fue manejado |
| 212 | block_event | (event_type, entity?) | — | Bloquea tipo de evento |
| 213 | unblock_event | (event_type, entity?) | — | Desbloquea |
| 214 | is_blocked | (event_type, entity?) | Bool | Verifica bloqueo |

**7d. Routing**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 215 | forward_event | (event, new_target) | — | Redirige a otra entity |
| 216 | broadcast | (type, source?, payload) | — | Emite a todas las entities |
| 217 | multicast | (type, targets, payload) | — | Emite a lista de targets |
| 218 | mirror_event | (event, mirror_source) | — | Reemite como otra fuente |
| 219 | suppress_event | (entity, event_type, dur) | — | Suprime por tiempo |

**7e. Consulta**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 220 | last_event | (type?) | Event? | Último evento de tipo |
| 221 | event_count | (type?) | Nat | Total de eventos de tipo |
| 222 | events_since | (type, tick) | [Event] | Eventos desde tick |
| 223 | has_event_pending | (type, entity?) | Bool | Hay en la cola |
| 224 | peek_next_event | () | Event? | Siguiente sin sacar |

---

### 8. PROJECTILE — entidades viajeras

**8a. Creación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 225 | spawn_projectile | (source, target, speed, payload, tags?) | EntityId | Viaja hacia target |
| 226 | spawn_ground | (center, radius, payload, delay?) | EntityId | Impacta área en punto |
| 227 | spawn_line | (from, to, width, speed, payload) | EntityId | Viaja en línea recta |
| 228 | spawn_homing | (source, target, speed, payload) | EntityId | Sigue al target |
| 229 | spawn_bouncing | (source, target, speed, payload, jumps) | EntityId | Rebota entre targets |
| 230 | spawn_chaining | (source, target, speed, payload, jumps) | EntityId | Encadena en secuencia |
| 231 | spawn_area | (center, speed, radius, payload) | EntityId | Área que se mueve |
| 232 | spawn_orbital | (source, radius, speed, payload) | EntityId | Orbita alrededor de source |

**8b. Movimiento**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 233 | redirect_projectile | (projectile, new_target) | — | Cambia dirección |
| 234 | accelerate | (projectile, new_speed) | — | Cambia velocidad |
| 235 | pause_projectile | (projectile) | — | Detiene temporalmente |
| 236 | resume_projectile | (projectile) | — | Reanuda |
| 237 | curve_projectile | (projectile, control_point) | — | Curva de Bezier |

**8c. Impacto**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 238 | on_hit | (projectile, effect) | — | Handler al impactar |
| 239 | on_miss | (projectile, effect) | — | Handler al fallar |
| 240 | on_expire | (projectile, effect) | — | Handler al expirar |
| 241 | on_hit_area | (projectile, area, effect) | — | Impacta área |
| 242 | on_first_hit | (projectile, effect) | — | Primer impacto |

**8d. Consulta**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 243 | projectile_alive | (projectile) | Bool | Proyectil activo |
| 244 | projectile_pos | (projectile) | Pos | Posición actual |
| 245 | projectile_dir | (projectile) | (dx,dy) | Dirección actual |
| 246 | projectile_dist | (projectile, point) | Int | Distancia al proyectil |
| 247 | destroy_projectile | (projectile) | — | Destruye sin efecto |

---

## [C] MODIFICACIÓN & CONTROL

---

### 9. MODIFIER — ciclo de vida de buffs/debuffs

**9a. Creación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 248 | apply_modifier | (source, target, type, dur, stacks?) | ModifierId | Aplica buff/debuff |
| 249 | apply_aura | (source, type, radius, dur, effect) | ModifierId | Afecta entities en área |
| 250 | apply_persistent | (source, target, type) | ModifierId | Sin expiración |
| 251 | apply_untargetable | (entity, dur) | ModifierId | No puede ser target |

**9b. Manipulación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 252 | refresh_modifier | (modifier) | — | Reinicia duración |
| 253 | extend_modifier | (modifier, extra) | — | Extiende duración |
| 254 | reduce_modifier | (modifier, less) | — | Reduce duración |
| 255 | add_stack | (modifier, amount?) | — | Añade stacks (+1 default) |
| 256 | remove_stack | (modifier, amount?) | — | Quita stacks |
| 257 | set_stacks | (modifier, n) | — | Fija stacks |
| 258 | transfer_modifier | (modifier, new_target) | — | Mueve a otra entity |
| 259 | replace_modifier | (entity, old_type, new_type, dur) | — | Sustituye |
| 260 | merge_modifiers | (mod_a, mod_b) | — | Combina mismo tipo |

**9c. Remoción**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 261 | remove_modifier | (modifier) | — | Remueve específico |
| 262 | remove_by_type | (entity, type) | — | Remueve todos de un tipo |
| 263 | remove_by_source | (entity, source_id) | — | Remueve todos de una fuente |
| 264 | remove_all | (entity) | — | Todos los modifiers |
| 265 | remove_all_debuffs | (entity) | — | Solo debuffs |
| 266 | remove_all_buffs | (entity) | — | Solo buffs |
| 267 | purge | (entity, source) | — | Buffs de enemy, debuffs de ally |
| 268 | unsummon_auras | (entity) | — | Remueve auras persistentes |

**9d. Consulta**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 269 | has_modifier | (entity, type) | Bool | Tiene modifier de tipo |
| 270 | get_modifier | (entity, type) | Modifier? | Primer modifier de tipo |
| 271 | get_all_modifiers | (entity) | [Modifier] | Todos |
| 272 | modifier_count | (entity, type?) | Nat | Cantidad |
| 273 | modifier_stacks | (entity, type) | Nat | Stacks |
| 274 | modifier_duration | (entity, type) | Int | Duración restante |
| 275 | is_buff | (modifier) | Bool | Es buff |
| 276 | is_debuff | (modifier) | Bool | Es debuff |

**9e. Propiedades**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 277 | set_undispellable | (modifier) | — | No puede ser dispelleado |
| 278 | set_hidden | (modifier) | — | No visible en UI |
| 279 | set_stacks_max | (modifier, max) | — | Límite de stacks |
| 280 | set_severity | (modifier, level) | — | basic/strong/hard |
| 281 | set_gate | (modifier, action_types) | — | Acciones que bloquea |

---

### 10. CONTROL — gating de acciones (stun/root/silence family)

**10a. Stun**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 282 | stun | (target, dur) | — | Paraliza: no puede actuar |
| 283 | stun_if | (target, dur, cond) | — | Stun condicional |
| 284 | stun_chain | (target, dur, next_target) | — | Salta al siguiente al expirar |

**10b. Root**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 285 | root | (target, dur) | — | No mueve, sí casthea |
| 286 | root_if | (target, dur, cond) | — | Root condicional |

**10c. Silence**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 287 | silence | (target, dur) | — | No casthea, sí mueve |
| 288 | silence_if | (target, dur, cond) | — | Silence condicional |
| 289 | spell_lock | (target, dur, ability?) | — | Bloquea habilidad específica |

**10d. Slow / Haste**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 290 | slow | (target, dur, factor%) | — | Reduce velocidad % |
| 291 | slow_flat | (target, dur, amount) | — | Reduce velocidad fija |
| 292 | haste | (target, dur, factor%) | — | Aumenta velocidad % |
| 293 | haste_flat | (target, dur, amount) | — | Aumenta velocidad fija |
| 294 | set_speed_mult | (target, dur, mult) | — | Multiplicador de velocidad |
| 295 | min_speed | (target, min) | — | Velocidad mínima |
| 296 | max_speed | (target, max) | — | Velocidad máxima |

**10e. Disarm**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 297 | disarm | (target, dur) | — | No puede atacar |
| 298 | disarm_if | (target, dur, cond) | — | Disarm condicional |
| 299 | attack_lock | (target, dur, attack_type?) | — | Bloquea tipo de ataque |

**10f. Taunt / Fear / Charm**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 300 | taunt | (target, source, dur) | — | Obliga a atacar source |
| 301 | fear | (target, away_from, dur) | — | Huye de entity/punto |
| 302 | fear_point | (target, point, dur) | — | Huye de punto específico |
| 303 | charm | (target, source, dur) | — | Aliado temporal que ataca aliados |
| 304 | mesmerize | (target, dur) | — | Confusión: actúa aleatoriamente |

**10g. Sleep / Stasis**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 305 | sleep | (target, dur) | — | Dormido: despierta con daño |
| 306 | stasis | (target, dur) | — | Fuera del mundo |
| 307 | invulnerable | (target, dur) | — | No recibe daño, puede actuar |
| 308 | ethereal | (target, dur) | — | Solo daño mágico, no ataca |
| 309 | ghost | (target, dur) | — | No ataca ni es atacado físicamente |

**10h. Hex / Break / Mute**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 310 | hex | (target, dur) | — | Forma débil, pierde habilidades |
| 311 | break | (target, dur) | — | Desactiva pasivas |
| 312 | mute | (target, dur) | — | No puede usar items activos |

**10i. Suppression / Leash**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 313 | suppress | (target, dur) | — | Stun no dispelleable |
| 314 | leash_point | (target, point, max_dist, dur) | — | No alejarse de punto |
| 315 | blind | (target, dur, miss_pct) | — | % de ataques que fallan |

**10j. Genérico**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 316 | gate | (target, action_types, dur) | — | Bloquea categorías genéricas |
| 317 | ungated | (target, action_type) | — | Desbloquea categoría |
| 318 | ungated_all | (target) | — | Desbloquea todo |
| 319 | is_gated | (target, action_type) | Bool | Verifica bloqueo |
| 320 | get_gates | (target) | [Type] | Lista bloqueadas |
| 321 | interrupt | (target) | — | Detiene canal/acción en curso |
| 322 | interrupt_channel | (target) | — | Interrumpe solo canal |
| 323 | stagger | (target, dur_per_stack, max) | — | Stun que escala con stacks |

---

### 11. DISPEL — remoción de modifiers

**11a. Dispel básico**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 324 | dispel_basic | (target) | — | Remueve básicos |
| 325 | dispel_basic_enemy | (target) | — | Remueve buffs |
| 326 | dispel_basic_ally | (target) | — | Remueve debuffs |

**11b. Dispel fuerte**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 327 | dispel_strong | (target) | — | Remueve más tipos |
| 328 | purge_strong | (target, source) | — | Purge fuerte con fuente |

**11c. Dispel total**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 329 | dispel_hard | (target) | — | Remueve todo excepto undispellable |
| 330 | dispel_all | (target) | — | Remueve absolutamente todo |
| 331 | banish | (target, dur) | — | Dispara modifiers temporalmente |

**11d. Dispel genérico**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 332 | dispel | (target, severity) | — | Con nivel de severidad |
| 333 | dispel_by_type | (target, modifier_type) | — | Solo un tipo específico |
| 334 | dispel_by_source | (target, source_id) | — | Todos de una fuente |
| 335 | dispel_by_predicate | (target, predicate) | — | Los que cumplen condición |
| 336 | self_dispel | (entity) | — | Auto-limpia |

---

### 12. AURA — modificadores persistentes de área

**12a. Creación / destrucción**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 337 | create_aura | (source, type, radius, effect) | AuraId | Crea aura en radio |
| 338 | destroy_aura | (aura) | — | Destruye aura |
| 339 | destroy_all_auras | (source) | — | Todas las de una entity |

**12b. Efectos de aura**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 340 | on_enter_aura | (aura, effect) | — | Al entrar al radio |
| 341 | on_exit_aura | (aura, effect) | — | Al salir del radio |
| 342 | while_in_aura | (aura, effect_per_tick) | — | Recurrente mientras está |
| 343 | aura_affects_enemies | (aura) | — | Configura para enemigos |
| 344 | aura_affects_allies | (aura) | — | Configura para aliados |

**12c. Consulta**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 345 | in_aura | (entity, aura) | Bool | Está dentro del radio |
| 346 | get_aura_source | (aura) | EntityId | Fuente |
| 347 | auras_of | (entity) | [Aura] | Auras que le afectan |
| 348 | aura_targets | (aura) | [Entity] | Entities afectadas |
| 349 | aura_radius | (aura) | Int | Radio |

---

### 13. SHIELD — capas de absorción

**13a. Creación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 350 | shield | (target, amount, dur?) | ModifierId | Absorbe hasta agotar/expirar |
| 351 | magic_shield | (target, amount, dur?) | ModifierId | Solo mágico |
| 352 | physical_shield | (target, amount, dur?) | ModifierId | Solo físico |
| 353 | spell_shield | (target, charges) | ModifierId | Absorbe N hechizos (Linken) |
| 354 | barrier_point | (center, radius, dur) | ModifierId | Bloquea proyectiles en área |

**13b. Absorción**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 355 | absorb_damage | (shield, raw_damage) | Int | Daño restante tras absorber |
| 356 | absorb_spell | (shield, event) | Bool | Niega hechizo |
| 357 | break_shield | (shield) | — | Rompe inmediatamente |
| 358 | refresh_shield | (shield) | — | Restaura HP del shield |
| 359 | add_shield | (shield, extra) | — | Añade más HP |

**13c. Consulta**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 360 | get_shield | (entity, type?) | Int | HP restante |
| 361 | has_shield | (entity, type?) | Bool | Tiene shield activo |
| 362 | shield_pct | (entity, type?) | Float | Porcentaje HP shield |

---

### 14. REFLECT — redirección de daño/eventos

**14a. Reflejo**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 363 | reflect_damage | (target, pct, source?) | — | Refleja % del daño recibido |
| 364 | reflect_spell | (target, pct) | — | Refleja % de hechizos |
| 365 | reflect_exact | (target, pct) | — | Reflejo exacto |
| 366 | return_damage | (target, amount, type) | — | Retorna daño fijo al recibir |

**14b. Redirección**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 367 | redirect_damage | (target, pct, to) | — | Redirige daño a otra entity |
| 368 | redirect_spell | (target, pct, to) | — | Redirige hechizos |
| 369 | redirect_event | (target, event_type, to) | — | Redirige eventos |

**14c. Enlace**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 370 | damage_link | (a, b, pct) | — | Comparten % del daño |
| 371 | damage_share | (target, to, pct) | — | Unidireccional |
| 372 | damage_steal | (target, source, pct) | — | Absorbe % del daño |

---

### 15. VISION — revelar/ocultar

**15a. Visibilidad**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 373 | reveal | (entity, dur?) | — | Hace visible |
| 374 | hide | (entity, dur) | — | Hace invisible |
| 375 | camouflage | (entity, dur) | — | Se rompe al atacar/castear |
| 376 | phase | (entity, dur) | — | Pasa a través, no target |
| 377 | break_invisibility | (entity) | — | Rompe invisibilidad |
| 378 | true_sight | (entity, dur?) | — | Revela invisibles |
| 379 | has_vision_of | (observer, target) | Bool | Puede ver al target |
| 380 | is_visible | (entity) | Bool | Es visible |

**15b. Ward**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 381 | place_ward | (owner, x, y, type, dur, vision_radius) | EntityId | Ward con visión de área |
| 382 | destroy_ward | (ward) | — | Destruye ward |
| 383 | wards_count | (owner, type?) | Nat | Wards activos |

**15c. Detección**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 384 | detect | (detector, target) | Bool | Detecta invisible en radio |
| 385 | scan | (center, radius) | [Entity] | Lista entities incluyendo invisibles |

---

## [D] COMBATE & DAÑO

---

### 16. DAMAGE — reducción de HP con mitigación

**16a. Daño directo**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 386 | damage | (target, amount, type?) | Int | Con mitigación; retorna restante |
| 387 | damage_pure | (target, amount) | Int | Sin mitigación |
| 388 | damage_type | (target, amount, damage_type) | Int | Con tipo explícito |
| 389 | damage_true | (target, amount) | Int | Ignora todo mitigación/evasion |
| 390 | instant_kill | (target) | — | Mata inmediatamente |

**16b. Daño de área**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 391 | damage_area | (center, radius, amount, type?) | — | Circular |
| 392 | damage_area_square | (center, half_size, amount, type?) | — | Cuadrada |
| 393 | damage_cone | (origin, dir, angle, range, amount, type?) | — | Cono |
| 394 | damage_line | (from, to, width, amount, type?) | — | Línea |
| 395 | damage_around_entity | (entity, radius, amount, type?) | — | Alrededor de entity |

**16c. Daño en tiempo**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 396 | dot | (target, dur, total_damage, type?) | — | Distribuido cada tick |
| 397 | dot_volatile | (target, dur, dps, type?) | — | Puede ser purgado |
| 398 | dot_persistent | (target, dps, type?) | — | Sin duración |
| 399 | bleed | (target, dur, damage_per_stack, type?) | — | Escala con stacks |
| 400 | cancel_dot | (target, type?) | — | Cancela DOT activo |

**16d. Daño crítico**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 401 | critical | (target, base, multiplier, type?) | Int | Con multiplicador |
| 402 | crit_chance | (entity, chance_pct, multiplier) | — | Probabilidad de crítico |
| 403 | guaranteed_crit | (entity, dur, multiplier) | — | Siguiente ataque crítico seguro |

**16e. Daño con lifesteal**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 404 | damage_lifesteal | (source, target, amount, lifesteal_pct) | Int | Cura al source |
| 405 | spell_lifesteal | (source, target, amount, pct) | Int | Lifesteal de hechizos |
| 406 | set_lifesteal | (entity, pct, dur?) | — | Configura temporal |

**16f. Mitigación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 407 | set_armor | (entity, armor, dur?) | — | Fija armadura |
| 408 | add_armor | (entity, delta, dur?) | — | Modifica armadura |
| 409 | set_magic_resist | (entity, pct, dur?) | — | Fija resistencia mágica |
| 410 | add_magic_resist | (entity, delta, dur?) | — | Modifica resistencia |
| 411 | damage_reduction | (entity, pct, type?, dur?) | — | Reducción por % |
| 412 | damage_block | (entity, flat_amount) | — | Bloquea daño plano |
| 413 | evasion | (entity, pct, dur?) | — | Probabilidad de evadir |
| 414 | set_evasion | (entity, pct) | — | Fija evasion |
| 415 | true_strike | (entity, dur?) | — | Ignora evasion |
| 416 | damage_immune | (entity, dur) | — | Inmunidad total |

**16g. Amplificación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 417 | amplify_damage | (target, pct, type?, dur?) | — | Amplifica daño recibido |
| 418 | amplify_spell_out | (entity, pct, dur?) | — | Amplifica daño saliente |
| 419 | weaken | (target, pct, dur?) | — | Reduce daño infligido |

**16h. Tipos de daño**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 420 | MAGIC | — | Enum | Daño mágico |
| 421 | PHYSICAL | — | Enum | Daño físico |
| 422 | PURE | — | Enum | Daño puro |
| 423 | COMPOSITE | — | Enum | Half+half |

**16i. Muerte por daño**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 424 | overkill | (target, excess_damage) | — | Daño que excedió HP |
| 425 | last_hit | (entity) | EntityId? | Último que dañó |
| 426 | deny_kill | (target, denier) | — | Aliado mata aliado |
| 427 | execute | (target) | — | Matar sin kill credit |

---

### 17. HEAL — restauración de HP

**17a. Curación directa**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 428 | heal | (target, amount) | Int | Restaura HP; retorna sobrante |
| 429 | heal_pct | (target, pct) | — | Porcentaje de max_hp |
| 430 | heal_minimum | (target, min) | — | Mínima garantizada |

**17b. Curación de área**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 431 | heal_area | (center, radius, amount) | — | Cura aliados en área |
| 432 | heal_line | (from, to, width, amount) | — | Cura en línea |
| 433 | heal_around | (entity, radius, amount) | — | Cura alrededor |

**17c. Curación en tiempo**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 434 | hot | (target, dur, total_heal) | — | Distribuida cada tick |
| 435 | hot_rejuvenation | (target, dur, hot_per_tick, burst) | — | HOT + burst al expirar |
| 436 | cancel_hot | (target, type?) | — | Cancela HOT |

**17d. Restauración de recursos**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 437 | restore_mana | (target, amount) | — | Restaura mana |
| 438 | restore_mana_pct | (target, pct) | — | % de max_mana |
| 439 | restore_all | (entity) | — | HP y mana al máximo |
| 440 | fountain_regen | (entity, dur) | — | Regen extremo (base) |

**17e. Restauración total**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 441 | full_restore | (entity) | — | HP=max, mana=max, cleanse |
| 442 | revive_to | (entity, hp_pct) | — | Revive con % HP |

---

### 18. DEATH — lifecycle terminal

**18a. Matar**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 443 | kill | (target, source?) | — | Mata con fuente opcional |
| 444 | suicide | (entity) | — | Se mata a sí mismo |
| 445 | execute_if | (target, condition, source?) | — | Mata si cumple condición |
| 446 | execute_below | (target, hp_pct, source?) | — | Mata si HP < %max |

**18b. Prevenir muerte**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 447 | prevent_death | (entity, dur) | — | Próxima muerte se queda en 1 |
| 448 | cull | (entity, max_hp_pct) | — | Mata si HP <= max_hp*pct |
| 449 | shallow_grave | (entity, dur) | — | Imposible morir por daño |
| 450 | second_wind | (entity, dur) | — | Daño letal cura en vez de matar |

**18c. Estado muerto**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 451 | is_dead | (entity) | Bool | Verifica muerte |
| 452 | get_killer | (entity) | EntityId? | Quién la mató |
| 453 | get_time_since_death | (entity) | Nat | Ticks desde muerte |
| 454 | get_death_cause | (entity) | String? | Tipo de evento letal |
| 455 | death_mark | (entity, dur) | — | Al morir, buff al asesino |

**18d. Muerte forzada**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 456 | execute_ward | (ward) | — | Destruye ward |
| 457 | kill_summon | (summon) | — | Destruye summon sin reward |
| 458 | banish_entity | (entity) | — | Retira sin ON_DEATH |
| 459 | soul_release | (entity) | — | Matar con liberación de alma |

---

### 19. RESPAWN — revivir

**19a. Respawn básico**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 460 | respawn | (entity, delay?) | — | Revive con HP/mana full en spawn |
| 461 | respawn_at | (entity, x, y, delay?) | — | Revive en posición |
| 462 | respawn_immediate | (entity) | — | Revive inmediatamente |
| 463 | revive | (entity, hp_pct) | — | Revive con % HP |

**19b. Buyback**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 464 | buyback | (entity) | — | Revive pagando oro |
| 465 | can_buyback | (entity) | Bool | Puede y tiene oro |
| 466 | buyback_cost | (entity) | Int | Costo |
| 467 | set_buyback_cooldown | (entity, dur) | — | Enfria buyback |

**19c. Consulta**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 468 | get_respawn_time | (entity) | Nat | Ticks hasta respawn |
| 469 | set_respawn_time | (entity, ticks) | — | Modifica tiempo |
| 470 | get_respawn_point | (entity) | Pos | Punto de respawn |
| 471 | add_respawn_time | (entity, delta) | — | Añade/quita tiempo |

---

### 20. CAST — pipeline de invocación de habilidad

**20a. Invocación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 472 | cast | (ability, source, target?) | — | Ejecuta sobre target |
| 473 | cast_point | (ability, source, x, y) | — | Hacia punto |
| 474 | cast_self | (ability, source) | — | Sobre sí mismo |
| 475 | cast_no_target | (ability, source) | — | Sin objetivo |
| 476 | cast_aoe | (ability, source, center, radius) | — | De área |
| 477 | cast_chained | (ability, source, target, jumps) | — | Efecto encadenante |
| 478 | cast_bouncing | (ability, source, target, jumps) | — | Efecto rebote |

**20b. Canal**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 479 | channel | (ability, source, target, dur) | — | Canaliza por duración |
| 480 | channel_tick | (ability, source, dur, effect_per_tick) | — | Con efecto cada tick |
| 481 | channel_breakable | (ability, source, target, dur) | — | Se rompe con stun |
| 482 | channel_unbreakable | (ability, source, target, dur) | — | Ignora interrupciones |
| 483 | is_channeling | (entity) | Bool | Verifica si canaliza |
| 484 | get_channel_time | (entity) | Nat | Ticks restantes |
| 485 | get_channel_target | (entity) | Entity? | Target del canal |

**20c. Cancelación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 486 | cancel_cast | (ability, source) | — | Cancela en curso |
| 487 | cancel_all_casts | (entity) | — | Cancela todas |
| 488 | interrupt_cast | (entity) | — | Interrumpe por fuerza externa |
| 489 | purge_cast | (entity) | — | Remueve estado de casteo |

**20d. Robo / reflect**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 490 | steal_ability | (source, target, ability?) | — | Copia habilidad (Rubick) |
| 491 | steal_random | (source, target) | — | Copia aleatoria |
| 492 | reflect_cast | (target, pct, source?) | — | Refleja hechizo |
| 493 | copy_cast | (target, ability, source, params) | — | Copia y ejecuta en otro |

**20e. Nivel de habilidad**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 494 | learn_ability | (entity, ability) | — | Aprende |
| 495 | upgrade_ability | (entity, ability) | — | Sube nivel |
| 496 | set_ability_level | (entity, ability, level) | — | Fija nivel |
| 497 | get_ability_level | (entity, ability) | Nat | Nivel actual |
| 498 | reset_cooldown | (entity, ability?) | — | Resetea cooldown |
| 499 | charge_cast | (entity, ability) | — | Usa un charge |
| 500 | get_charges | (entity, ability) | Nat | Charges restantes |

---

### 21. TARGET — resolución de objetivo

**21a. Target estático**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 501 | target_self | — | Entity | El caster |
| 502 | target_entity | (entity_id) | Entity | Entity específica |
| 503 | target_point | (x, y) | Pos | Punto |
| 504 | target_last_point | — | Pos | Último punto usado |
| 505 | target_last_cast | (source) | Entity? | Target última habilidad |

**21b. Target dinámico**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 506 | target_nearest_enemy | (source) | Entity? | Enemigo más cercano |
| 507 | target_nearest_ally | (source) | Entity? | Aliado más cercano |
| 508 | target_nearest_hero | (source) | Entity? | Héroe más cercano |
| 509 | target_furthest_enemy | (source) | Entity? | Enemigo más lejano |
| 510 | target_lowest_hp | (source, filter?) | Entity? | Menor HP |
| 511 | target_highest_hp | (source, filter?) | Entity? | Mayor HP |
| 512 | target_lowest_hp_pct | (source, filter?) | Entity? | Menor % HP |
| 513 | target_random_enemy | (source) | Entity? | Enemigo aleatorio |
| 514 | target_random_hero | (source) | Entity? | Héroe aleatorio |
| 515 | target_last_damaged | (entity) | Entity? | Último que dañó |
| 516 | target_killer | (entity) | Entity? | Quién mató |
| 517 | target_attacker | (entity) | Entity? | Quién ataca |

**21c. Target múltiple**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 518 | targets_in_area | (center, radius, filter?) | [Entity] | Todas en área |
| 519 | targets_in_line | (from, to, width, filter?) | [Entity] | Todas en línea |
| 520 | targets_in_cone | (origin, dir, angle, range, filter?) | [Entity] | Todas en cono |
| 521 | all_enemies | (source) | [Entity] | Todos los enemigos |
| 522 | all_allies | (source) | [Entity] | Todos los aliados |
| 523 | all_heroes | () | [Entity] | Todos los héroes |
| 524 | chain_targets | (source, max_targets, max_dist) | [Entity] | Encadena cercanos |

**21d. Target por rayo**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 525 | target_first_hit | (from, to, width) | Entity? | Primera en rayo |
| 526 | target_line_all | (from, to, width) | [Entity] | Todas en trayectoria |
| 527 | target_bounce_chain | (from, max_jumps, max_dist) | [Entity] | Rebota entre targets |
| 528 | target_filter | (candidates, predicate) | [Entity] | Filtra lista |
| 529 | target_sort | (candidates, comparator) | [Entity] | Ordena candidatos |

---

### 22. SUMMON — entidades derivadas

**22a. Invocaciones**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 530 | summon | (type, owner, pos, dur) | EntityId | Invoca unit temporal |
| 531 | summon_at | (type, owner, x, y, dur) | EntityId | En posición |
| 532 | summon_leashed | (type, owner, pos, leash_r, dur) | EntityId | Con leash |
| 533 | summon_copy | (source, owner, dur) | EntityId | Copia de entity |
| 534 | summon_wolf | (owner, dur) | EntityId | Lobo |
| 535 | summon_golem | (owner, dur) | EntityId | Golem |
| 536 | summon_skeleton | (owner, dur, count) | [EntityId] | Varios esqueletos |
| 537 | summon_demon | (owner, dur) | EntityId | Demonio |

**22b. Ilusiones**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 538 | create_illusion | (source, owner, dur, dmg_out, dmg_in) | EntityId | Con modificadores de daño |
| 539 | mirror_image | (source, owner, count, dur) | [EntityId] | N ilusiones simétricas |
| 540 | conjure_copy | (source, owner, dur) | EntityId | Sin modificadores |
| 541 | split | (source, count) | [EntityId] | Divide en N copias |
| 542 | get_illusion_damage_out | (illusion) | Float | % daño infligido |
| 543 | get_illusion_damage_in | (illusion) | Float | % daño recibido |

**22c. Wards**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 544 | place_observer | (owner, x, y, dur) | EntityId | Visión |
| 545 | place_sentry | (owner, x, y, dur) | EntityId | True sight |
| 546 | place_ward_ability | (ability, owner, x, y, dur, radius) | EntityId | Por habilidad |
| 547 | ward_destroy | (ward) | — | Destruye |

**22d. Pets / Summons persistentes**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 548 | summon_persistent | (type, owner, pos) | EntityId | Sin duración |
| 549 | summon_treant | (owner, pos, dur) | EntityId | Treant |
| 550 | summon_boar | (owner, pos, dur) | EntityId | Jabalí |
| 551 | summon_familiar | (owner, pos, dur) | EntityId | Familiar |
| 552 | summon_spiderling | (owner, pos, dur) | EntityId | Spiderling |

**22e. Gestión**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 553 | unsummon | (summon) | — | Desinvoca |
| 554 | unsummon_all | (owner) | — | Todo de un owner |
| 555 | unsummon_by_type | (owner, type) | — | Por tipo |
| 556 | is_summon | (entity) | Bool | Verifica |
| 557 | get_summon_owner | (summon) | EntityId | Owner |
| 558 | count_summons | (owner, type?) | Nat | Cantidad activos |
| 559 | set_summon_command | (summon, command) | — | Orden (attack/move/follow) |

---

### 23. INVENTORY — gestión de items

**23a. Añadir/quitar**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 560 | add_item | (hero, item) | — | Añade |
| 561 | remove_item | (hero, item) | — | Quita |
| 562 | replace_item | (hero, old, new) | — | Sustituye |
| 563 | drop_item | (hero, item) | — | Suelta al suelo |
| 564 | pick_up_item | (hero, ground_item) | — | Recoge |
| 565 | swap_items | (hero, slot_a, slot_b) | — | Intercambia slots |
| 566 | sell_item | (hero, item) | — | Vende por oro |

**23b. Uso**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 567 | use_item | (hero, item, target?) | — | Usa activo |
| 568 | use_item_point | (hero, item, x, y) | — | Hacia punto |
| 569 | use_item_aoe | (hero, item, center, radius) | — | De área |
| 570 | consume_item | (hero, item) | — | Usa y consume |
| 571 | activate_item | (hero, item) | — | Activa temporalmente |
| 572 | toggle_item | (hero, item) | — | Alterna activo/inactivo |

**23c. Consulta**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 573 | has_item | (hero, item) | Bool | Tiene el item |
| 574 | item_count | (hero, item?) | Nat | Cantidad |
| 575 | get_items | (hero) | [Item] | Lista |
| 576 | inventory_full | (hero) | Bool | Lleno |
| 577 | inventory_space | (hero) | Nat | Slots libres |
| 578 | item_cooldown | (hero, item) | Nat | Cooldown restante |
| 579 | item_ready | (hero, item) | Bool | Listo para usar |

**23d. Tienda**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 580 | buy_item | (hero, item) | — | Compra si tiene oro |
| 581 | can_afford | (hero, item) | Bool | Tiene oro |
| 582 | get_item_cost | (item) | Int | Costo |
| 583 | get_item_value | (item) | Int | Valor de venta |
| 584 | is_in_shop_range | (hero) | Bool | Cerca de tienda |

**23e. Carga / Combinación**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 585 | set_item_charges | (hero, item, charges) | — | Fija cargas |
| 586 | add_item_charge | (hero, item) | — | Añade carga |
| 587 | use_item_charge | (hero, item) | Bool | Usa carga; false si vacío |
| 588 | get_item_charges | (hero, item) | Nat | Restantes |
| 589 | item_has_charges | (hero, item) | Bool | Tiene cargas |
| 590 | combine_items | (hero, item_a, item_b, recipe) | — | Combina |
| 591 | disassemble | (hero, item) | — | Desarma en componentes |

---

## [E] LINGÜÍSTICA & META

---

### 24. FLOW — control de flujo

**24a. Condición**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 592 | if | (condition, then, else?) | — | Ramificación |
| 593 | switch | (value, cases, default?) | — | Selección múltiple |
| 594 | match | (entity, cases) | — | Match sobre estado/tipo |
| 595 | ternary | (condition, a, b) | Value | Retorna a o b |

**24b. Iteración**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 596 | loop | (body, times?) | — | N veces (infinito si no) |
| 597 | while | (condition, body) | — | Mientras true |
| 598 | for_each | (collection, body) | — | Itera colección |
| 599 | for_range | (start, end, step, body) | — | Rango numérico |
| 600 | break | — | — | Sale del loop |
| 601 | continue | — | — | Siguiente iteración |
| 602 | repeat | (n, body) | — | Exactamente N veces |
| 603 | do_while | (body, condition) | — | Al menos una vez |

**24c. Llamada**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 604 | call | (handler, args?) | — | Llama a handler |
| 605 | call_return | (handler, args?) | Value | Llama y retorna |
| 606 | return | (value?) | — | Retorna de handler |
| 607 | tail_call | (handler, args?) | — | Llamada de cola |
| 608 | spawn_routine | (handler, args?) | HandlerId | Ejecuta en paralelo conceptual |
| 609 | await_routine | (handler_id) | — | Espera que termine |
| 610 | cancel_routine | (handler_id) | — | Cancela |

**24d. Pausa / Espera**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 611 | wait | (ticks) | — | Espera N ticks |
| 612 | wait_until | (condition) | — | Hasta condición |
| 613 | wait_event | (event_type) | — | Hasta evento |
| 614 | wait_event_of | (event_type, entity) | — | Evento de entity |
| 615 | yield | — | — | Cede al scheduler |

**24e. Concurrencia**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 616 | fork | (effect_a, effect_b) | — | Dos efectos simultáneos |
| 617 | parallel | (effects[]) | — | Lista simultánea |
| 618 | race | (effects[]) | — | Primero en completar |
| 619 | barrier | (effects[]) | — | Espera a que todos terminen |

---

### 25. MATH — aritmética

**25a. Operaciones básicas**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 620 | add | (a, b) | Int/Float | Suma |
| 621 | sub | (a, b) | Int/Float | Resta |
| 622 | mul | (a, b) | Int/Float | Multiplicación |
| 623 | div | (a, b) | Int/Float | División (error si b=0) |
| 624 | mod | (a, b) | Int | Módulo |
| 625 | neg | (a) | Int/Float | Negación |
| 626 | abs | (a) | Int/Float | Valor absoluto |
| 627 | inc | (a) | Int/Float | a+1 |
| 628 | dec | (a) | Int/Float | a-1 |

**25b. Comparación numérica**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 629 | lt | (a, b) | Bool | a < b |
| 630 | lte | (a, b) | Bool | a <= b |
| 631 | gt | (a, b) | Bool | a > b |
| 632 | gte | (a, b) | Bool | a >= b |
| 633 | eq | (a, b) | Bool | a == b |
| 634 | neq | (a, b) | Bool | a != b |
| 635 | between | (a, lo, hi) | Bool | lo <= a <= hi |
| 636 | in_set | (a, set) | Bool | a ∈ set |

**25c. Avanzadas**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 637 | pow | (a, e) | Float | a^e |
| 638 | sqrt | (a) | Float | √a |
| 639 | min_val | (a, b) | Float | Mínimo |
| 640 | max_val | (a, b) | Float | Máximo |
| 641 | clamp | (a, lo, hi) | Float | Limita al rango |
| 642 | floor | (a) | Int | Redondeo abajo |
| 643 | ceil | (a) | Int | Redondeo arriba |
| 644 | round | (a) | Int | Más cercano |
| 645 | lerp | (a, b, t) | Float | Interpolación lineal |
| 646 | inverse_lerp | (a, b, v) | Float | Inversa de lerp |
| 647 | remap | (v, f_lo, f_hi, t_lo, t_hi) | Float | Remapea rango |

**25d. Colecciones numéricas**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 648 | sum_vals | (values[]) | Float | Suma |
| 649 | avg_vals | (values[]) | Float | Promedio |
| 650 | min_of | (values[]) | Float | Mínimo |
| 651 | max_of | (values[]) | Float | Máximo |
| 652 | count_where | (values[], pred) | Nat | Cuántos cumplen |
| 653 | sum_where | (values[], pred) | Float | Suma los que cumplen |

---

### 26. LOGIC — booleanos/predicados

**26a. Operadores**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 654 | and | (a, b) | Bool | Conjuncción |
| 655 | or | (a, b) | Bool | Disyunción |
| 656 | not | (a) | Bool | Negación |
| 657 | xor | (a, b) | Bool | O exclusivo |
| 658 | implies | (a, b) | Bool | a → b |
| 659 | iff | (a, b) | Bool | a ↔ b |

**26b. Predicados generales**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 660 | is_true | (a) | Bool | Verifica truthy |
| 661 | is_false | (a) | Bool | Verifica falsy |
| 662 | is_null | (a) | Bool | Es null |
| 663 | is_not_null | (a) | Bool | No es null |
| 664 | in_type | (a, type) | Bool | Verifica tipo |
| 665 | is_between | (a, lo, hi) | Bool | Verifica rango |
| 666 | satisfies | (entity, predicate) | Bool | Cumple predicado |

**26c. Colecciones lógicas**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 667 | any | (collection, predicate) | Bool | Al menos uno |
| 668 | all | (collection, predicate) | Bool | Todos |
| 669 | none | (collection, predicate) | Bool | Ninguno |
| 670 | exists | (collection) | Bool | No vacía |
| 671 | is_empty | (collection) | Bool | Vacía |
| 672 | count_bool | (collection, predicate) | Nat | Cuenta verdaderos |

---

### 27. RANDOM — RNG sembrado

**27a. Aleatoriedad numérica**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 673 | random_int | (min, max) | Int | Entero en [min, max] |
| 674 | random_float | (min, max) | Float | Float en [min, max) |
| 675 | random_unit | — | Float | En [0, 1) |
| 676 | random_normal | (mean, stddev) | Float | Distribución normal |

**27b. Elección**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 677 | random_choice | (collection) | Value | Elemento aleatorio |
| 678 | random_enemy_of | (entity) | Entity? | Enemigo aleatorio |
| 679 | random_ally_of | (entity) | Entity? | Aliado aleatorio |
| 680 | random_point_in_area | (center, radius) | Pos | Punto en área |
| 681 | shuffle | (collection) | — | Reordena in-place |
| 682 | sample | (collection, n) | [Value] | Muestra de tamaño n |

**27c. Probabilidad**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 683 | chance | (pct) | Bool | Probabilidad pct% |
| 684 | chance_of | (value, weights[]) | Value | Selección con pesos |
| 685 | coin_flip | — | Bool | 50/50 |
| 686 | dice_roll | (sides) | Int | Dado de N lados |

**27d. Semilla**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 687 | get_seed | — | Nat | Semilla actual |
| 688 | reseed | (seed) | — | Cambia semilla global |
| 689 | fork_rng | — | Nat | Subsemilla derivada |
| 690 | checkpoint_rng | — | Nat | Guarda estado |
| 691 | restore_rng | (checkpoint) | — | Restaura estado |

---

### 28. IO — entrada/salida

**28a. Entrada**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 692 | input_wait | — | Value | Espera y lee siguiente |
| 693 | input_peek | — | Value? | Lee sin consumir |
| 694 | input_has | — | Bool | Hay pendiente |
| 695 | input_count | — | Nat | Pendientes |
| 696 | input_at | (index) | Value | Posición específica |

**28b. Salida**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 697 | output | (value) | — | Escribe valor |
| 698 | output_char | (char_code) | — | Carácter ASCII |
| 699 | output_string | (string) | — | Cadena |
| 700 | output_number | (number) | — | Número |
| 701 | output_newline | — | — | Salto de línea |
| 702 | output_entity_state | (entity, key?) | — | Volcado de entity |
| 703 | output_all | (filter?) | — | Todas las entities |

**28c. Archivo (experimental)**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 704 | file_read | (path) | String? | Lee archivo |
| 705 | file_write | (path, content) | — | Escribe archivo |
| 706 | file_exists | (path) | Bool | Verifica |
| 707 | file_delete | (path) | — | Elimina |

> NOTA: FILE puede ser UNSUPPORTED en MVP. Decidir en SPEC.

---

### 29. TRACE — observabilidad/debug

**29a. Logging**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 708 | log | (message, level?) | — | Log con nivel |
| 709 | log_entity | (entity, message?) | — | Con contexto |
| 710 | log_event | (event, message?) | — | Con contexto de evento |
| 711 | log_state | (entity, keys?) | — | Estado completo/parcial |

**29b. Depuración**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 712 | assert | (condition, message) | — | Falla si false |
| 713 | assert_state | (entity, key, expected) | — | Verifica estado |
| 714 | assert_resource | (entity, resource, expected) | — | Verifica recurso |
| 715 | assert_alive | (entity) | — | Verifica vivo |
| 716 | assert_dead | (entity) | — | Verifica muerto |
| 717 | assert_in_range | (entity, target, range) | — | Verifica posición |
| 718 | assert_modifier | (entity, type, exists) | — | Verifica modifier |
| 719 | assert_no_modifier | (entity, type) | — | Verifica ausencia |

**29c. Inspección**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 720 | inspect | (entity) | — | Dump completo |
| 721 | inspect_state | (entity) | — | Solo estado |
| 722 | inspect_modifiers | (entity) | — | Solo modifiers |
| 723 | inspect_triggers | (entity) | — | Solo triggers |
| 724 | inspect_position | (entity) | — | Solo posición |
| 725 | inspect_resources | (entity) | — | Solo recursos |
| 726 | inspect_inventory | (hero) | — | Solo inventario |
| 727 | inspect_auras | (entity) | — | Solo auras |
| 728 | inspect_event_queue | — | — | Cola de eventos |
| 729 | inspect_world | () | — | Mundo completo |

**29d. Métricas**

| # | NOMBRE | FIRMA | RET | DESCRIPCIÓN |
|---|--------|-------|-----|-------------|
| 730 | get_tick | — | Nat | Tick actual |
| 731 | get_event_count | (type?) | Nat | Total emitidos |
| 732 | get_entity_count | (type?) | Nat | Total entities |
| 733 | get_modifier_count | (type?) | Nat | Total modifiers |
| 734 | get_total_damage | (entity?) | Int | Daño total |
| 735 | get_total_healing | (entity?) | Int | Curación total |
| 736 | get_kills | (entity) | Nat | Kills |
| 737 | get_deaths | (entity) | Nat | Muertes |
| 738 | get_assists | (entity) | Nat | Assists |
| 739 | get_gold_earned | (entity) | Int | Oro ganado |
| 740 | trace_event | (event) | — | Añade al trace |
| 741 | trace_state_change | (entity, key, before, after) | — | Cambio de estado |
| 742 | trace_resource_change | (entity, resource, before, after) | — | Cambio de recurso |
| 743 | trace_output | (trace_entry) | — | Añade entrada |
| 744 | dump_trace | () | [TraceEntry] | Trace completo |

---

## Cross-references: gating por CONTROL

El sistema **CONTROL §10** afecta múltiples ramas:

```
MODIFIER          → ACCIONES QUE BLOQUEA
─────────────────────────────────────────────────────────────
STUN              → CAST (§20), MOVEMENT (§5c), ITEM_USE (§23b),
                    CHANNEL (§20b)
ROOT              → MOVEMENT (§5c)
SILENCE           → CAST (§20)
DISARM            → ATTACK (implícito)
TAUNT             → fuerza ATTACK, bloquea otros CAST
FEAR              → restringe MOVEMENT a dirección away
SLEEP             → todas las acciones
HEX               → CAST (§20), ITEMS (§23)
BREAK             → abilities pasivas (modifiers activos)
MUTE              → ITEM_USE (§23b)
SUPPRESS          → todo excepto items básicos
LEASH             → MOVEMENT más allá de max_dist
BLIND             → ATTACK (% miss)
```

---

## Estadísticas del catálogo

| Rama | Subramas | Acciones |
|------|----------|----------|
| 1. ENTITY | 4 | 17 |
| 2. STATE | 5 | 22 |
| 3. MEMORY | 6 | 45 |
| 4. RESOURCE | 5 | 28 |
| 5. SPACE | 8 | 64 |
| 6. TIME | 4 | 23 |
| 7. EVENT | 5 | 25 |
| 8. PROJECTILE | 4 | 23 |
| 9. MODIFIER | 5 | 34 |
| 10. CONTROL | 10 | 42 |
| 11. DISPEL | 4 | 13 |
| 12. AURA | 3 | 13 |
| 13. SHIELD | 3 | 13 |
| 14. REFLECT | 3 | 10 |
| 15. VISION | 3 | 13 |
| 16. DAMAGE | 9 | 42 |
| 17. HEAL | 5 | 15 |
| 18. DEATH | 4 | 17 |
| 19. RESPAWN | 3 | 12 |
| 20. CAST | 5 | 29 |
| 21. TARGET | 4 | 29 |
| 22. SUMMON | 5 | 30 |
| 23. INVENTORY | 5 | 32 |
| 24. FLOW | 5 | 28 |
| 25. MATH | 4 | 34 |
| 26. LOGIC | 3 | 19 |
| 27. RANDOM | 4 | 19 |
| 28. IO | 3 | 16 |
| 29. TRACE | 4 | 37 |
| **TOTAL** | **119** | **744** |

---

## Nota sobre IMPLEMENTACIÓN

**No todas las 744 acciones son primitivas del runtime.**

Muchas son **derivadas**: composiciones de las 7 primitivas de MODEL_DISCOVERY.md.
Por ejemplo:

- `heal(target, amount)` = `gain(target, hp, amount)`
- `stun(target, dur)` = `apply_modifier(target, target, STUN, dur)` con `gate={move,cast,attack}`
- `damage_area(...)` = loop sobre `area_cast` + `damage`
- `spawn_projectile(...)` = `spawn_entity` + `periodic` de movimiento + `on_hit`

En SPEC.md se decidirá cuáles son **primitivas del runtime** (implementadas directamente) y cuáles se **construyen** como macros de composición. El catálogo es la superficie completa del lenguaje; la implementación decidirá la profundidad del runtime.

---

## Nota sobre FLOW §24

El control de flujo **emerge del sistema de eventos + schedule**:

- `if(cond, then, else)` → Effect que evalúa condición y ejecuta branch
- `loop(body)` → `periodic(body, every=1)` hasta `cancel_periodic`
- `wait(ticks)` → `schedule(continuation, at=now+ticks)`
- `call(handler)` → composición inline (sin call stack explícito en runtime)

La sintaxis literal de FLOW es opcional: puede aparecer como azúcar sintáctico o como composición de Effects. Decidir en SPEC.

---

Evidence before narrative.
Never Guess.
