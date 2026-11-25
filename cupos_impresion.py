from contextlib import nullcontext
from threading import Lock


class CuposImpresion:
    """Representa la disponibilidad total con un entero."""

    def __init__(self, total: int, sincronizado: bool):
        self.disponibles: int = total
        self._mutex = Lock() if sincronizado else None

    def reservar(self, solicitud: str, pausa_demostracion=None, evento=None) -> bool:
        with self._mutex if self._mutex is not None else nullcontext():
            # SECCIÓN CRÍTICA: consultar, validar y descontar el cupo.
            cupos = self.disponibles
            if evento is not None:
                evento['antes'] = cupos
            if pausa_demostracion is not None:
                pausa_demostracion.wait()
            if cupos <= 0:
                if evento is not None:
                    evento['despues'] = self.disponibles
                return False
            # Sin Lock, ambos pueden escribir 0 a partir de la misma lectura.
            self.disponibles = cupos - 1
            if evento is not None:
                evento['despues'] = self.disponibles
            return True
