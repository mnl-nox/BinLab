# BinLab Engineering

<p align="center">
  <strong>Computational Science & Technology Laboratory</strong><br>
  Engenharia computacional, experimentação técnica e análise local-first.
</p>

<p align="center">
  <strong>Python Core · React + TypeScript · Local-first · MIT</strong>
</p>

<p align="center">
  <a href="https://github.com/mnl-nox/BinLab/actions"><img alt="CI" src="https://github.com/mnl-nox/BinLab/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <a href="branding/LICENSE"><img alt="Visual assets: CC BY 4.0" src="https://img.shields.io/badge/Visual%20Assets-CC%20BY%204.0-0b7285.svg"></a>
</p>

> **Estado do projeto:** a versão Python 0.3.1 (CLI e GUI Tkinter) é a base funcional. A aplicação Web está em desenvolvimento; o Binary & Logic Lab é a primeira experiência funcional no navegador. API FastAPI, persistência e desktop Tauri ainda não fazem parte do produto integrado.

O BinLab é um laboratório de engenharia computacional projetado para estudar, experimentar e investigar sistemas desde a representação binária até arquitetura de computadores, compiladores, sistemas operacionais, redes, segurança e computação científica. A prioridade arquitetural é **execução local, transparência técnica, modularidade e segurança por padrão**.

## Instalação Linux

A primeira distribuição binária é destinada a Linux x86_64 e inclui a CLI e a GUI Tkinter:

- Debian, Ubuntu e derivados: pacote `.deb`.
- Fedora, RHEL e derivados: pacote `.rpm`.
- Outras distribuições: arquivo `.tar.gz` com executáveis e recursos em uma árvore `usr/`.

Os pacotes são publicados como ativos de uma GitHub Release. A versão precisa corresponder à versão do pacote Python.

### Debian / Ubuntu

```bash
sudo apt install ./binlab_0.3.1_amd64.deb
binlab
binlab-gui
```

### Fedora / RHEL / openSUSE compatível com RPM

```bash
sudo dnf install ./binlab-0.3.1-1.x86_64.rpm
binlab
binlab-gui
```

### Outras distribuições

```bash
tar -xzf binlab-0.3.1-linux-x86_64.tar.gz
sudo cp -a usr/. /usr/
binlab
binlab-gui
```

A GUI requer sessão gráfica X11/compatibilidade XWayland e bibliotecas gráficas do sistema. A primeira entrega não inclui AppImage, Flatpak nem build ARM64.

## Instalação Python

Requisitos: Python 3.8 ou superior. GNU `objdump` é opcional.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
binlab
```

Interface gráfica:

```bash
binlab-gui
```

Em algumas distribuições Linux, instale `python3-tk` pelo gerenciador de pacotes. Para executar diretamente do checkout:

```bash
PYTHONPATH=src python3 -m binlab
PYTHONPATH=src python3 -m binlab.gui
```

## Aplicação Web

Requisitos: Node.js 20+ e npm 10+.

```bash
cd apps/web
npm install
npm run dev
```

Validação local:

```bash
npm test
npm run build
```

A fundação Web implementa conversão de bases e operações BigInt no navegador. A API não está integrada nesta versão.

## Arquitetura

A direção é um **monólito modular**, evitando a complexidade prematura de microserviços.

```text
React / TypeScript ───────┐
                          ├── HTTP /api/v1 ── FastAPI adapter
Tauri Desktop ────────────┘                         │
                                            Application services
                                                    │
                                             Python domain
                                                    │
                                       Infrastructure adapters
                                       SQLite · filesystem · tools
```

Princípios:

1. O domínio permanece independente de frameworks, interfaces, banco de dados e sistema operacional.
2. Interfaces Web e Desktop consomem casos de uso por contratos explícitos.
3. Contratos HTTP serão versionados e documentados por OpenAPI.
4. A aplicação Web não acessará filesystem ou banco diretamente.
5. O backend local deverá validar origem, autenticação, CSRF, Host e tentativas de DNS rebinding.
6. C/C++ serão introduzidos somente quando houver justificativa mensurável de desempenho ou acesso de baixo nível.

## Capacidades Python disponíveis

- Conversão entre binário, octal, decimal e hexadecimal.
- Aritmética inteira e operações lógicas bit a bit.
- Análise de largura, sinal, bytes e caracteres ASCII.
- Inspeção estática de fontes C/Assembly, dumps HEX e arquivos binários.
- Desassemblagem opcional por GNU `objdump`.
- CLI e GUI Tkinter sem dependências Python extras no runtime de base.

## Segurança e limites

O leitor Python realiza **inspeção estática**. Arquivos importados não são executados nem compilados automaticamente. Isso não equivale a uma sandbox; não use o BinLab como ambiente de execução de arquivos não confiáveis.

Limites atuais: fontes 2 MiB; binários 8 MiB; texto Intel HEX 4 MiB; 65.536 registros; span decodificado 1 MiB; lacunas 64 KiB; saída combinada de objdump 64 KiB; timeout 20 segundos.

A exposição do leitor pela API permanece bloqueada até a conclusão da [Issue #2](https://github.com/mnl-nox/BinLab/issues/2), incluindo fuzzing e revisão complementar.

## Desenvolvimento e qualidade

O CI valida Python 3.8 e 3.13, executa testes unitários e property-based, verifica compilação e constrói wheel/sdist. O job Web executa testes Vitest e build de produção.

Para instalar dependências de teste:

```bash
python -m pip install -e ".[test]"
python -m unittest discover -s tests -v
```

Para construir os pacotes Linux (Ubuntu 22.04 x86_64, PyInstaller e FPM):

```bash
python -m pip install . pyinstaller==6.16.0
sudo apt install ruby ruby-dev rpm
sudo gem install --no-document fpm
bash packaging/build-linux.sh
```

## Estrutura

```text
src/binlab/                 núcleo Python, CLI, GUI e leitor estático
apps/web/                   aplicação React/TypeScript
packaging/                  entrypoints e pipeline de pacotes Linux
website/                    site institucional estático
branding/                   logotipos e licença dos ativos visuais
docs/                       arquitetura, contratos, auditoria e roadmap
tests/                      testes Python
.github/workflows/          CI e automações de release/deploy
```

## Documentação

- [Roadmap](docs/ROADMAP.md)
- [Visão geral da arquitetura](docs/architecture/overview.md)
- [Contratos](docs/contracts/README.md)
- [Modelo de ameaças](docs/security/threat-model.md)
- [Auditoria técnica](docs/audit/2026-11-02-code-review.md)
- [Política de segurança](SECURITY.md)
- [Contribuição](CONTRIBUTING.md)
- [Histórico de alterações](CHANGELOG.md)

## Licenças e autoria

**Código-fonte:** MIT License. Consulte [LICENSE](LICENSE).

**Ativos visuais originais:** Creative Commons Attribution 4.0 International (CC BY 4.0). Consulte [branding/LICENSE](branding/LICENSE).

**Autoria:** Copyright © 2026 Manoel E. S. S.
