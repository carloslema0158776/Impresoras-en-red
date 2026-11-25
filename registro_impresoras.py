from contextlib import nullcontext
from threading import Lock


class RegistroImpresoras:
    """Relaciona cada impresora con su solicitud; None indica libre."""

    def __init__(self, ids, sincronizado: bool):
        self.registro: dict[str, str | None] = dict.fromkeys(ids)
        self._mutex = Lock() if sincronizado else None

    def reservar(self, solicitud: str, pausa_demostracion=None, evento=None) -> bool:
        with self._mutex if self._mutex is not None else nullcontext():
            # SECCIÓN CRÍTICA: buscar una impresora, validar y asignarla.
            lectura = self.registro.copy()
            if evento is not None:
                evento['antes'] = lectura
            if pausa_demostracion is not None:
                pausa_demostracion.wait()
            for impresora, asignada in lectura.items():
                if asignada is None:
                    # Sin Lock, la segunda escritura puede borrar la primera.
                    self.registro[impresora] = solicitud
                    if evento is not None:
                        evento['despues'] = self.registro.copy()
                    return True
            if evento is not None:
                evento['despues'] = self.registro.copy()
            return False
