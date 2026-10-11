# Objetivo e escopo

BinLab é uma calculadora e leitor didático para explorar inteiros em binário, octal, decimal e hexadecimal e fazer inspeção estática básica de código-fonte e arquivos de bytes. O programa recebe valores pelo terminal e apresenta operações, conversões e propriedades das sequências analisadas.

O projeto está na versão 0.2.0. A arquitetura e a organização dos módulos estão descritas em [architecture.md](architecture.md). O sistema cobre aritmética inteira, operações lógicas bit a bit, deslocamentos, conversões entre bases, tabela verdade e leitura estática de fontes C/assembly, dumps hex e alguns formatos binários. Não depende de pacotes Python de terceiros em tempo de execução; desassemblagem usa GNU `objdump` opcionalmente.

## Limites da representação

As entradas das operações bit a bit são inteiros não negativos. A subtração pode produzir um resultado negativo; nesse caso, a aplicação mostra o sinal seguido da magnitude binária. A análise de sequência binária interpreta seu primeiro bit como sinal em complemento de dois com a largura informada. O leitor é estático e educacional: não executa nem compila arquivos. As estatísticas de C/assembly são heurísticas, e o suporte à desassemblagem depende do formato e da arquitetura aceitos por `objdump`.
