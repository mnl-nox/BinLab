# Arquitetura

BinLab é organizado como pacote Python com interface de terminal, lógica de operações e leitor de artefatos. O fluxo esperado é entrada do usuário → validação → operação/leitura → apresentação de resultados.

```text
src/binlab/
├── domain/              regras puras e API reutilizável
│   ├── numeric.py       parsing e conversão de bases
│   ├── operations.py    aritmética, lógica e shifts
│   └── analysis.py      interpretação de sequências de bits
├── cli.py               adaptador de terminal
├── gui.py               adaptador desktop opcional em Tkinter
├── artifact_reader.py   leitura estática e relatórios de arquivos
├── __main__.py          execução com python -m binlab
└── __init__.py          versão do pacote
```

## Módulos

- `domain/` não depende do terminal, Tkinter, arquivos ou bibliotecas externas. A API pública fica disponível em `binlab.domain`.
- `cli.py` e `gui.py` são adaptadores: validam/recebem entradas, chamam o domínio e formatam resultados para cada interface. A GUI não importa a CLI.
- `artifact_reader.py` contém os casos de uso de inspeção de arquivos; retorna relatórios em texto em vez de escrever diretamente no terminal, para que os dois adaptadores possam reutilizá-lo.
- O leitor chama `objdump` como processo externo somente para desassemblagem estática.
- `__main__.py` e o script de console `binlab` encaminham para a mesma função `main`.
- `gui.py` disponibiliza o comando `binlab-gui`; a interface gráfica é importada separadamente e não é exigida pelo CLI.
- `src/halfAdder.py` preserva compatibilidade com o caminho de execução antigo.

![Diagrama de componentes](../images/architecture.svg)

O pacote usa apenas a biblioteca padrão do Python em tempo de execução. O `pyproject.toml` define metadados, versão, construção e comandos de console. A versão fica em `binlab.__version__` e é consumida dinamicamente durante a construção do pacote.

Exemplo de uso da API sem interface:

```python
from binlab.domain import analyze_bits, calculate, convert_integer

print(convert_integer("2A", 16, 2))
print(calculate(10, "XOR", 3))
print(analyze_bits("01000001").ascii_text)
```

Os testes unitários em `tests/` usam essa mesma API pública e o leitor de artefatos. Execute-os com `python -m unittest discover -s tests -v`; o CI roda a suíte em cada versão Python da matriz.
