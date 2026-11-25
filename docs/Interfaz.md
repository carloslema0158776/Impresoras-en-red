# Interfaz de consola

Se conserva una sola clase derivada de Thread: HiloCliente. InterfazConsola gestiona el menú, Simulador prepara los hilos y las clases CuposImpresion y RegistroImpresoras administran las dos representaciones del recurso.

## Ejecución en Codespaces

Desde la raíz del repositorio: `python3 impresoras.py`. No requiere instalar paquetes. La opción 0 cierra el programa; Ctrl+C o el cierre de la entrada también terminan de forma controlada.

## Menú y configuración

1. Configurar entre 2 y 20 clientes y entre 1 y 10 impresoras.
2. Ejecutar entero sin mutex.
3. Ejecutar entero con mutex.
4. Ejecutar diccionario sin mutex.
5. Ejecutar diccionario con mutex.
6. Comparar las cuatro versiones con los mismos parámetros.

La configuración inicial es de dos clientes y una impresora. Los datos no numéricos o fuera de rango se rechazan y se solicita el valor de nuevo. Cada ejecución crea un recurso nuevo compartido por todos sus hilos; las pruebas no acumulan reservas entre versiones.

## Registro de operaciones

Al terminar la ejecución se muestran las operaciones ordenadas por su instante de finalización. Cada una incluye identificación del hilo, operación solicitada, lectura anterior del recurso, aceptación o rechazo y captura posterior. Las copias del diccionario evitan que una actualización posterior modifique la evidencia de una operación anterior.

La visualización es un registro posterior, no una animación en vivo. Sin mutex, las operaciones se intercalan: el estado anterior es la lectura utilizada para decidir y el posterior es la captura al terminar esa operación, no el estado final global. El orden de los clientes puede variar.

Al finalizar todos los hilos se muestra el estado final y las cantidades de solicitudes aceptadas y rechazadas. En el entero, las reservas guardadas se calculan como total de impresoras menos cupos disponibles. En el diccionario, son las impresoras con una solicitud asignada. Si ese número difiere de las aceptaciones, se informa una condición de carrera.

## Prueba sin mutex y solución

Una barrera de demostración hace que todos los clientes lean antes de actualizar. Así se reproduce el fallo sin depender de la velocidad del equipo: cada cliente puede aceptar según una lectura que ya quedó desactualizada. Esa barrera no protege el recurso ni forma parte de la solución.

Con mutex no se usa la barrera: la consulta, validación y actualización quedan bajo el mismo Lock. Se aceptan como máximo tantas solicitudes como impresoras disponibles. No se imprimen ni se liberan dispositivos durante esta prueba, para observar reservas simultáneas.

## Comparación esperada con dos clientes y una impresora

| Recurso | Mutex | Aceptadas | Reservas guardadas | Carrera |
|---|---|---:|---:|---|
| Entero | No | 2 | 1 | Sí |
| Entero | Sí | 1 | 1 | No |
| Diccionario | No | 2 | 1 | Sí |
| Diccionario | Sí | 1 | 1 | No |

Para comprobar otra configuración, selecciona 1, introduce los valores y selecciona 6. Las condiciones de carrera no son errores de ejecución: son el resultado intencional de la prueba sin mutex.

## Verificación

`python3 -m unittest -v test_interfaz` comprueba las cuatro versiones con cuatro configuraciones, el registro de operaciones, los límites, las opciones del menú, la recuperación ante entradas no válidas y el cierre de entrada.

La evidencia de uso está en [evidencia_interfaz.txt](evidencia_interfaz.txt). La documentación y evidencia anteriores describen el avance previo; este documento explica el menú añadido.
