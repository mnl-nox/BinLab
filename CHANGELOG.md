# Histórico de alterações

Este projeto segue [Semantic Versioning](https://semver.org/).

## 0.3.2 — 2026-11-04

### Website
- Adicionado site institucional estático, responsivo e acessível em `website/`.
- Incluídos visão do produto, laboratórios, arquitetura, segurança, instalação e roadmap.
- Adicionados alternância de tema, navegação móvel, página 404 e validação de referências locais.
- Criado workflow de publicação GitHub Pages com actions fixadas por SHA.
- Política de privacidade ampliada para cobrir o site institucional e a fundação Web local.

### Web
- Criada a fundação React + TypeScript + Vite + Tailwind CSS em `apps/web/`.
- Adicionada navegação responsiva entre laboratórios e alternância de tema independente.
- Implementado conversor de bases e operações AND/OR/XOR/shift-left locais com BigInt.
- Adicionados limites de entrada e largura de operandos/resultados no domínio Web.
- Revertida a atualização de Vitest 4.1.11 para 2.1.8 após falha de instalação no CI.
- Parsing numérico em Python e TypeScript agora valida separadores somente entre dígitos válidos da base.
- Mensagens de erro do domínio são preservadas e exibidas na interface.
- Ampliada a cobertura de testes para sinais, separadores, bases inválidas, precisão e operações bit a bit.
- Laboratórios ainda não implementados são identificados como planejados; não há integração com API.

### Linux packaging
- Adicionados entrypoints PyInstaller para CLI e GUI Tkinter.
- Adicionado pipeline de release Linux x86_64 com pacotes `.deb`, `.rpm` e tarball portátil.
- Definida baseline de build Ubuntu 22.04; suporte ARM64, AppImage e Flatpak permanece fora da primeira entrega.

### CI
- Pipeline valida testes e build da aplicação Web em Node.js 20.
- Branches `feature/**` incluídas no gatilho de push.
- Adicionado job Linux para construir e inspecionar pacotes .deb, .rpm e tar.gz.
- Fixada a referência `actions/checkout` do workflow de tags de feature por SHA completo.
- Permissões de escrita dos workflows de tags e release limitadas aos jobs que precisam delas.

### Segurança
- Limites de leitura aplicados durante a leitura de fontes, binários e arquivos HEX.
- Parser Intel HEX exige EOF único e terminal, valida tipos e campos, rejeita sobreposição e limita linhas/registros, endereços, lacunas e span decodificado.
- Extração de strings limitada incrementalmente a 30 ocorrências.
- Saída de objdump limitada durante a execução, com timeout, pipes drenados concorrentemente, stdin fechado e ambiente reduzido.
- Operações de domínio validam tipos em runtime e limitam operandos, largura de NOT, shifts e sequências binárias.
- Adicionados testes property-based com Hypothesis para round-trip numérico, operações lógicas, HEX bruto, Intel HEX válido e checksum corrompido.
- A dependência Hypothesis é opcional e instalada somente no extra `test`.

### Documentação
- README consolidado, removendo seções duplicadas e separando recursos atuais de planejados.
- Documentadas arquitetura, execução, limites, estado da aplicação Web e distribuição Linux.
- Adicionado relatório de code review de 4 de novembro de 2026.

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
