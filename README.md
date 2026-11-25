# Sistema de Impresoras en Red

## Integrantes

- Christian Guerrero
- Carlos Lema

## Descripción

El proyecto **Sistema de Impresoras en Red** se enfoca en representar y gestionar un entorno en el que varias impresoras se encuentran conectadas a una red y pueden ser utilizadas por diferentes usuarios.

La situación permitirá analizar y desarrollar una solución para administrar las impresoras disponibles y los procesos relacionados con su utilización dentro de una red compartida.

## Avance de implementación

Ejecuta `python3 impresoras.py` desde la raíz del repositorio en Codespaces (Python 3.10 o posterior, sin dependencias externas). En Windows puedes usar `python impresoras.py`. El menú permite configurar clientes e impresoras y ejecutar una versión o comparar las cuatro: entero o diccionario, con o sin mutex.

Consulta la [sección crítica y la tabla de resultados](docs/Implementacion.md) y la [salida real de la ejecución](docs/evidencia_ejecucion.txt).

El proyecto está dividido en archivos. Abre la carpeta completa en tu IDE y ejecuta **`impresoras.py`**. Los demás archivos se cargan automáticamente:

| Archivo | Función |
|---|---|
| `impresoras.py` | Inicia el menú interactivo. |
| `interfaz_consola.py` | Solicita parámetros y muestra operaciones y comparación. |
| `simulador.py` | Crea el recurso compartido y coordina los clientes. |
| `hilo_cliente.py` | Define la única clase que hereda de `Thread`. |
| `cupos_impresion.py` | Guarda la disponibilidad como entero. |
| `registro_impresoras.py` | Guarda las asignaciones en un diccionario. |

Una reserva rechazada significa que ya no hay impresoras libres. El aviso de doble reserva identifica el fallo que se busca reproducir sin mutex. Un error de ejecución indica que la prueba no pudo completarse.

La interfaz actual muestra `CONDICIÓN DE CARRERA` si las aceptaciones no coinciden con las reservas guardadas. Consulta las instrucciones y los límites de la prueba en [Interfaz de consola](docs/Interfaz.md). Para ejecutar las pruebas automáticas: `python3 -m unittest -v test_interfaz`.
