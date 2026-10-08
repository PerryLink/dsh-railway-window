# dsh-railway-window — Comprobación de tiempos y aritmética del registro de ventanas de trabajo ferroviario

`dsh-railway-window` lee un registro ferroviario de ventanas de trabajo —la cabecera del día más una fila por ventana— y comprueba la coherencia temporal y aritmética de ese propio registro: que cada ventana registre su contenido de trabajo o su número de orden de control de tráfico, que el inicio y el fin se puedan analizar y sean sucesivos, que la duración registrada sea igual al intervalo, que la duración aprobada no supere la solicitada, que el tipo de ventana proceda de su vocabulario, que los números de ventana no se repitan y que el registro declare su fecha de trabajo y la administración ferroviaria (grupo empresarial).

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una fila no registra ni el contenido de trabajo ni el número de orden de control de tráfico. ¿Se informa de ello? | Sí. `RW-001` exige que en cada ventana esté puesto al menos uno de los dos, `workContent` o `permitNo`, e informa de la fila en la que faltan ambos. Solo comprueba que uno de ellos esté rellenado; no juzga si la obra se mantuvo dentro de su ámbito autorizado ni si algo invadió el gálibo de circulación. |
| Una ventana va de `23:30` a `01:30` y está escrita como dos horas del mismo día. ¿Por qué se informa de que el fin es anterior al inicio? | `RW-002` compara los dos instantes y no modela el cruce de medianoche, así que un par del mismo día se lee invertido; registre la fecha en ambos lados o desactive la regla. Si el inicio y el fin coinciden, se considera que el inicio no es posterior, y una hora que no se puede analizar se informa por separado en lugar de omitirse en silencio. |
| La columna de duración está en minutos (`120`) y la ventana fue de 08:00 a 10:00. ¿Por qué no cuadra la aritmética? | `RW-003` mide el intervalo en días, así que un registro en minutos difiere por un factor de 1440; la tolerancia de fábrica es de 0,01 día. Apunte `daysField` a una columna de duración expresada en días o desactive la regla. Solo comprueba la aritmética, nunca si la ventana fue lo bastante larga para la obra. |
| La duración aprobada es mayor que la solicitada. ¿Qué se informa, y qué ocurre si falta una de las dos columnas? | `RW-004` informa de ese par, porque un despachador no concede más de lo solicitado y lo habitual es que las dos columnas estén invertidas. Solo se ejecuta cuando `approvedMin` y `appliedMin` se pueden analizar; si falta uno, informa de que entró en `skipped`. No incorpora ningún techo de reducción de la aprobación y no concluye si la ventana debería concederse. |
| La columna del tipo de ventana tiene valor, pero la regla nunca informa de nada. ¿Se está ejecutando? | No. `RW-005` viene con `values: []`, es decir sin configurar, e informa de que entró en `skipped` hasta que liste las clasificaciones que usan las medidas de su administración. Aun configurada, solo comprueba que el valor figure en su lista; no decide en qué clase debe encuadrarse una ventana. |
| El registro del día está incompleto: la cabecera no nombra la administración y dos ventanas de un mismo tramo repiten número. ¿Qué reglas se activan? | Dos. `RW-007` informa de una cabecera que no declara la fecha de trabajo y la administración ferroviaria (grupo empresarial) —solo comprueba que la cabecera las declare, y puede añadir `skylightPlanNo` a sus `fields` si su formulario también registra un número de plan—. `RW-006` informa del `windowNo` repetido, comparando con los espacios en blanco ignorados; que un tramo reciba varias ventanas el mismo día es normal, así que numérelas por separado. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
|---|---|---|
| 《铁路营业线施工安全管理办法》 | 现行版本与条号本次未核实 | RW-001, RW-002, RW-003, RW-006, RW-007 |
| 各铁路局集团公司施工天窗管理办法（本机构配置） | 无统一标准（本条依据为台账的申请与批准两栏） | RW-004 |
| 各铁路局集团公司施工天窗管理办法（本机构配置） | 无统一标准（本条依据为本机构分类口径） | RW-005 |

**Boundary:** this plugin checks a **铁路施工天窗台账** for time and arithmetic self-consistency — that each window
records its work content or its traffic-control order number, that the start and end times parse and follow each
other, that the recorded duration equals the span, that the approved duration does not exceed the applied
duration, that the window type comes from your vocabulary, that window numbers are unique, and that the register
names its working date and railway bureau. It does **not** decide whether a window should be granted, whether
work encroached on the clearance gauge, whether it was an unsafe act, or whether it affected traffic safety.

> ### ⚠️ Read this before trusting a citation in the report
>
> **Every `excerpt` in this plugin's rule pack says, in so many words, that the clause text was not
> obtained.** The regime lives in 《铁路营业线施工安全管理办法》 and in each railway bureau's own work-window
> and traffic-control-order measures. The verification pass could not retrieve verbatim clause text, so rather
> than paraphrase a quotation the pack states the gap in the `excerpt` field itself and puts the honest
> reasoning in `note`. Every rule is therefore `warn` or `info`, and a test asserts that no rule claims a
> quotation it does not have. **When the texts are in hand, replace each `excerpt` with the real clause and
> raise `kind` to `direct`.**
>
> Three limits matter before trusting a finding:
>
> - **The plugin ships no window classification and no status vocabulary.** How windows are classified and how
>   their states are worded varies by bureau, so `RW-005` reports itself in `skipped` until you configure them.
> - **No approval-ratio ceiling is built in.** Whether an approved window may be shorter than applied for, and
>   by how much, is the bureau's rule; `RW-004` only checks that the approved figure does not exceed the
>   applied one, which is a data-entry property rather than a substantive one.
> - **The duration unit is days, and the rule says so.** `RW-003` measures the span in minutes internally and
>   expresses it in days, so a window that starts and ends on the same calendar day is measured correctly. A
>   register that records durations in minutes differs by a factor of 1440 — repoint `daysField` at a
>   day-denominated column, or disable the rule.
>
> The plugin also **does not handle crossing midnight**: a window written as two same-day times
> (`23:30` to `01:30`) will read as a reversed pair. Record the date on both sides, or disable that rule.

## Compatibility

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-railway-window
dsh --profile <name> --dump-config | grep 'dsh-railway-window'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/railway-window.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-railway-window
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-railway-window contributors.
