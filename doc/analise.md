# Conversões e análise de sequências

## Tradutor de bases

No menu, selecione **Conversão de bases**, informe a base de origem e a base de destino (`2`, `8`, `10` ou `16`) e digite o valor. Para hexadecimal, use os dígitos `0`–`9`, `A`–`F` ou `a`–`f`. Prefixos `0b`, `0o`, `0d` e `0x` são opcionais e removidos quando correspondem à base escolhida. Sublinhados são aceitos como separadores visuais.

Exemplo: origem `16`, destino `2`, valor `0x2A` produz `101010`.

## Interpretador de sequência binária

Selecione **Análise de sequência binária** e informe os bits, por exemplo `0100_0001`. A largura é preservada, inclusive zeros à esquerda. O relatório mostra:

- largura da sequência em bits;
- valor inteiro sem sinal;
- interpretação em complemento de dois, usando o bit mais à esquerda como sinal;
- forma hexadecimal preenchida para representar todos os bits;
- contagem de zeros e uns;
- bytes em hexadecimal e caracteres ASCII imprimíveis se a largura for múltipla de oito.

Para bytes fora do intervalo ASCII imprimível, o relatório usa `.`. Em comprimentos que não formam bytes completos, o campo ASCII é omitido. O interpretador analisa uma sequência fornecida pelo usuário; ele não abre ou executa arquivos.

## Exemplos

| Bits | Sem sinal | Complemento de dois | Hexadecimal |
|---|---:|---:|---|
| `01000001` | 65 | 65 | `41` |
| `11111111` | 255 | -1 | `FF` |

A mesma sequência pode ter interpretações diferentes conforme o formato. Por isso, o relatório exibe lado a lado o valor sem sinal e o valor com sinal na largura selecionada.
