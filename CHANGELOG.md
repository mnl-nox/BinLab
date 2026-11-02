# Histórico de alterações

Este projeto segue [Semantic Versioning](https://semver.org/).

## Não lançado

### Segurança
- Limites de leitura aplicados durante a leitura de fontes, binários e arquivos HEX.
- Parser Intel HEX agora exige EOF único e terminal, valida tipos e campos, rejeita sobreposição e limita linhas/registros, endereços, lacunas e span decodificado.
- Extração de strings limitada incrementalmente a 30 ocorrências.
- Saída de objdump limitada durante a execução, com timeout, pipes drenados concorrentemente, stdin fechado e ambiente reduzido.
- Operações de domínio validam tipos em runtime e limitam operandos, largura de NOT, shifts e sequências binárias.
- Testes de regressão e abuso adicionados para entradas grandes, Intel HEX malformado, saída excessiva e timeout de subprocesso.

### Documentação
- Modelo de ameaças, contratos e README atualizados com limites e controles do leitor.

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
