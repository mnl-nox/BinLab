# Gestão das entregas

Cada etapa do BinLab Engineering será entregue por pull request independente, preferencialmente em branches `feat/...` ou `stage/...`. A branch principal deve permanecer instalável e testável.

## Definition of Done

- Escopo e critérios de aceite atendidos.
- Testes unitários, integração e regressão aplicáveis executados.
- Contratos e documentação atualizados.
- Segurança revisada para entradas, I/O, subprocessos e permissões.
- Dependências justificadas e versões compatíveis registradas.
- CI verde; nenhum segredo ou dado local commitado.
- Limitações e rollback descritos.
- Nenhuma etapa futura é simulada como concluída por meio de diretórios vazios ou stubs.

## Status

- Etapa 0 — em execução nesta branch.
- Etapas 1–10 — planejadas; não implementadas.
