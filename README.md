# Sistema de Impresoras en Red

## Integrantes

- Christian Guerrero
- Carlos Lema

## Descripción

El proyecto **Sistema de Impresoras en Red** se enfoca en representar y gestionar un entorno en el que varias impresoras se encuentran conectadas a una red y pueden ser utilizadas por diferentes usuarios.

La situación permitirá analizar y desarrollar una solución para administrar las impresoras disponibles y los procesos relacionados con su utilización dentro de una red compartida.

## Avance de implementación

Ejecuta `python impresoras.py` desde la raíz del repositorio (Python 3.10 o posterior, sin dependencias externas). La demostración compara un entero y un diccionario con dos clientes que intentan reservar una sola impresora, primero sin exclusión mutua y luego con un `Lock`.

Consulta la [sección crítica y la tabla de resultados](docs/Implementacion.md) y la [salida real de la ejecución](docs/evidencia_ejecucion.txt).

El proyecto está dividido en archivos. Abre la carpeta completa en tu IDE y ejecuta **`impresoras.py`**. Los demás archivos se cargan automáticamente:

| Archivo | Función |
|---|---|
| `impresoras.py` | Ejecuta los cuatro casos y muestra sus resultados. |
| `simulador.py` | Crea el recurso compartido y coordina los clientes. |
| `hilo_cliente.py` | Define la única clase que hereda de `Thread`. |
| `cupos_impresion.py` | Guarda la disponibilidad como entero. |
| `registro_impresoras.py` | Guarda las asignaciones en un diccionario. |

Una reserva rechazada significa que ya no hay impresoras libres. El aviso de doble reserva identifica el fallo que se busca reproducir sin mutex. Un error de ejecución indica que la prueba no pudo completarse.
