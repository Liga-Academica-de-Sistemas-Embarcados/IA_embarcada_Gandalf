import os
import sys
import unittest

# Garante que o Python encontre a pasta do módulo
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RPI_SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../src/raspberry-pi_src"))
sys.path.insert(0, RPI_SRC_DIR)

from databaseCheck.databaseCheck import checkDatabase


class TestDatabaseCheck(unittest.TestCase):

    def test_placa_autorizada(self):
        # ABC1234 está no JSON -> deve retornar True
        self.assertTrue(checkDatabase("ABC1234"))

    def test_placa_nao_autorizada(self):
        # XYZ5678 não está no JSON -> deve retornar False
        self.assertFalse(checkDatabase("XYZ5678"))

    def test_placa_com_espacos_ou_minuscula(self):
        # Deve tratar espaços e minúsculas
        self.assertTrue(checkDatabase("  abc1234  "))

    def test_entrada_invalida(self):
        # Entrada vazia ou nula
        self.assertFalse(checkDatabase(""))
        self.assertFalse(checkDatabase(None))


if __name__ == "__main__":
    unittest.main()