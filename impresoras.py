from contextlib import nullcontext
from threading import Barrier, Lock, Thread


class CuposImpresion:
    """Representa la disponibilidad total con un entero."""

    def __init__(self, total: int, sincronizado: bool):
        self.disponibles: int = total
        self._mutex = Lock() if sincronizado else None

    def reservar(self, solicitud: str, pausa_demostracion=None) -> bool:
        with self._mutex if self._mutex is not None else nullcontext():
            # SECCIÓN CRÍTICA: consultar, validar y descontar el cupo.
            cupos = self.disponibles
            if cupos <= 0:
                return False
            if pausa_demostracion is not None:
                pausa_demostracion.wait()
            # Sin Lock, ambos pueden escribir 0 a partir de la misma lectura.
            self.disponibles = cupos - 1
            return True


class RegistroImpresoras:
    """Relaciona cada impresora con su solicitud; None indica libre."""

    def __init__(self, ids, sincronizado: bool):
        self.registro: dict[str, str | None] = dict.fromkeys(ids)
        self._mutex = Lock() if sincronizado else None

    def reservar(self, solicitud: str, pausa_demostracion=None) -> bool:
        with self._mutex if self._mutex is not None else nullcontext():
            # SECCIÓN CRÍTICA: buscar una impresora, validar y asignarla.
            for impresora, asignada in self.registro.items():
                if asignada is None:
                    if pausa_demostracion is not None:
                        pausa_demostracion.wait()
                    # Sin Lock, la segunda escritura puede borrar la primera.
                    self.registro[impresora] = solicitud
                    return True
            return False


class HiloCliente(Thread):
    """Única clase de hilo: pide una reserva y guarda su resultado."""

    def __init__(self, solicitud, recurso, pausa_demostracion=None):
        super().__init__(name=solicitud)
        self.recurso = recurso
        self.pausa_demostracion = pausa_demostracion
        self.aceptada = None

    def run(self):
        self.aceptada = self.recurso.reservar(self.name, self.pausa_demostracion)


class Simulador:
    """Crea una instancia por prueba y se la pasa a los dos clientes."""

    def ejecutar(self, tipo: str, sincronizado: bool):
        if tipo == "entero":
            recurso = CuposImpresion(1, sincronizado)
        elif tipo == "diccionario":
            recurso = RegistroImpresoras(["P1"], sincronizado)
        else:
            raise ValueError(f"Tipo desconocido: {tipo}")

        # Solo para reproducir la carrera: ambos leen antes de escribir.
        pausa = None if sincronizado else Barrier(2, timeout=5)
        clientes = [HiloCliente(s, recurso, pausa) for s in ("S1", "S2")]
        for cliente in clientes:
            cliente.start()
        for cliente in clientes:
            cliente.join()
        if any(cliente.aceptada is None for cliente in clientes):
            raise RuntimeError("Un hilo terminó sin registrar su resultado.")

        aceptadas = [c.name for c in clientes if c.aceptada]
        rechazadas = [c.name for c in clientes if not c.aceptada]
        estado = recurso.disponibles if tipo == "entero" else recurso.registro
        return aceptadas, rechazadas, estado


if __name__ == "__main__":
    simulador = Simulador()
    print("Una impresora disponible y dos solicitudes: S1 y S2.")
    for tipo in ("entero", "diccionario"):
        for sincronizado in (False, True):
            aceptadas, rechazadas, estado = simulador.ejecutar(tipo, sincronizado)
            modo = "con Lock" if sincronizado else "sin Lock"
            print(f"\n{tipo} / {modo}")
            print(f"  Aceptadas ({len(aceptadas)}): {', '.join(aceptadas) or '-'}")
            print(f"  Rechazadas: {', '.join(rechazadas) or '-'}")
            print(f"  Estado final: {estado}")
