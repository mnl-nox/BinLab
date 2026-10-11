# Interface gráfica

O BinLab oferece uma interface desktop opcional feita com Tkinter, incluído na biblioteca padrão do Python. Após instalar o pacote, inicie com:

```bash
binlab-gui
```

No checkout, use `PYTHONPATH=src python3 -m binlab.gui`. Se Tkinter não estiver instalado pela distribuição Linux, instale o pacote de sistema correspondente (frequentemente chamado `python3-tk`).

A interface usa uma paleta clara com texto escuro, azul de alto contraste para ações e estados selecionados, além de contornos visíveis nos campos. Os controles preservam navegação por teclado e indicadores de foco. O monograma do projeto é `BL`.

## Abas

- **Conversor:** transforma inteiros entre binário, octal, decimal e hexadecimal e mostra as representações relacionadas.
- **Calculadora:** operações aritméticas, lógicas e deslocamentos com operandos binários.
- **Análise de bits:** largura, valor sem sinal, complemento de dois, hexadecimal, contagem de bits e ASCII por byte.
- **Leitor de arquivos:** seleciona fontes C/assembly, dumps HEX/Intel HEX e binários para leitura estática; HEX pode ser desassemblado com `objdump` após informar a arquitetura.

A GUI não executa nem compila os arquivos selecionados. A análise e as limitações são as mesmas descritas em [leitor.md](leitor.md).
