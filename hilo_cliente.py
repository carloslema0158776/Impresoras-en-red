from threading import BrokenBarrierError, Thread


class HiloCliente(Thread):
    """Única clase de hilo: pide una reserva y guarda su resultado."""

    def __init__(self, solicitud, recurso, pausa_demostracion=None):
        super().__init__(name=solicitud)
        self.recurso = recurso
        self.pausa_demostracion = pausa_demostracion
        self.aceptada = None
        self.error = None

    def run(self):
        try:
            self.aceptada = self.recurso.reservar(self.name, self.pausa_demostracion)
        except BrokenBarrierError:
            self.error = "No se pudo reproducir la prueba: ambos clientes no llegaron a tiempo."
        except Exception as exc:
            self.error = f"No se pudo intentar la reserva ({exc})."
            if self.pausa_demostracion is not None:
                self.pausa_demostracion.abort()
