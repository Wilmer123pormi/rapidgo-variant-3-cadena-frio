
# KPI y reglas de alerta — Cadena de frío

## 1. Objetivo

Definir indicadores para evaluar las condiciones de transporte
y reglas para detectar desviaciones en la cadena de frío.

## 2. KPI

### KPI 1. Tiempo acumulado fuera del rango permitido

- **Descripción:** tiempo total durante el cual un producto permanece
  fuera del rango de temperatura establecido.
- **Unidad:** minutos.
- **Cálculo inicial:** suma de los intervalos estimados fuera de rango.

### KPI 2. Duración de cada episodio fuera de rango

- **Descripción:** tiempo transcurrido desde que se detecta una
  desviación de temperatura hasta que se recupera la condición permitida.
- **Unidad:** minutos.
- **Cálculo inicial:** hora de recuperación menos hora de inicio
  de la desviación.

### KPI 3. Porcentaje de tiempo dentro del rango permitido

- **Descripción:** proporción del tiempo monitorizado en que la
  temperatura estuvo dentro del rango establecido.
- **Unidad:** porcentaje.
- **Cálculo inicial:** tiempo estimado dentro de rango dividido
  entre el tiempo total monitorizado, multiplicado por 100.

## 3. Reglas de alerta

### Alerta 1. Temperatura crítica

Generar una alerta cuando una medición alcance o supere el
umbral crítico definido para el producto transportado.

### Alerta 2. Exposición prolongada fuera de rango

Generar una alerta cuando la temperatura permanezca fuera del
rango permitido durante un tiempo superior al límite establecido.

## 4. Parámetros pendientes

Antes de implementar estas reglas, el equipo debe definir:

- Tipo de producto transportado.
- Temperatura mínima y máxima permitidas.
- Umbral de temperatura crítica.
- Duración máxima tolerada fuera del rango.
- Frecuencia de muestreo de los sensores.

Los umbrales serán provisionales hasta que se justifiquen
según el producto seleccionado.

## 5. Consideraciones de cálculo

Los tiempos fuera de rango se estimarán a partir de las marcas
de tiempo de los eventos. La precisión dependerá de la frecuencia
de muestreo y de la calidad de los datos recibidos.
