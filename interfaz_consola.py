from simulador import Simulador


class InterfazConsola:
    """Configura las pruebas y muestra el registro de los hilos."""

    def __init__(self):
        self.clientes = 2
        self.impresoras = 1

    def numero(self, mensaje, minimo, maximo):
        while True:
            try:
                valor = int(input(mensaje))
                if minimo <= valor <= maximo:
                    return valor
            except ValueError:
                pass
            print(f"[DATO NO VÁLIDO] Escribe un entero entre {minimo} y {maximo}.")

    def mostrar(self, r):
        modo = "con mutex" if r['sincronizado'] else "sin mutex"
        print(f"\n=== {r['tipo'].upper()} / {modo} ===")
        print("Registro al terminar, ordenado por finalización de operaciones.")
        print("Antes: lectura usada para decidir. Después: captura tras la operación.")
        print("Los hilos pueden intercalarse; la captura no es el estado final global.")
        for e in r['eventos']:
            resultado = "ACEPTADA" if e['aceptada'] else "RECHAZADA: sin disponibilidad"
            print(f"\nHilo: {e['hilo']} | Operación: {e['operacion']}")
            print(f"  Antes: {e['antes']}")
            print(f"  Resultado: {resultado}")
            print(f"  Después: {e['despues']}")
        print(f"\nESTADO FINAL: {r['estado_final']}")
        print(f"Aceptadas: {len(r['aceptadas'])} | Rechazadas: {len(r['rechazadas'])}")
        print(f"Reservas guardadas: {r['ocupadas']}")
        if r['carrera']:
            print("[CONDICIÓN DE CARRERA] Las aceptaciones no coinciden con las reservas guardadas.")
        else:
            print("[ESTADO CONSISTENTE] Cada aceptación tiene una reserva registrada.")

    def ejecutar(self):
        casos = [('entero', False), ('entero', True),
                 ('diccionario', False), ('diccionario', True)]
        try:
            while True:
                print("\n=== SISTEMA DE IMPRESORAS EN RED ===")
                print(f"Configuración: {self.clientes} clientes / {self.impresoras} impresoras")
                print("1. Configurar clientes e impresoras")
                print("2. Entero sin mutex\n3. Entero con mutex")
                print("4. Diccionario sin mutex\n5. Diccionario con mutex")
                print("6. Comparar las cuatro versiones\n0. Salir")
                opcion = self.numero("Opción: ", 0, 6)
                if opcion == 0:
                    print("Simulador cerrado.")
                    return 0
                if opcion == 1:
                    self.clientes = self.numero("Clientes (2-20): ", 2, 20)
                    self.impresoras = self.numero("Impresoras (1-10): ", 1, 10)
                    continue
                resultados = []
                try:
                    for tipo, mutex in (casos if opcion == 6 else [casos[opcion - 2]]):
                        r = Simulador().ejecutar(tipo, mutex, self.clientes,
                                                self.impresoras, detallado=True)
                        self.mostrar(r)
                        resultados.append(r)
                except (ValueError, RuntimeError) as exc:
                    print(f"[ERROR DE EJECUCIÓN] {exc}")
                    continue
                if opcion == 6:
                    print("\n=== COMPARACIÓN: recurso nuevo por versión ===")
                    print("Recurso / Mutex / Aceptadas / Guardadas / Carrera")
                    for r in resultados:
                        print(f"{r['tipo']} / {r['sincronizado']} / "
                              f"{len(r['aceptadas'])} / {r['ocupadas']} / "
                              f"{'SÍ' if r['carrera'] else 'NO'}")
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada cerrada. Simulador finalizado.")
            return 0
