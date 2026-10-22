# Contrato del evento — Cadena de frío

Cada lectura de sensor de un vehículo que transporta un pedido se publica en Kafka (tópico `cadena_frio_eventos`, clave `pedido_id`) como un evento JSON.

| Campo | Tipo | Unidad | Obligatorio | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `evento_id` | string | — | Sí | Identificador único del evento | `evt-0001` |
| `pedido_id` | string | — | Sí | Pedido transportado (`PED-` + número). Clave del mensaje en Kafka | `PED-001` |
| `vehiculo_id` | string | — | Sí | Vehículo que transporta el pedido (`VEH-` + número) | `VEH-001` |
| `producto_tipo` | string | — | Sí | Tipo de producto transportado; por ahora solo `producto_refrigerado` | `producto_refrigerado` |
| `timestamp` | string | UTC | Sí | Momento de la lectura, formato ISO 8601 | `2026-10-21T10:30:00Z` |
| `temperatura_c` | number | °C | Sí | Temperatura medida (rango físico válido: -30 a 60) | `4.2` |
| `humedad_pct` | number | % | Sí | Humedad relativa (0 a 100) | `65.0` |

Cubre los eventos mínimos de la variante 3: **pedido, temperatura, humedad, vehículo y tiempo**.

## Ejemplos
- Evento válido dentro de rango: [`samples/evento_cadena_frio.json`](../samples/evento_cadena_frio.json)
- Evento fuera de rango: [`samples/evento_fuera_de_rango.json`](../samples/evento_fuera_de_rango.json)
- Esquema formal (JSON Schema, útil para las pruebas de la Semana 2): [`schemas/evento_cadena_frio.schema.json`](schemas/evento_cadena_frio.schema.json)
