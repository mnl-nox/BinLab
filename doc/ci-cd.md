# CI/CD, tags e versões

## Integração contínua

`.github/workflows/ci.yml` executa em pull requests e em pushes para `main` e `feat/**`. Em Python 3.8 e 3.13, compila os módulos, instala o pacote, confirma a importação e executa a suíte `unittest`. A permissão do token fica somente em leitura. Localmente, rode `python -m unittest discover -s tests -v`.

## Tags automáticas para funcionalidades

`.github/workflows/feature-tags.yml` é acionado em cada push para uma branch `feat/*`. Cria e envia uma tag anotada para o commit recebido, no padrão:

```text
feat/<nome-da-branch>/<sha-completo>
```

Assim cada commit publicado na branch de funcionalidade possui sua própria referência imutável. O workflow precisa da permissão de repositório `contents: write` concedida ao `GITHUB_TOKEN`. Repositórios que bloqueiam criação de tags por Actions precisam liberar esse padrão de tag nas regras do GitHub.

## Releases versionadas

`.github/workflows/release.yml` é acionado por tags `v*`. Antes de publicar, compara a tag com `binlab.__version__`, constrói wheel e source distribution e cria um GitHub Release com notas automáticas. A versão atual está em `src/binlab/__init__.py`; atualize-a antes de criar a próxima tag.

Exemplo de release manual:

```bash
git switch main
git pull --ff-only
git tag -a v0.3.0 -m "Release 0.3.0"
git push origin v0.3.0
```

Crie versões somente depois de integrar e revisar as funcionalidades desejadas. Tags `feat/...` não publicam releases.
