import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from interfaz_consola import InterfazConsola
from simulador import Simulador


class PruebasInterfaz(unittest.TestCase):
    def test_parametros_y_cuatro_versiones(self):
        for clientes, impresoras in [(2, 1), (5, 3), (2, 5), (20, 10)]:
            for tipo in ('entero', 'diccionario'):
                for mutex in (False, True):
                    with self.subTest(clientes=clientes, impresoras=impresoras,
                                      tipo=tipo, mutex=mutex):
                        r = Simulador().ejecutar(tipo, mutex, clientes, impresoras, True)
                        self.assertEqual(len(r['eventos']), clientes)
                        self.assertEqual(len(r['aceptadas']),
                                         min(clientes, impresoras) if mutex else clientes)
                        self.assertEqual(r['carrera'], not mutex)
                        for e in r['eventos']:
                            self.assertIn('antes', e)
                            self.assertIn('despues', e)
                        if tipo == 'diccionario':
                            self.assertIsNot(r['eventos'][0]['antes'], r['estado_final'])

    def test_configuracion_invalida(self):
        for clientes, impresoras in [(1, 1), (21, 1), (2, 0), (2, 11)]:
            with self.assertRaises(ValueError):
                Simulador().ejecutar('entero', True, clientes, impresoras)

    def test_menu_completo(self):
        entradas = ['texto', '99', '1', '1', '3', '0', '2',
                    '2', '3', '4', '5', '6', '0']
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas), redirect_stdout(salida):
            self.assertEqual(InterfazConsola().ejecutar(), 0)
        texto = salida.getvalue()
        for fragmento in ('DATO NO VÁLIDO', 'Hilo: S3', 'Antes:', 'Después:',
                          'ESTADO FINAL', 'COMPARACIÓN', 'Simulador cerrado'):
            self.assertIn(fragmento, texto)

    def test_entrada_cerrada(self):
        with patch('builtins.input', side_effect=EOFError), redirect_stdout(io.StringIO()):
            self.assertEqual(InterfazConsola().ejecutar(), 0)


if __name__ == '__main__':
    unittest.main()
