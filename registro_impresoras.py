from contextlib import nullcontext
from threading import Lock


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
