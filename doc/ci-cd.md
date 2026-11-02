# CI/CD, tags e versões

## Integração contínua

`.github/workflows/ci.yml` executa em pull requests e em pushes para `main`, `feat/**`, `stage/**` e `architecture/**`. Em Python 3.8 e 3.13, compila fontes e testes, instala o pacote, verifica a importação, executa `unittest` e constrói wheel e source distribution. O token tem permissão somente de leitura nesse workflow.

Execução local:

```bash
python -m compileall -q src tests
python -m pip install .
python -m unittest discover -s tests -v
python -m pip install build
python -m build
```

## Tags automáticas para funcionalidades

`.github/workflows/feature-tags.yml` é acionado em cada push para uma branch `feat/*`. Cria uma tag anotada por commit no padrão `feat/<nome-da-branch>/<sha-completo>`. Requer `contents: write`; não representa uma release.

## Releases versionadas

`.github/workflows/release.yml` é acionado por tags `v*`. Compara a tag com `binlab.__version__`, compila fontes e testes, instala o pacote, executa a suíte `unittest`, constrói wheel e source distribution e só então cria um GitHub Release. Atualize a versão e o changelog antes de marcar uma release.

```bash
git switch main
git pull --ff-only
git tag -a vX.Y.Z -m "Release X.Y.Z"
git push origin vX.Y.Z
```

Crie versões somente após revisão e integração. Tags de feature não publicam releases.

## Segurança de pipeline

- CI de validação usa `contents: read`.
- Permissões de escrita ficam restritas ao workflow de tags/release que precisa delas.
- Não inserir tokens em arquivos, argumentos de build ou logs.
- Ações de terceiros e dependências devem ser revisadas e atualizadas de forma controlada.
