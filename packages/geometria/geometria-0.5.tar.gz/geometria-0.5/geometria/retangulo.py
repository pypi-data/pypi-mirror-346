def area_retangulo(base, altura):
    if base <= 0 or altura <= 0:
        return "Digite um valor de entrada válido"
    return base * altura


def perimetro(base, altura):
    if base <= 0 or altura <= 0:
        return "Digite um valor de entrada válido"
    return 2 * (base + altura)

