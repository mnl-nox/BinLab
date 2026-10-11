<p align="center">
  <img src="images/binlab-logo.svg" alt="BinLab — Binary, Hex, Code" width="720">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white" alt="CI com GitHub Actions">
  <img src="https://img.shields.io/badge/version-0.2.0-49e3c1" alt="Versão 0.2.0">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776ab?logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Linux-supported-fcc624?logo=linux&logoColor=black" alt="Linux">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="Licença MIT">
</p>

BinLab é uma aplicação de terminal para aprender operações numéricas e lógicas, converter bases e inspecionar estaticamente dados binários, dumps hexadecimais, fontes C e assembly.

## Recursos

- Aritmética inteira e operações lógicas bit a bit.
- Conversão entre binário, octal, decimal e hexadecimal.
- Análise de largura, sinal, bytes e caracteres ASCII.
- Leitura estática de fontes C/assembly, dumps hex e arquivos binários.
- Desassemblagem opcional com GNU `objdump`.

## Requisitos

- Python 3.8 ou superior.
- GNU `objdump` opcional para disassemblagem; sua disponibilidade depende do formato e da arquitetura.

## Instalação e execução

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
binlab
```

Também é possível executar sem instalar, a partir da raiz do repositório:

```bash
python3 src/halfAdder.py
# ou
PYTHONPATH=src python3 -m binlab
```

## Estrutura

```text
src/binlab/        pacote da aplicação e leitor estático
src/halfAdder.py   ponto de entrada legado
doc/               guias de uso, arquitetura, análise e CI/CD
images/            logo e diagrama da arquitetura em SVG
.github/workflows/ integração contínua, tags de feat e releases
```

![Diagrama da arquitetura BinLab](images/architecture.svg)

## Documentação

- [Objetivo e escopo](doc/objetive.md)
- [Arquitetura](doc/architecture.md)
- [Operações e análise](doc/operacoes.md) · [Leitor de arquivos](doc/leitor.md)
- [Uso](doc/case.md) · [Conversões](doc/analise.md)
- [CI/CD, tags e versões](doc/ci-cd.md)
- [Como contribuir](CONTRIBUTING.md) · [Histórico](CHANGELOG.md)

## Limites

O leitor não executa nem compila os arquivos. As estatísticas de C e assembly são heurísticas. Um executável compilado não contém necessariamente o código C original; a desassemblagem depende dos formatos e processadores suportados por `objdump`.
