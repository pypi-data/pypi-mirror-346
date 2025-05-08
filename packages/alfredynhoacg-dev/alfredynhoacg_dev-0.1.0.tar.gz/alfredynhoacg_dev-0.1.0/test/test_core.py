import unittest
from alfred import saludar

class TestMiLibreria(unittest.TestCase):
    def test_saludar(self):
        self.assertEqual(saludar("Mundo"), "Hola, Mundo! Bienvenido a tu primera librería.")