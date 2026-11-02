# Histórico de alterações

Este projeto segue [Semantic Versioning](https://semver.org/).

## Não lançado

### Segurança e documentação

- Auditoria estática documentada com achados e critérios de bloqueio para a futura API.
- Política de privacidade da versão 0.3.1 e escopo da licença MIT documentados.
- README atualizado para não carregar badges remotos de terceiros.
- Metadados do pacote agora apontam para repositório, issues e canal de segurança.
- Workflow de release reforçado para executar testes antes de publicar.

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
