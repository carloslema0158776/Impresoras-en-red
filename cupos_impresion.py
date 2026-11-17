from contextlib import nullcontext
from threading import Lock


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
