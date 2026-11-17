import sys

from simulador import Simulador


def main():
    print("=== SISTEMA DE IMPRESORAS EN RED ===")
    print("Dos clientes intentan reservar la última impresora.")
    simulador = Simulador()

    for tipo in ("entero", "diccionario"):
        for sincronizado in (False, True):
            modo = "con mutex" if sincronizado else "sin mutex"
            print(f"\n--- {tipo.upper()} | {modo} ---")
            try:
                aceptadas, rechazadas, estado = simulador.ejecutar(tipo, sincronizado)
            except (RuntimeError, ValueError) as exc:
                print(f"[ERROR DE EJECUCIÓN] {exc}", file=sys.stderr)
                return 1

            for solicitud in aceptadas:
                print(f"  [ACEPTADA] {solicitud}: se registró la reserva.")
            for solicitud in rechazadas:
                print(f"  [RECHAZADA] {solicitud}: no quedan impresoras libres.")

            if isinstance(estado, int):
                print(f"  Cupos libres al finalizar: {estado}.")
            else:
                for impresora, solicitud in estado.items():
                    detalle = "libre" if solicitud is None else f"asignada a {solicitud}"
                    print(f"  Impresora {impresora}: {detalle}.")

            if len(aceptadas) > 1:
                print("  [DOBLE RESERVA] Dos clientes obtuvieron un solo cupo.")
            else:
                print("  [RESULTADO CORRECTO] Solo se aceptó una reserva.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
