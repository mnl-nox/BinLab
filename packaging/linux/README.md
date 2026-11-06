# BinLab Engineering @VERSION@

O BinLab é uma ferramenta local de aprendizagem sobre sistemas numéricos, operações bit a bit e inspeção estática de artefatos computacionais.

## Iniciar a aplicação

- Execute `binlab` para abrir o menu no terminal.
- Execute `binlab-gui` para abrir a interface desktop em uma sessão gráfica.
- Em ambientes compatíveis, o atalho **BinLab Engineering** também aparece no menu de aplicativos.

As interfaces incluem conversão de bases, aritmética inteira, operações bit a bit, análise de bits e leitura estática de arquivos.

## Inspeção de arquivos

O leitor inspeciona fontes C e Assembly, arquivos HEX e Intel HEX e arquivos binários. Arquivos importados não são executados nem compilados. O GNU `objdump` é opcional e só é usado quando a desassemblagem é solicitada.

O leitor aplica limites de 2 MiB para fontes, 8 MiB para binários, 4 MiB para texto HEX e 64 KiB para saída de desassemblagem. Inspeção estática não é uma sandbox; não use o BinLab para executar arquivos não confiáveis.

## Plataforma

Este pacote destina-se a Linux x86_64 com glibc 2.14 ou superior. A interface gráfica requer uma sessão desktop com X11 ou XWayland e as bibliotecas gráficas indicadas pelo gerenciador de pacotes. No tarball, talvez seja necessário instalar essas bibliotecas manualmente.

Esta versão não inclui pacotes para Windows, macOS, ARM64 ou Alpine/musl.

## Projeto e suporte

- Código-fonte e guia de uso: <https://github.com/mnl-nox/BinLab>
- Problemas e sugestões: <https://github.com/mnl-nox/BinLab/issues>
- Relato de vulnerabilidades: <https://github.com/mnl-nox/BinLab/blob/main/SECURITY.md>
- Licença: consulte o arquivo `LICENSE` instalado junto deste documento.
