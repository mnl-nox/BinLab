# Referência das operações

Considere `A = 1010₂` (10) e `B = 0011₂` (3). Zeros à esquerda podem ser usados para facilitar a leitura; a calculadora não exige que os operandos tenham o mesmo comprimento.

## Aritmética

| Operador | Significado | Exemplo decimal | Resultado |
|---|---|---:|---:|
| `+` | soma | 10 + 3 | 13 (`1101₂`) |
| `-` | subtração | 10 - 3 | 7 (`111₂`) |
| `*` | multiplicação | 10 × 3 | 30 (`11110₂`) |
| `//` | divisão inteira, descarta fração | 10 // 3 | 3 (`11₂`) |
| `%` | resto da divisão inteira | 10 % 3 | 1 (`1₂`) |

## Lógica bit a bit

| Operação | Regra | Exemplo (`1010` e `0011`) |
|---|---|---|
| `AND` | bit é 1 se ambos são 1 | `0010` |
| `OR` | bit é 1 se ao menos um é 1 | `1011` |
| `XOR` | bit é 1 se os bits diferem | `1001` |
| `NOT` | inverte cada bit na largura escolhida | `NOT(1010)` em 4 bits = `0101` |

## Deslocamento

Deslocar à esquerda (`<<`) uma posição equivale a multiplicar por 2; deslocar à direita (`>>`) equivale a dividir por 2 e descartar a fração para valores não negativos. Por exemplo, `1010 << 1 = 10100` e `1010 >> 1 = 101`.

## Conversão e tabela verdade

As conversões permitem transformar um inteiro binário em decimal e um inteiro decimal em binário. A tabela verdade enumera as quatro combinações de entrada de um bit para AND, OR, XOR e NOT. No meio somador, `SUM = A XOR B` e `CARRY = A AND B`.
