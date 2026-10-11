# Leitor estático de arquivos

Escolha a opção **Leitor de arquivos C/assembly/binário/hex** no menu e informe o caminho. O leitor seleciona o modo de acordo com a extensão:

| Extensão | Leitura |
|---|---|
| `.c`, `.h`, `.cc`, `.cpp`, `.cxx` | Mostra o início do fonte e contagens aproximadas de includes, macros, funções e tipos. |
| `.s`, `.S`, `.asm` | Mostra o início e contagens heurísticas de instruções, labels e diretivas. |
| `.hex`, `.ihex` | Interpreta hexadecimal em texto ou registros Intel HEX e analisa os bytes resultantes. |
| Outras extensões | Trata o conteúdo como bytes e mostra informações estáticas. |

## Arquivos binários

O relatório inclui tamanho, SHA-256, assinatura provável para ELF, MZ/PE, Mach-O e WebAssembly, dump hexadecimal dos primeiros 512 bytes e até 30 strings ASCII. Se GNU `objdump` estiver instalado, também tenta mostrar formato, seções e desassemblagem (`-f -h -d`). A saída do desassembler é limitada; formatos ou arquiteturas não reconhecidos podem não produzir instruções.

## Texto hexadecimal

Um dump bruto pode usar bytes separados por espaço, vírgula, dois-pontos ou sublinhado, por exemplo `DE AD BE EF` ou `0xDE, 0xAD, 0xBE, 0xEF`. O formato Intel HEX (`.hex`/`.ihex`) valida tamanho e checksum dos registros de dados e entende endereços estendidos. Registros de dados esparsos são preenchidos com zeros no resultado linear. Após o relatório, é possível pedir disassemblagem dos bytes informando a arquitetura reconhecida pela instalação do `objdump` (por exemplo `i386:x86-64`, `i386`, `arm` ou `aarch64`); deixe em branco para ignorar.

## O que significa “ler” C e assembly

Arquivos-fonte C são texto; as estatísticas são heurísticas e não substituem compilador ou parser da linguagem. Arquivos de assembly também são apresentados como texto, pois a sintaxe depende do assembler e da arquitetura. Um executável compilado não preserva necessariamente nomes, comentários ou o código C original. `objdump` faz desassemblagem estática quando consegue identificar o formato e a arquitetura, mas não reconstrói o fonte original.

O leitor nunca executa nem compila o arquivo. A análise é informativa e não valida a segurança do conteúdo.
