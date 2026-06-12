# Symbol Context Protocol (SCP)

## Protocolo Open Source de Representación de Contexto para Sistemas de IA

**Autor:** Johanny Baez
**Estado:** Borrador v0.2

---

## Visión

Los sistemas multiagente consumen grandes cantidades de contexto describiendo repetidamente objetivos, tareas, estados y relaciones en lenguaje natural.

SCP propone una capa intermedia con **dos representaciones equivalentes**:

- **SCP-C (capa canónica):** notación ASCII densa, optimizada para tokens. Es lo que viaja entre agentes y se guarda en memoria.
- **SCP-V (capa visual):** renderizado con emojis, optimizado para humanos. Es lo que se muestra en dashboards, logs y documentación.

Un parser traduce entre ambas capas y hacia JSON/grafos sin pérdida.

```txt
SCP-C (máquina):   G > T:script > A:writer > X = OK
SCP-V (humano):    🎯 ↓ 📋(script) ↓ 🤖(writer) ↓ ⚡ → ✓
JSON (sistemas):   {"goal":{"task":"script","agent":"writer","exec":"ok"}}
```

La meta no es reemplazar el lenguaje humano. Es separar la eficiencia (capa C) de la legibilidad (capa V) para que ninguna comprometa a la otra.

---

## Problema

- Alto consumo de tokens en sistemas multiagente.
- Contextos extensos y repetitivos.
- Reconstrucción constante del estado operativo.
- Dificultad para compartir conocimiento entre agentes.

Ejemplo tradicional (≈18 tokens):

```txt
El agente de video debe ejecutar la tarea de crear contenido orientado al crecimiento y la monetización.
```

SCP-C (≈10 tokens):

```txt
A:video > T:content = GROW+REV
```

SCP-V (solo para humanos):

```txt
🤖🎬 ⚡ 📋 → 📈 + 💰
```

> **Nota honesta sobre tokens:** los emojis y símbolos Unicode raros suelen costar 2-4 tokens cada uno en los tokenizadores actuales, mientras que los códigos ASCII cuestan 1. Por eso la capa canónica es ASCII y los emojis son únicamente una capa de renderizado. Esta corrección es el cambio principal respecto a v0.1.

---

## Principios Fundamentales

1. **Compresión real, medida.** Toda afirmación de ahorro de tokens debe validarse con benchmarks de tokenizadores reales (tiktoken o equivalente), comparando contra lenguaje natural y JSON.
2. **Legibilidad humana sin costo.** La capa visual existe para humanos; nunca viaja por el contexto del modelo.
3. **Compatibilidad con LLMs actuales.** El diccionario SCP-C cabe en un bloque corto de system prompt; no requiere entrenamiento adicional.
4. **Estructura jerárquica.** Goal → Memory → Task → Agent → Execute → Result.
5. **Orientación a grafos.** Los símbolos son nodos; los operadores son aristas. Mapeo directo a triples (sujeto, relación, objeto).

---

## Diccionario v0.2

| Código (SCP-C) | Render (SCP-V) | Significado | Categoría |
|---|---|---|---|
| `G` | 🎯 | Goal — objetivo | Planificación |
| `M` | 🧠 | Memory — contexto almacenado | Memoria |
| `T` | 📋 | Task — unidad de trabajo | Ejecución |
| `A` | 🤖 | Agent — agente autónomo | Agentes |
| `X` | ⚡ | Execute — paso de ejecución | Ejecución |
| `OK` | ✓ | Complete — éxito | Estado |
| `FAIL` | ✗ | Failed — fallo | Estado |
| `RTY` | 🔄 | Retry — reintento | Estado |
| `GROW` | 📈 | Growth — crecimiento | Negocio |
| `REV` | 💰 | Revenue — ingresos | Negocio |
| `VID` | 🎬 | Video — producción audiovisual | Producción |

---

## Gramática v0.2

| Operador | Nombre | Significado |
|---|---|---|
| `>` | Secuencia | Un elemento conduce/asigna al siguiente (render: ↓) |
| `=` | Resultado | La expresión produce este resultado (render: →) |
| `+` | Combinación | Elementos combinados |
| `:` | Parámetro | Asigna nombre o valor a un símbolo |
| `[ ]` | Grupo | Agrupa expresiones |
| `( )` | Metadata | Contexto adicional |

**Cambio respecto a v0.1:** los operadores ↓ ("conduce a") y → ("produce") se solapaban. En v0.2: `>` encadena pasos del flujo; `=` marca exclusivamente el resultado final de una ejecución.

### Patrones

```txt
Flujo estándar:    G > T > A > X = OK
                   🎯 ↓ 📋 ↓ 🤖 ↓ ⚡ → ✓

Fallo y reintento: G > T > A > X = FAIL > RTY
                   🎯 ↓ 📋 ↓ 🤖 ↓ ⚡ → ✗ → 🔄

Objetivo negocio:  G = [GROW+REV]
                   🎯 → [📈 + 💰]

Con parámetros:    T:script(priority:high) > A:writer > X = OK
                   📋(script, alta prioridad) ↓ 🤖(writer) ↓ ⚡ → ✓

Memoria:           M:user_pref = VID+retention
                   🧠(preferencia): 🎬 + retención
```

---

## Benchmark (medido, tokenizadores reales)

Primer benchmark v0.3 sobre 200 entradas de workflow (cl100k y o200k):

| Formato | Tokens | Ahorro vs prosa |
|---|---|---|
| Prosa en inglés | 4.932 | — |
| JSON compacto | 4.326 | 12% |
| TOON | 2.307 | 53% |
| **SCP-C + leyenda** | **2.508** | **49%** |

Break-even: SCP supera a la prosa desde ~7 entradas y al JSON desde ~9.

Segundo benchmark (estado heterogéneo: workflows + metadata + memoria + reglas, orden preservado): **SCP es el único formato que ahorra tokens (26%) preservando el orden de las entradas** — TOON preservando orden cuesta 2,1x más que SCP y el JSON compacto sale peor que la prosa. En datos tabulares uniformes sin orden, TOON gana: los formatos son complementarios. Datos completos: [benchmarks/results.md](benchmarks/results.md).

---

## Integración con AIOS

```txt
Goal Engine → Knowledge Graph → SCP-C → Agents → Execution
                                  ↕
                               SCP-V (dashboards, logs, humanos)
```

SCP puede funcionar como capa de memoria, comunicación interagente, representación de conocimiento y seguimiento de ejecución.

---

## Roadmap

- **v0.2 — Dos capas (este documento):** diccionario ASCII+render, gramática desambiguada.
- **v0.3 — Parser prototipo + benchmark:** Python, SCP-C ↔ SCP-V ↔ JSON, validación de sintaxis, benchmark de tokens publicado. *(Adelantado: el parser es lo que convierte el concepto en herramienta.)*
- **v0.4 — Diccionario extendido:** 100+ códigos por categoría, convenciones de nombres.
- **v0.5 — Gramática formal:** especificación EBNF, anidamiento, patrones reutilizables.
- **v0.6 — Mapeo a Knowledge Graphs:** nodos, aristas, metadata, ejemplos con bases de grafos.
- **v0.7 — SDKs:** Python y JavaScript (con renderer visual).
- **v0.8 — Integraciones:** LangGraph, CrewAI, AutoGen, AIOS.
- **v1.0 — Estándar estable:** especificación congelada, implementación de referencia.

---

## Trabajo relacionado

Comparativa completa con LLMLingua, TOON, MetaGlyph y otras estrategias: [docs/related-work.md](docs/related-work.md).

SCP se diferencia de: compresión de prompts (LLMLingua) — SCP es una notación, no un compresor estadístico; triples RDF — SCP prioriza flujos de ejecución y legibilidad; y formatos estructurados (JSON/YAML) — SCP-C es más denso y SCP-V más legible. El roadmap incluye comparativas formales.

---

## Misión

Crear un protocolo abierto para representar conocimiento, objetivos, memoria y ejecución de forma compacta para las máquinas y visual para las personas — sin que una meta comprometa la otra.

---

## Skill para Claude

El directorio [`skills/scp-context-optimizer`](skills/scp-context-optimizer) contiene una skill instalable para Claude (Cowork / Claude Code) que aplica SCP automáticamente: comprime contexto operativo a SCP-C, lo renderiza como SCP-V e incluye el parser de referencia (`scripts/scp.py`, SCP-C ↔ JSON ↔ SCP-V).
