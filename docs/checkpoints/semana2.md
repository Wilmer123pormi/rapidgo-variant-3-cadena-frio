# Checkpoint Semana 2

1. **Qué quedó funcionando:** 
El productor de Kafka está implementado en Python. Envía eventos al topic `eventos-cadena-frio` usando el `pedido_id` como Key.

2. **Valor o evidencia real observada:** 
Al ejecutar el productor y el consumidor de Kafka al mismo tiempo, se observó que los eventos JSON llegaron correctamente y con su Key a la izquierda.

3. **Decisión técnica tomada:** 
Se decidió que el productor lea los archivos de `samples/` para garantizar que se respete el contrato del evento.

4. **Problema encontrado:** 
Error `ModuleNotFoundError: No module named 'kafka'`. Se resolvió instalando la librería con `pip install kafka-python`.

5. **Enlaces:** 
Issue #5 - PR #