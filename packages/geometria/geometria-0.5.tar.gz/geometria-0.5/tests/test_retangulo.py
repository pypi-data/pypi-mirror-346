from unittest import TestCase
from geometria import area_retangulo, perimetro_retangulo


class TestRetangulo(TestCase):
    def test_area_retangulo(self):
        assert area_retangulo(10, 20) == 200
        assert area_retangulo(5, 5) == 25

    def test_area_retangulo_invalido(self):
        assert area_retangulo(0, 10) == "Digite um valor de entrada válido"
        assert area_retangulo(-5, 5) == "Digite um valor de entrada válido"

    def test_perimetro_retangulo(self):
        assert perimetro_retangulo(10, 20) == 60
        assert perimetro_retangulo(5, 5) == 20

    def test_perimetro_retangulo_invalido(self):
        assert perimetro_retangulo(0, 10) == "Digite um valor de entrada válido"
        assert perimetro_retangulo(-5, 5) == "Digite um valor de entrada válido"