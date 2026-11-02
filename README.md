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

### Aplicação Python 0.3.1

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

Consulte [apps/web/README.md](apps/web/README.md) para a estrutura e as limitações atuais.

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
3. Contratos HTTP serão versionados e documentados em OpenAPI.
4. A aplicação Web não acessará filesystem ou banco diretamente.
5. O backend local deverá validar origem, autenticação, CSRF, Host e tentativas de DNS rebinding.
6. C/C++ serão introduzidos somente quando houver justificativa mensurável de desempenho ou acesso de baixo nível.

## Segurança e limites

O leitor Python realiza **inspeção estática**. Arquivos importados não são executados nem compilados automaticamente.

Limites atuais documentados:

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

Esses controles **não equivalem a uma sandbox**. Não use o BinLab como ambiente de execução de arquivos não confiáveis. A exposição do leitor pela API permanece bloqueada até a conclusão da [Issue #2](https://github.com/mnl-nox/BinLab/issues/2), incluindo testes de fronteira, fuzzing reproduzível e revisão complementar.

## Estrutura do repositório

```text
src/binlab/                 núcleo Python, CLI, GUI e leitor estático
apps/web/                   aplicação React/TypeScript
apps/desktop/               integração Tauri (planejada)
website/                    site institucional estático
branding/                   logotipos e licença dos ativos visuais
docs/                       arquitetura, contratos, auditoria e roadmap
doc/                        documentação da versão Python atual
tests/                      testes Python
images/                     diagramas e recursos históricos
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
8. Persistência de experimentos e distribuição reproduzível.

A evolução de cada etapa depende de testes, documentação, critérios de aceite e revisão. A API não deve ser liberada antes da conclusão dos critérios de segurança pendentes.

## Desenvolvimento e qualidade

O CI do repositório valida Python 3.8 e 3.13, executa testes unitários, verifica compilação e constrói wheel/sdist. O job Web instala dependências, executa testes Vitest e gera build de produção.

Contribuições devem preservar:

- compatibilidade com a versão mínima de Python;
- ausência de dependências obrigatórias desnecessárias no runtime Python;
- testes para entradas válidas, inválidas e limites;
- documentação dos contratos e mudanças de comportamento;
- análise estática por padrão e execução explícita somente em ambiente controlado;
- ausência de segredos, tokens e dados pessoais em commits e logs.

Leia [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir uma contribuição e [SECURITY.md](SECURITY.md) para reportar vulnerabilidades.

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
