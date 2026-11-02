# Objetivo e escopo atual

BinLab é uma calculadora e leitor didático para explorar inteiros em binário, octal, decimal e hexadecimal e fazer inspeção estática básica de código-fonte e arquivos de bytes.

A versão atual é **0.3.1**. O sistema cobre aritmética inteira, operações lógicas bit a bit, deslocamentos, conversões entre bases, tabela verdade e leitura estática de fontes C/assembly, dumps HEX e alguns formatos binários. A interface desktop usa Tkinter; não há dependências Python de terceiros em tempo de execução. A desassemblagem usa GNU `objdump` opcionalmente.

## Limites da representação

As entradas das operações bit a bit são inteiros não negativos. A subtração pode produzir um resultado negativo; nesse caso, a aplicação mostra o sinal seguido da magnitude binária. A análise de sequência binária interpreta seu primeiro bit como sinal em complemento de dois com a largura informada. O leitor é estático e educacional: não executa nem compila arquivos. As estatísticas de C/assembly são heurísticas, e o suporte à desassemblagem depende do formato e da arquitetura aceitos por `objdump`.

## Escopo futuro

A visão BinLab Engineering e suas etapas de entrega estão descritas em [docs/ROADMAP.md](../docs/ROADMAP.md). Web, API, Tauri, persistência e laboratórios avançados são planejamento, não funcionalidades presentes na versão 0.3.1.
