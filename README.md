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

> **Estado do projeto:** a versão Python 0.3.2 (CLI e GUI Tkinter) é a base funcional. A aplicação Web está em desenvolvimento; o Binary & Logic Lab é a primeira experiência funcional no navegador. API FastAPI, persistência e desktop Tauri ainda não fazem parte do produto integrado.

O BinLab é um laboratório de engenharia computacional projetado para estudar, experimentar e investigar sistemas desde a representação binária até arquitetura de computadores, compiladores, sistemas operacionais, redes, segurança e computação científica. A prioridade arquitetural é **execução local, transparência técnica, modularidade e segurança por padrão**.

## Índice

- [Escopo e estado](#escopo-e-estado)
- [Capacidades disponíveis](#capacidades-disponíveis)
- [Instalação e execução](#instalação-e-execução)
- [Arquitetura](#arquitetura)
- [Segurança e limites](#segurança-e-limites)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Roadmap](#roadmap)
- [Desenvolvimento e qualidade](#desenvolvimento-e-qualidade)
- [Documentação](#documentação)
- [Licenças e autoria](#licenças-e-autoria)

## Escopo e estado

| Componente | Estado | Tecnologia |
|---|---|---|
| CLI | Disponível | Python 3.8+ |
| Desktop legado | Disponível | Tkinter |
| Web | Fundação funcional em desenvolvimento | React, TypeScript, Vite, Tailwind CSS |
| API local | Bloqueada até conclusão do hardening | FastAPI — planejado |
| Desktop multiplataforma | Planejado | Tauri |
| Persistência de experimentos | Planejada | SQLite |

## Capacidades disponíveis

### Aplicação Python 0.3.2

- Conversão entre binário, octal, decimal e hexadecimal.
- Aritmética inteira e operações lógicas bit a bit.
- Análise de largura, sinal, bytes e caracteres ASCII.
- Inspeção estática de fontes C/Assembly, dumps HEX e arquivos binários.
- Desassemblagem opcional por GNU `objdump`.
- CLI e GUI Tkinter sem dependências Python extras no runtime de base.

### Aplicação Web

- Navegação modular pelos oito laboratórios previstos.
- Binary & Logic Lab com conversão de bases usando `BigInt`.
- Operações AND, OR, XOR e deslocamento à esquerda.
- Temas claro e escuro e layout responsivo.
- Módulos ainda não implementados identificados como planejados.
- Sem API remota ou persistência integrada nesta etapa.

## Instalação e execução

### Pacotes Linux (primeira linha: x86_64)

A primeira distribuição binária é destinada a Linux x86_64 e inclui CLI e GUI Tkinter:

- Debian, Ubuntu e derivados: pacote `.deb`.
- Fedora, RHEL e sistemas compatíveis: pacote `.rpm`.
- Outras distribuições: arquivo `.tar.gz` com executáveis e recursos em uma árvore `usr/`.

Os arquivos são publicados como ativos de uma GitHub Release, depois da aprovação do CI.

Debian / Ubuntu:

```bash
sudo apt install ./binlab_0.3.2_amd64.deb
binlab
binlab-gui
```

Fedora / RHEL:

```bash
sudo dnf install ./binlab-0.3.2-1.x86_64.rpm
binlab
binlab-gui
```

Outras distribuições:

```bash
tar -xzf binlab-0.3.2-linux-x86_64.tar.gz
sudo cp -a usr/. /usr/
binlab
binlab-gui
```

A GUI requer uma sessão gráfica X11/compatibilidade XWayland e bibliotecas gráficas do host. A primeira linha não inclui AppImage, Flatpak nem build ARM64. A instalação dos pacotes deve ser validada em distribuições-alvo antes de declarar compatibilidade ampla.

### Python

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

### Web

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

Consulte [apps/web/README.md](apps/web/README.md) para estrutura e limitações atuais.

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

Princípios de projeto:

1. O domínio permanece independente de frameworks, interfaces, banco de dados e sistema operacional.
2. Interfaces Web e Desktop consomem casos de uso por contratos explícitos.
3. Contratos HTTP serão versionados e documentados por OpenAPI.
4. A aplicação Web não acessará filesystem ou banco diretamente.
5. O backend local deverá validar origem, autenticação, CSRF, Host e tentativas de DNS rebinding.
6. C/C++ serão introduzidos somente quando houver justificativa mensurável de desempenho ou acesso de baixo nível.

## Segurança e limites

O leitor Python realiza **inspeção estática**. Arquivos importados não são executados nem compilados automaticamente.

Limites atuais:

| Superfície | Limite |
|---|---:|
| Código-fonte | 2 MiB |
| Binário | 8 MiB |
| Texto Intel HEX | 4 MiB |
| Registros Intel HEX | 65.536 |
| Span decodificado | 1 MiB |
| Lacuna esparsa | 64 KiB |
| Saída combinada do `objdump` | 64 KiB |
| Timeout do `objdump` | 20 s |

O parser Intel HEX valida checksum e estrutura, exige EOF único e terminal, rejeita sobreposições e limita endereços e alocações esparsas. O `objdump` é iniciado sem shell, com ambiente reduzido, timeout e saída drenada sob limite.

Esses controles **não equivalem a uma sandbox**. Não use o BinLab como ambiente de execução de arquivos não confiáveis. A exposição do leitor pela API permanece bloqueada até a conclusão da [Issue #2](https://github.com/mnl-nox/BinLab/issues/2), incluindo fuzzing e revisão complementar.

## Estrutura do repositório

```text
src/binlab/                 núcleo Python, CLI, GUI e leitor estático
apps/web/                   aplicação React/TypeScript
apps/desktop/               integração Tauri (planejada)
website/                    site institucional estático
branding/                   logotipos e licença dos ativos visuais
packaging/                  entrypoints e pipeline de pacotes Linux
docs/                       arquitetura, contratos, auditoria e roadmap
tests/                      testes Python
.github/workflows/          CI e automações de release/deploy
```

## Roadmap

1. Estabilização, auditoria e hardening dos parsers.
2. Testes property-based/fuzzing e conclusão da Issue #2.
3. Backend de aplicação e contratos HTTP seguros.
4. Expansão da aplicação Web e integração Desktop via Tauri.
5. Binary & Logic Lab e Architecture Lab.
6. Compiler, Operating Systems, Network e Security Labs.
7. Computação científica, dados e IA local.
8. Persistência de experimentos e projetos reproduzíveis.
9. Releases Linux, builds reproduzíveis, SBOM e attestations.

A conclusão de cada etapa depende de testes, documentação, critérios de aceite e revisão. Uma etapa não é considerada pronta apenas porque o código compila.

## Desenvolvimento e qualidade

O CI valida Python 3.8 e 3.13, executa testes unitários e property-based, verifica compilação e constrói wheel/sdist. O job Web instala dependências, executa testes Vitest e gera build de produção. Um job Linux constrói e inspeciona .deb, .rpm e tar.gz em Ubuntu 22.04 x86_64.

Para instalar dependências de teste:

```bash
python -m pip install -e ".[test]"
python -m unittest discover -s tests -v
```

Para construir pacotes Linux:

```bash
python -m pip install . pyinstaller==6.16.0
sudo apt install ruby ruby-dev rpm
sudo gem install --no-document fpm
bash packaging/build-linux.sh
```

## Documentação

- [Site institucional — fonte e publicação](website/README.md)
- [Roadmap](docs/ROADMAP.md)
- [Visão geral da arquitetura](docs/architecture/overview.md)
- [Arquitetura da aplicação Web](docs/architecture/web-application.md)
- [Contratos](docs/contracts/README.md)
- [Modelo de ameaças](docs/security/threat-model.md)
- [Auditoria técnica](docs/audit/2026-11-02-code-review.md)
- [Licenciamento](docs/legal/LICENSING.md)
- [Privacidade](docs/legal/PRIVACY.md)
- [Política de segurança](SECURITY.md)
- [Contribuição](CONTRIBUTING.md)
- [Histórico de alterações](CHANGELOG.md)

## Licenças e autoria

**Código-fonte:** MIT License. Consulte [LICENSE](LICENSE).

**Ativos visuais originais:** Creative Commons Attribution 4.0 International (CC BY 4.0). Consulte [branding/LICENSE](branding/LICENSE) e [branding/README.md](branding/README.md).

**Autoria:** Copyright © 2026 Manoel E. S. S. (mnl-nox).

A licença dos ativos visuais é independente da licença do código. CC BY 4.0 não concede direitos de marca registrada.
