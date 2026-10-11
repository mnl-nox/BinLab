# Contribuindo

1. Crie uma branch de funcionalidade no formato `feat/nome-curto`.
2. Mantenha as mudanças focadas e atualize a documentação quando alterar comportamento.
3. Verifique localmente com `python -m compileall -q src` e `python -m pip install .`.
4. Envie a branch e abra um pull request para `main`.

Cada push para `feat/*` recebe uma tag automática `feat/<branch>/<sha>`. Essa tag identifica o commit e não representa uma versão de release.

## Mensagens de commit

Use mensagens curtas no padrão Conventional Commits:

```text
feat: adiciona conversão hexadecimal
fix: valida checksum Intel HEX
docs: explica leitura de assembly
refactor: separa leitor estático da interface
```

## Versões

O projeto usa Semantic Versioning. Atualize `src/binlab/__init__.py` e o `CHANGELOG.md`, então crie uma tag de release `vX.Y.Z`. O workflow constrói as distribuições e publica o GitHub Release automaticamente.
