# Contribuindo

1. Crie uma branch de trabalho no padrão `feat/nome-curto`, `stage/nome-curto` ou `architecture/nome-curto`.
2. Mantenha mudanças focadas em uma etapa/entrega.
3. Atualize documentação, contratos e testes no mesmo pull request.
4. Execute localmente:

```bash
python -m compileall -q src tests
python -m pip install .
python -m unittest discover -s tests -v
python -m pip install build
python -m build
``

5. Envie a branch e abra pull request para `main`. Não integre etapas incompletas sem explicitar bloqueios e riscos.

Branches `feat/*` recebem tags automáticas por commit. Tags de feature são referências de rastreabilidade, não releases.

## Critérios de revisão

- Responsabilidade única e dependências apontando para dentro.
- Contratos explícitos e compatibilidade considerada.
- Entradas externas validadas e limites de recursos definidos.
- Nenhuma execução automática de arquivos importados.
- Testes de regressão e documentação atualizados.
- Dependências novas justificadas.

## Mensagens de commit

Use Conventional Commits:

```text
feat: adiciona conversão hexadecimal
fix: valida checksum Intel HEX
docs: explica leitura de assembly
refactor: separa leitor estático da interface
```

## Versões

O projeto usa Semantic Versioning. Atualize `src/binlab/__init__.py` e `CHANGELOG.md`, então crie uma tag `vX.Y.Z`. O workflow de release valida a correspondência e publica as distribuições.
