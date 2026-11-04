# Histórico de alterações

Este projeto segue [Semantic Versioning](https://semver.org/).

## Não lançado

### Linux packaging
- Adicionados entrypoints PyInstaller para CLI e GUI Tkinter.
- Adicionado pipeline de release Linux x86_64 com pacotes `.deb`, `.rpm` e tarball portátil.
- Definida baseline de build Ubuntu 22.04; suporte ARM64, AppImage e Flatpak permanece fora da primeira entrega.

### Web
- Revertida a atualização de Vitest 4.1.11 para 2.1.8 após falha de instalação no CI.
- Parsing numérico agora valida separadores somente entre dígitos válidos da base.
- Mensagens de erro do domínio são preservadas e exibidas na interface.
- Ampliada a cobertura de testes para sinais, separadores, bases inválidas, precisão e operações bit a bit.

### Python / segurança
- Adicionados testes property-based com Hypothesis para round-trip numérico, operações lógicas, HEX bruto, Intel HEX válido e checksum corrompido.
- A dependência Hypothesis é opcional e instalada somente no extra `test`.

### CI / supply chain
- Fixada a referência `actions/checkout` do workflow de tags de feature por SHA completo.
- Permissões de escrita do workflow de tags e release limitadas aos jobs que precisam delas.
- CI passa a construir e inspecionar pacotes Linux em runner Ubuntu 22.04.

## 0.3.1 — 2026-10-11

### Corrigido
- Seletor de arquivos inicia na pasta pessoal do usuário, não na raiz do projeto.
- Falha ao abrir a GUI sem uma sessão gráfica agora apresenta uma orientação legível.
- Documentação da GUI esclarece requisitos de X11/XWayland e a pasta inicial do leitor.

## 0.3.0 — 2026-10-11

### Adicionado
- Interface gráfica desktop em Tkinter com conversor, calculadora, analisador de bits e leitor de arquivos.
- Interface visual simplificada com paleta clara de alto contraste e monograma `BL`.
- Banner ASCII colorido em terminais compatíveis, com suporte à variável `NO_COLOR`.
- Domínio numérico desacoplado das interfaces CLI e GUI, com API reutilizável.
- Testes unitários para domínio e leitura de arquivos, também executados no CI.

## 0.2.0 — 2026-10-11

### Adicionado
- Pacote Python instalável e comando de terminal `binlab`.
- Leitura estática de fontes C/assembly, dumps HEX/Intel HEX e arquivos binários.
- Workflow de CI, tags automáticas em branches `feat/*` e publicação por tag de versão.
- Logo, diagrama SVG e documentação de arquitetura e contribuição.

### Mantido
- Compatibilidade com `python3 src/halfAdder.py`.
