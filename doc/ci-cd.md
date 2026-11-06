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

## Pré-releases de funcionalidades

`.github/workflows/feature-tags.yml` é acionado em cada push para uma branch `feat/**`. Executa os testes Python e Web, valida o atalho desktop, constrói e inspeciona os pacotes `.deb`, `.rpm` e tarball x86_64 e instala o `.deb` no runner para smoke test da CLI e da GUI via Xvfb. Só depois publica uma pré-release GitHub com uma tag anotada por commit no padrão `feat/<nome-da-branch>/<sha-completo>`.

Cada execução define uma versão de pacote maior que a versão base atual, usando `X.Y.Z.AAAAMMDD.RUN_NUMBER`. Assim, `apt` e `dnf` podem aplicar uma pré-release posterior sobre a versão base instalada. Essas publicações destinam-se a testes e continuam limitadas a Linux x86_64 com glibc; não são releases estáveis nem suportam Alpine/musl ou ARM64.

## Releases versionadas

`.github/workflows/release.yml` é acionado por tags `v*`. Compara a tag com `binlab.__version__`, executa a suíte `unittest`, constrói wheel, source distribution e pacotes Linux, valida a entrada desktop, instala o `.deb` no runner e inicia a GUI sob Xvfb. Só publica o GitHub Release depois que esses passos passam. Atualize a versão e o changelog antes de marcar uma release.

```bash
git switch main
git pull --ff-only
git tag -a vX.Y.Z -m "Release X.Y.Z"
git push origin vX.Y.Z
```

Crie versões estáveis somente após revisão e integração. Tags `v*` continuam sendo o canal de releases estáveis; versões de feature são pré-releases independentes.

## Segurança de pipeline

- CI de validação usa `contents: read`.
- Permissões de escrita ficam restritas ao workflow de tags/release que precisa delas.
- Não inserir tokens em arquivos, argumentos de build ou logs.
- Ações de terceiros e dependências devem ser revisadas e atualizadas de forma controlada.

## Atualização de actions

`.github/dependabot.yml` verifica semanalmente atualizações das GitHub Actions. A configuração de Dependabot não substitui a revisão de segurança: as referências dos workflows ainda precisam ser fixadas em SHA completo verificado. Esse trabalho está rastreado na [issue #3](https://github.com/mnl-nox/BinLab/issues/3).
