# Geometria (Em construção)

**Geometria** é uma biblioteca Python para cálculos geométricos, como áreas, perímetros, e outras propriedades de figuras geométricas.

## Funcionalidades

- Cálculo da área de triângulos (incluindo equiláteros) e retângulos.
- Cálculo do perímetro de triângulos e retângulos.
- Verificação da existência de triângulos com base nos lados.
- Cálculo de propriedades avançadas de triângulos:
  - Fórmula de Heron.
  - Altura do triângulo.
  - Raio do círculo inscrito e circunscrito.
  - Ângulos internos.
  - Tipo do triângulo (Equilátero, Isósceles, Escaleno).

---

## Instalação

Você pode instalar a biblioteca diretamente do PyPI:

```bash
pip install geometria
```

## Como Usar
Exemplo de Uso
```
from geometria import area_triangulo, area_triangulo_equilatero, tipo_triangulo

# Área de um triângulo
print(area_triangulo(10, 5))  # Saída: 25.0

# Área de um triângulo equilátero
print(area_triangulo_equilatero(12))  # Saída: 62.35

# Tipo do triângulo
print(tipo_triangulo(3, 4, 5))  # Saída: Escaleno
```

### Desenvolvimento
Pré-requisitos
Certifique-se de ter o Python 3.9 ou superior instalado. Instale as dependências do projeto:
```
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

Rodando os Testes
Para executar os testes unitários, utilize o comando:
```
pytest tests/
```

Cobertura de Testes
Para verificar a cobertura de testes, execute:
```
coverage run -m pytest
coverage report
coverage html
```

O relatório HTML será gerado na pasta htmlcov.

### Contribuindo
Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

Faça um fork do repositório.
```
git checkout -b minha-feature
```

Faça as alterações e adicione os commits.
Envie um pull request para o repositório principal.

Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

Contato
Criado por Mayumi Shingaki.
E-mail: contato.mayulabs@gmail.com