from threading import BrokenBarrierError, Thread
from time import monotonic_ns


class HiloCliente(Thread):
    """Única clase de hilo: pide una reserva y guarda su resultado."""

    def __init__(self, solicitud, recurso, pausa_demostracion=None):
        super().__init__(name=solicitud)
        self.recurso = recurso
        self.pausa_demostracion = pausa_demostracion
        self.aceptada = None
        self.error = None
        self.evento = {'hilo': solicitud, 'operacion': 'Reservar una impresora'}

    def run(self):
        try:
            self.aceptada = self.recurso.reservar(self.name, self.pausa_demostracion, self.evento)
        except BrokenBarrierError:
            self.error = "La prueba agotó el tiempo de espera de los clientes. Intenta de nuevo."
        except Exception as exc:
            self.error = f"No se pudo intentar la reserva ({exc})."
            if self.pausa_demostracion is not None:
                self.pausa_demostracion.abort()
        finally:
            self.evento['aceptada'] = self.aceptada
            self.evento['fin'] = monotonic_ns()
