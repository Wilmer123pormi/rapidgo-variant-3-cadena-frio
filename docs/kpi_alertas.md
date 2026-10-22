# KPI y reglas de alerta — Cadena de frío

## 1. Objetivo

Definir indicadores para evaluar las condiciones de transporte
y reglas para detectar desviaciones en la cadena de frío.

## 2. Parámetros iniciales (provisionales)

Producto de referencia: `producto_refrigerado` (alimento perecedero o medicamento de refrigeración).

| Parámetro | Valor | Unidad |
|---|---|---|
| Temperatura permitida | 2 a 8 | °C |
| Humedad permitida | 35 a 65 | % |
| Umbral de temperatura crítica | ≥ 10 o ≤ 0 | °C |
| Duración máxima tolerada fuera de rango | 10 | minutos |
| Frecuencia de muestreo esperada | 1 evento por minuto por pedido | — |

Los límites son inclusivos. Un evento está **fuera de rango** si su temperatura o su humedad salen del rango permitido.

Los valores son **provisionales**: se justifican con el producto de referencia y se validarán con los datos reales de la ejecución del pipeline (Semana 2).

## 3. KPI

Cada evento representa el intervalo hasta el siguiente evento del mismo `pedido_id`; para el último evento se usa la frecuencia de muestreo.

### KPI 1. Tiempo acumulado fuera del rango permitido

- **Descripción:** tiempo total durante el cual un pedido permanece fuera del rango permitido.
- **Unidad:** minutos.
- **Cálculo:** suma de los intervalos cuyo evento inicial está fuera de rango.

### KPI 2. Duración de cada episodio fuera de rango

- **Descripción:** tiempo transcurrido desde que se detecta una desviación hasta que se recupera la condición permitida. Un episodio es una racha de eventos consecutivos fuera de rango.
- **Unidad:** minutos.
- **Cálculo:** `timestamp` del primer evento que vuelve a rango menos `timestamp` del primer evento fuera de rango. Si el episodio sigue abierto, se usa el último evento recibido.

### KPI 3. Porcentaje de tiempo dentro del rango permitido

- **Descripción:** proporción del tiempo monitorizado en que el pedido estuvo dentro del rango permitido.
- **Unidad:** porcentaje.
- **Cálculo:** `100 × (1 − KPI 1 / tiempo total monitorizado del pedido)`.

## 4. Reglas de alerta

| # | Alerta | Condición | Severidad |
|---|---|---|---|
| 1 | Temperatura crítica | `temperatura_c >= 10` o `temperatura_c <= 0` en un evento | CRÍTICA |
| 2 | Exposición prolongada fuera de rango | Episodio abierto (KPI 2) con duración `>= 10` minutos | ALTA |

### Justificación de los umbrales
- **Temperatura crítica (≥ 10 °C o ≤ 0 °C):** queda 2 °C por fuera del rango permitido; evita alertar por oscilaciones normales (sensor, apertura de puerta) y detecta excursiones reales de calor o congelación.
- **Exposición prolongada (10 min):** una salida breve de rango suele ser tolerable (por ejemplo, durante una entrega); 10 minutos continuos indican una falla del vehículo o de la carga.

## 5. Consideraciones de cálculo

Los tiempos fuera de rango se estiman a partir de las marcas de tiempo de los eventos.
La precisión depende de la frecuencia de muestreo y de la calidad de los datos recibidos.
