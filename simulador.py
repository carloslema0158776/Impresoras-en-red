from threading import Barrier

from cupos_impresion import CuposImpresion
from hilo_cliente import HiloCliente
from registro_impresoras import RegistroImpresoras


class Simulador:
    """Crea una instancia por prueba y se la pasa a los dos clientes."""

    def ejecutar(self, tipo: str, sincronizado: bool, clientes: int = 2,
                 impresoras: int = 1, detallado: bool = False):
        if type(clientes) is not int or not 2 <= clientes <= 20:
            raise ValueError('La cantidad de clientes debe ser un entero entre 2 y 20.')
        if type(impresoras) is not int or not 1 <= impresoras <= 10:
            raise ValueError('La cantidad de impresoras debe ser un entero entre 1 y 10.')
        if tipo == "entero":
            recurso = CuposImpresion(impresoras, sincronizado)
        elif tipo == "diccionario":
            recurso = RegistroImpresoras([f'P{i+1}' for i in range(impresoras)], sincronizado)
        else:
            raise ValueError(f"Tipo de recurso no válido: {tipo!r}. Usa entero o diccionario.")

        # Solo para reproducir la carrera: ambos leen antes de escribir.
        pausa = None if sincronizado else Barrier(clientes, timeout=10)
        clientes = [HiloCliente(f'S{i+1}', recurso, pausa) for i in range(clientes)]
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
        if detallado:
            ocupadas = impresoras - estado if tipo == 'entero' else sum(s is not None for s in estado.values())
            return {'tipo': tipo, 'sincronizado': sincronizado,
                    'aceptadas': aceptadas, 'rechazadas': rechazadas,
                    'estado_final': estado, 'ocupadas': ocupadas,
                    'carrera': len(aceptadas) != ocupadas,
                    'eventos': sorted((c.evento for c in clientes), key=lambda e: e['fin'])}
        return aceptadas, rechazadas, estado
