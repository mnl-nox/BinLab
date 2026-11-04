# Code review e preparação de distribuição Linux — 2026-11-04

## Escopo

Revisão estática da branch principal e do estado dos workflows, domínio TypeScript, leitor Python, metadados do pacote e processo de release. A revisão não substitui execução em ambiente Linux limpo, teste de instalação em distribuições suportadas, fuzzing de longo prazo ou auditoria independente.

## Achados tratados nesta entrega

### BL-WEB-001 — Dependência Vitest atualizada sem validação de CI

- Evidência: a atualização para Vitest 4.1.11 foi seguida por falha do job Web durante `npm install`, com `Cannot read properties of null (reading 'edgesOut')`.
- Correção: retornar Vitest para 2.1.8, a versão anterior conhecida por ter passado no CI, mantendo o restante do toolchain fixado.
- Validação pendente: executar novamente instalação, testes e build em runner limpo.

### BL-WEB-002 — Separadores numéricos eram removidos antes da validação

- Evidência: `replaceAll("_", "")` aceitava entradas como `_10`, `10_` e `1__0`.
- Correção: validar separadores somente entre dígitos válidos da base antes de normalizar.
- Testes adicionados: separadores válidos, posições inválidas, sinal, base inválida e round-trip.

### BL-WEB-003 — Erros de domínio eram ocultados na interface

- Evidência: a interface convertia qualquer exceção em `null` e exibia uma mensagem genérica.
- Correção: preservar mensagens de validação e apresentar erros acessíveis via `role=alert`.

### BL-SEC-007 — Ausência de testes property-based

- Evidência: testes unitários determinísticos não exploravam sistematicamente o espaço de entradas.
- Correção: adicionar Hypothesis como dependência opcional de teste e propriedades para round-trip numérico, operações bitwise, parsing hexadecimal bruto, registros Intel HEX válidos e checksums corrompidos.
- Limite: esses testes não substituem fuzzing especializado contínuo, fuzzing dos subprocessos nativos ou revisão independente do parser.

### BL-CI-003 — Referência mutável de GitHub Action

- Evidência: `feature-tags.yml` utilizava `actions/checkout@v7`, enquanto os demais workflows já utilizavam SHA completo.
- Correção: fixar checkout no SHA oficial v7.0.1 e restringir `contents: write` ao job que cria tags. O workflow de release também passa a limitar escrita ao job de publicação.

### BL-PKG-001 — Ausência de instaladores Linux

- Correção proposta: criar entrypoints PyInstaller e pipeline FPM para .deb e .rpm, além de tarball portátil com árvore /usr.
- Escopo: primeira linha x86_64, construída em Ubuntu 22.04.
- Limite: não declara suporte ARM64, AppImage, Flatpak nem instalação validada em distribuições alvo nesta etapa.

## Distribuição Linux proposta

A primeira distribuição binária é x86_64, construída em Ubuntu 22.04 para manter uma baseline de glibc conservadora. O pipeline produz:
- Debian package `.deb`;
- RPM `.rpm`;
- arquivo portátil `.tar.gz` com árvore `usr/`.

Os executáveis CLI e GUI são empacotados com PyInstaller. O pacote GUI depende de bibliotecas gráficas do host e de uma sessão X11/XWayland.

## Riscos e validações ainda necessárias

1. Executar CI após as alterações e investigar qualquer falha residual.
2. Confirmar se PyInstaller inclui corretamente Tcl/Tk no runner escolhido.
3. Instalar .deb em Debian/Ubuntu limpos e validar CLI e GUI.
4. Instalar .rpm em Fedora/RHEL compatível e validar dependências.
5. Validar extração e execução do tarball em uma distribuição não Debian.
6. Gerar hashes SHA-256 e, em etapa posterior, SBOM e attestations.
7. Encerrar Issue #2 somente após fuzzing Intel HEX mais amplo e revisão de segurança complementar.
8. Encerrar Issue #3 somente após confirmar todas as referências `uses:` fixadas e permissões mínimas.

## Status

Esta revisão documenta alterações propostas na branch de release. Não afirma que os pacotes já foram construídos ou instalados com sucesso. A release só deve ser criada depois de CI verde e validação dos artefatos.
