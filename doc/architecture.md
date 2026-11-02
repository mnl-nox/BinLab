# Arquitetura atual

BinLab é atualmente um pacote Python com interface de terminal, lógica de operações, interface Tkinter e leitor de artefatos estáticos.

```text
src/binlab/
├── domain/              regras puras e API reutilizável
│   ├── numeric.py       parsing e conversão de bases
│   ├── operations.py    aritmética, lógica e shifts
│   └── analysis.py      interpretação de sequências de bits
├── cli.py               adaptador de terminal
├── gui.py               adaptador desktop Tkinter
├── artifact_reader.py   leitura estática e relatórios
├── __main__.py          execução com python -m binlab
└── __init__.py          versão do pacote
```

## Fronteiras existentes

- `domain/` não depende do terminal, Tkinter, arquivos ou bibliotecas externas.
- `cli.py` e `gui.py` são adaptadores independentes.
- `artifact_reader.py` oferece inspeção estática e relatórios textuais reutilizáveis.
- `__main__.py` e o script `binlab` encaminham para a CLI.
- `src/halfAdder.py` preserva compatibilidade com o caminho antigo.

O pacote usa apenas a biblioteca padrão do Python em tempo de execução. A versão é definida em `binlab.__version__`.

## API de domínio existente

```python
from binlab.domain import analyze_bits, calculate, convert_integer

print(convert_integer("2A", 16, 2))
print(calculate(10, "XOR", 3))
print(analyze_bits("01000001").ascii_text)
```

## Evolução planejada

A arquitetura alvo será um monólito modular: `domain`, `application`, `infrastructure` e `api`, com Web e Desktop como clientes. O domínio atual será preservado e envolvido por serviços de aplicação; não será acoplado diretamente a FastAPI, SQLite ou frameworks de interface.

Consulte [docs/architecture/overview.md](../docs/architecture/overview.md) para regras de dependência e [docs/ROADMAP.md](../docs/ROADMAP.md) para as entregas e critérios de aceite.

## Testes

```bash
python -m unittest discover -s tests -v
```
