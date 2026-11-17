from threading import Barrier

from cupos_impresion import CuposImpresion
from hilo_cliente import HiloCliente
from registro_impresoras import RegistroImpresoras


class Simulador:
    """Crea una instancia por prueba y se la pasa a los dos clientes."""

    def ejecutar(self, tipo: str, sincronizado: bool):
        if tipo == "entero":
            recurso = CuposImpresion(1, sincronizado)
        elif tipo == "diccionario":
            recurso = RegistroImpresoras(["P1"], sincronizado)
        else:
            raise ValueError(f"Tipo de recurso no válido: {tipo!r}. Usa entero o diccionario.")

        # Solo para reproducir la carrera: ambos leen antes de escribir.
        pausa = None if sincronizado else Barrier(2, timeout=5)
        clientes = [HiloCliente(s, recurso, pausa) for s in ("S1", "S2")]
        for cliente in clientes:
            cliente.start()
        for cliente in clientes:
            cliente.join()
        for cliente in clientes:
            if cliente.error:
                raise RuntimeError(f"Cliente {cliente.name}: {cliente.error}")
            if cliente.aceptada is None:
                raise RuntimeError(f"El cliente {cliente.name} terminó sin registrar su resultado.")

        aceptadas = [c.name for c in clientes if c.aceptada]
        rechazadas = [c.name for c in clientes if not c.aceptada]
        estado = recurso.disponibles if tipo == "entero" else recurso.registro
        return aceptadas, rechazadas, estado
