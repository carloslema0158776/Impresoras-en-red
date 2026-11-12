# Avance de implementación concurrente

**Christian Guerrero y Carlos Lema · Sistemas Operativos**

Dos clientes, S1 y S2, compiten por la última impresora disponible. Cada prueba crea un solo recurso y pasa esa misma instancia a ambos hilos. El avance se limita a la reserva: no ejecuta trabajos reales ni libera la impresora durante la prueba, porque eso permitiría dos reservas sucesivas válidas y ocultaría la doble asignación que queremos demostrar.

## Clases

| Clase | Responsabilidad |
|---|---|
| `HiloCliente` | Única clase que hereda de `Thread`. Su método `run()` pide una reserva al recurso recibido y guarda el resultado. Se crean dos objetos de esta clase. |
| `Simulador` | Crea una instancia del recurso, se la pasa a ambos clientes, inicia los hilos y espera con `join()` antes de leer los resultados. |
| `CuposImpresion` | Gestiona la cantidad disponible mediante el entero `disponibles`. `reservar()` descuenta un cupo si lo hay. |
| `RegistroImpresoras` | Gestiona un diccionario de impresoras y solicitudes. `None` significa libre. `reservar()` busca una impresora libre y registra el identificador de la solicitud. |

El simulador y los recursos son clases normales dentro del mismo proceso de Python. Los dos hilos comparten el objeto del recurso; no se crea una copia por cliente.

## Sección crítica y solución

- **Entero:** leer el contador, validar que sea mayor que cero y guardar el valor decrementado. Si ambos hilos leen 1, ambos pueden guardar 0 y reportar éxito aunque solo había un cupo.
- **Diccionario:** consultar la asignación, validar que sea `None` y guardar la solicitud. Si ambos hilos ven P1 libre, ambos reportan éxito, pero el diccionario solo conserva la última escritura.
- **Con mutex:** cada recurso sincronizado tiene un solo `Lock`, compartido por ambos clientes. `with` lo adquiere antes de la consulta y lo libera al salir del bloque, incluso si el método retorna antes o lanza una excepción. El segundo hilo consulta el estado ya actualizado y rechaza su reserva.

Los comentarios `SECCIÓN CRÍTICA` señalan estas operaciones en ambos métodos. La variante sin mutex usa `nullcontext()`, que no bloquea. Solo en esa variante, una barrera de prueba espera a que ambos clientes hayan consultado y validado la disponibilidad antes de escribir. La barrera provoca la intercalación para que el fallo sea reproducible; no protege las escrituras ni forma parte de la solución.

## Resultados

| Representación | Modo | Aceptadas | Rechazadas | Estado final |
|---|---|---:|---:|---|
| Entero | Sin Lock | 2 | 0 | 0 cupos; dos aceptaciones para un solo cupo. |
| Entero | Con Lock | 1 | 1 | 0 cupos; una sola reserva válida. |
| Diccionario | Sin Lock | 2 | 0 | P1 conserva una solicitud y la otra queda sobrescrita. |
| Diccionario | Con Lock | 1 | 1 | P1 conserva la única solicitud aceptada. |

Para reproducir los cuatro casos, ejecuta `python impresoras.py`. La [evidencia](evidencia_ejecucion.txt) es la salida real de una ejecución. El cliente ganador y la última escritura pueden variar; las cantidades esperadas son las de la tabla.

## Decisión

El diccionario es preferible para el sistema porque identifica qué impresora recibió qué solicitud. El entero solo indica cuántos cupos quedan. Este avance muestra acceso directo a una instancia compartida para demostrar el problema de sincronización que pide la consigna. En el diseño previo de Paso de Mensajes, el gestor sería el único encargado de acceder al registro.

**Para exponer:** «Dos clientes ven libre la última impresora. Sin mutex los dos creen que la reservaron. Con mutex, el primero consulta y registra su reserva antes de que el segundo pueda consultar. El diccionario, además, nos dice quién quedó asignado a P1».
