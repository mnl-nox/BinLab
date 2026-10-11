# Execução e uso

Execute a partir do diretório do projeto:

```bash
python3 src/halfAdder.py
```

Para usar a interface gráfica, instale o pacote com `python -m pip install .` e execute `binlab-gui`. Consulte [gui.md](gui.md) para conhecer as abas.

O menu fica ativo até selecionar `0. Sair`. Uma entrada inválida mostra uma mensagem e permite tentar novamente.

Para ler um arquivo C, assembly, binário ou hexadecimal, escolha a opção 7 e informe o caminho. Os detalhes estão em [leitor.md](leitor.md).

## Exemplo: soma

Para somar `101` (5) e `11` (3), escolha a opção de aritmética, informe os dois números e use `+`. O resultado é `1000` (8).

## Exemplo: divisão inteira

`1101` dividido por `10` com `//` resulta em `110` (6), descartando o resto. A operação `%` retorna o resto, que neste caso é `1`.

## Entrada

- Binários aceitam os dígitos `0` e `1`, com sublinhado opcional entre grupos.
- A conversão decimal aceita inteiros, inclusive negativos.
- A quantidade de posições de deslocamento deve ser um inteiro não negativo.
- Divisão inteira e resto por zero são recusados.
