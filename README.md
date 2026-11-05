<p align="center">
  <img src="branding/logo.svg" alt="BinLab Engineering" width="560">
</p>

<p align="center">
  <strong>Laboratório de Engenharia Computacional</strong><br>
  Entenda os fundamentos. Inspecione sistemas. Construa experimentos reproduzíveis.
</p>

<p align="center">
  <a href="https://github.com/mnl-nox/BinLab/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/mnl-nox/BinLab/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/mnl-nox/BinLab/actions/workflows/pages.yml"><img alt="GitHub Pages" src="https://github.com/mnl-nox/BinLab/actions/workflows/pages.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/Code-MIT-2563eb.svg"></a>
  <a href="branding/LICENSE"><img alt="Visual assets: CC BY 4.0" src="https://img.shields.io/badge/Branding-CC%20BY%204.0-0891b2.svg"></a>
  <a href="https://github.com/mnl-nox/BinLab/releases"><img alt="Release" src="https://img.shields.io/badge/version-0.3.2-informational.svg"></a>
</p>

<p align="center">
  <a href="https://github.com/mnl-nox/BinLab">Repositório</a> ·
  <a href="https://github.com/mnl-nox/BinLab/tree/main/docs">Documentação</a> ·
  <a href="https://github.com/mnl-nox/BinLab/issues">Issues</a> ·
  <a href="https://github.com/mnl-nox/BinLab/blob/main/CONTRIBUTING.md">Contribuir</a> ·
  <a href="https://github.com/mnl-nox/BinLab/blob/main/SECURITY.md">Segurança</a>
</p>

> **Versão atual do núcleo: 0.3.2.** CLI Python, GUI Tkinter, leitor estático de artefatos e a primeira fundação Web estão disponíveis. Os pacotes Linux x86_64 foram construídos e validados no CI. A publicação da GitHub Release oficial depende da criação da tag v0.3.2; até lá, os instaladores podem ser obtidos no artefato do workflow indicado em [Distribuição Linux](#distribuição-linux).

BinLab Engineering é um laboratório open source para estudar, experimentar e investigar sistemas computacionais — da representação binária à arquitetura de computadores, compiladores, sistemas operacionais, redes, segurança e computação científica.

O projeto evolui a partir de um núcleo Python funcional para uma plataforma **local-first, modular, verificável e segura por padrão**. O objetivo não é esconder a complexidade atrás de uma interface: é tornar cada camada observável e cada experimento reproduzível.

## Sumário

- [Estado do projeto](#estado-do-projeto)
- [O que já funciona](#o-que-já-funciona)
- [Distribuição Linux](#distribuição-linux)
- [Instalação a partir do código-fonte](#instalação-a-partir-do-código-fonte)
- [Aplicação Web](#aplicação-web)
- [Arquitetura](#arquitetura)
- [Segurança e limites conhecidos](#segurança-e-limites-conhecidos)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Desenvolvimento e testes](#desenvolvimento-e-testes)
- [Roadmap](#roadmap)
- [Documentação e suporte](#documentação-e-suporte)
- [Contribuição](#contribuição)
- [Comunidade e suporte](#comunidade-e-suporte)
- [Licenças e autoria](#licenças-e-autoria)

## Estado do projeto

| Área | Estado em 0.3.2 | Implementação |
|---|---|---|
| Núcleo numérico | Disponível | Python |
| CLI | Disponível | Python |
| Desktop clássico | Disponível | Tkinter |
| Leitor estático | Disponível | Python, Intel HEX, binários e fontes |
| Aplicação Web | Fundação funcional | React, TypeScript, Vite |
| Binary & Logic Lab Web | Disponível em escopo inicial | BigInt no navegador |
| API local | Não integrada | FastAPI planejado, bloqueado por revisão de segurança |
| Desktop integrado | Planejado | Tauri |
| Projetos e persistência | Planejado | SQLite |

**Importante:** a aplicação Web e a aplicação Python ainda são experiências separadas. Não existe integração HTTP entre elas, backend FastAPI publicado ou persistência compartilhada nesta versão.

## O que já funciona

### Núcleo Python 0.3.2

- Conversão de inteiros entre bases 2, 8, 10 e 16.
- Formatação, aritmética e operações lógicas bit a bit.
- Análise de largura, sinal, bytes e caracteres ASCII.
- Leitura e inspeção estática de fontes C/Assembly, dumps HEX, Intel HEX e arquivos binários.
- Desassemblagem opcional com GNU objdump.
- Interface de terminal (binlab) e interface Tkinter (binlab-gui).

### Aplicação Web

- Interface React + TypeScript com navegação modular e temas claro/escuro.
- Conversão de bases e operações AND, OR, XOR e shift-left usando BigInt.
- Validação de entradas, limites de operandos e mensagens de erro explícitas.
- Laboratórios ainda não implementados identificados como planejados.

### Princípios técnicos

- Execução local por padrão; sem conta, analytics ou backend remoto exigido pelo núcleo.
- Domínio numérico separado das interfaces.
- Entradas externas validadas e limites de recursos explícitos.
- Arquivos importados são inspecionados estaticamente, nunca executados automaticamente.
- Testes unitários e property-based no pipeline de qualidade.

## Distribuição Linux

<sub>Primeira linha de distribuição: Linux x86_64 · build em Ubuntu 22.04 · baseline GLIBC_2.14</sub>

| Formato | Distribuições | Arquivo |
|---|---|---|
| Debian | Debian, Ubuntu e derivados | binlab_0.3.2_amd64.deb |
| RPM | Fedora, RHEL e compatíveis | binlab-0.3.2-1.x86_64.rpm |
| Tarball | Distribuições glibc compatíveis | binlab-0.3.2-linux-x86_64.tar.gz |

**Obter os pacotes:** [workflow Linux — artefatos da versão 0.3.2](https://github.com/mnl-nox/BinLab/actions/runs/41939255038). Abra a execução e baixe o artefato binlab-linux-x86_64. O artefato inclui os três pacotes e SHA256SUMS; a retenção do GitHub Actions é limitada e exige sessão autenticada.

A tag v0.3.2 e a GitHub Release pública ainda precisam ser publicadas. A página [Releases](https://github.com/mnl-nox/BinLab/releases) é o destino das distribuições oficiais quando essa etapa for concluída.

### Debian / Ubuntu

~~~bash
sha256sum -c SHA256SUMS
sudo apt install ./binlab_0.3.2_amd64.deb
binlab
binlab-gui
~~~

### Fedora / RHEL

~~~bash
sha256sum -c SHA256SUMS
sudo dnf install ./binlab-0.3.2-1.x86_64.rpm
binlab
binlab-gui
~~~

### Outras distribuições glibc

~~~bash
tar -xzf binlab-0.3.2-linux-x86_64.tar.gz
sudo cp -a usr/. /usr/
binlab
binlab-gui
~~~

**Compatibilidade e validação:** o pacote DEB foi instalado no runner Ubuntu 22.04 e CLI/GUI passaram por smoke test; o RPM foi construído e inspecionado, mas ainda não foi instalado em uma VM Fedora/RHEL. A GUI requer bibliotecas gráficas do host e sessão X11 ou XWayland. Alpine/musl, ARM64, AppImage e Flatpak não fazem parte desta entrega. Não interprete x86_64 como compatibilidade universal com toda distribuição Linux.

## Instalação a partir do código-fonte

### Requisitos

- Python 3.8 ou superior.
- GNU objdump opcional para desassemblagem.
- Para a interface Web: Node.js 22 e npm.

### Python — ambiente virtual

~~~bash
git clone https://github.com/mnl-nox/BinLab.git
cd BinLab

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .

binlab
# Interface gráfica:
binlab-gui
~~~

Para executar sem instalar o pacote:

~~~bash
PYTHONPATH=src python -m binlab
PYTHONPATH=src python -m binlab.gui
~~~

Em algumas distribuições Debian, a GUI requer o pacote de sistema python3-tk.

### Web — ambiente de desenvolvimento

~~~bash
cd apps/web
npm install
npm run dev
~~~

Validação da aplicação:

~~~bash
npm test
npm run build
~~~

Consulte [apps/web/README.md](apps/web/README.md) para detalhes e limitações da fundação Web.

## Arquitetura

A direção arquitetural é um **monólito modular**, não uma coleção prematura de microserviços.

~~~text
React / TypeScript ───────┐
                          ├── HTTP /api/v1 ── FastAPI adapter (planejado)
Tauri Desktop ────────────┘                         │
                                            Application services
                                                    │
                                             Python domain
                                                    │
                                       Infrastructure adapters
                                       SQLite · filesystem · tools
~~~

Regras de dependência:

1. O domínio não depende de frameworks, interfaces, banco de dados ou sistema operacional.
2. Casos de uso coordenam domínio e portas; adaptadores implementam portas.
3. Contratos HTTP serão versionados e documentados por OpenAPI.
4. A interface Web não acessará filesystem ou banco diretamente.
5. O backend local deverá tratar origem, autenticação, CSRF, Host e DNS rebinding antes de expor operações.
6. C/C++ serão introduzidos quando houver justificativa mensurável de desempenho ou acesso de baixo nível.

## Segurança e limites conhecidos

O leitor de artefatos realiza **inspeção estática**. Arquivos importados não são executados nem compilados automaticamente.

| Superfície | Limite atual |
|---|---:|
| Código-fonte | 2 MiB |
| Binário | 8 MiB |
| Texto Intel HEX | 4 MiB |
| Registros Intel HEX | 65.536 |
| Span decodificado | 1 MiB |
| Lacuna esparsa | 64 KiB |
| Saída combinada do objdump | 64 KiB |
| Timeout do objdump | 20 s |

O parser Intel HEX valida checksum e estrutura, exige EOF único e terminal, rejeita sobreposições e limita endereços e alocações esparsas. O objdump é iniciado sem shell, com ambiente reduzido, timeout e saída limitada.

Esses controles **não constituem uma sandbox**. Não use o BinLab para executar arquivos não confiáveis. A exposição do leitor por API permanece bloqueada até a conclusão da [Issue #2](https://github.com/mnl-nox/BinLab/issues/2), incluindo fuzzing mais amplo e revisão complementar. A [Issue #3](https://github.com/mnl-nox/BinLab/issues/3) acompanha validações adicionais do pipeline e das permissões do repositório.

Consulte [SECURITY.md](SECURITY.md) para reporte responsável e [o modelo de ameaças](docs/security/threat-model.md) para os limites da arquitetura.

## Estrutura do repositório

~~~text
src/binlab/                 núcleo Python, CLI, GUI e leitor estático
apps/web/                   aplicação React/TypeScript
apps/desktop/               integração Tauri (planejada)
website/                    site institucional estático
branding/                   logotipos vetoriais e licença dos ativos
packaging/                  entrypoints e pipeline de pacotes Linux
docs/                       arquitetura, contratos, auditoria e roadmap
tests/                      testes Python
.github/workflows/          CI, release e publicação do site
~~~

## Desenvolvimento e testes

Instale dependências de teste:

~~~bash
python -m pip install -e ".[test]"
python -m compileall -q src tests
python -m unittest discover -s tests -v
~~~

Verifique a Web:

~~~bash
cd apps/web
npm install
npm test
npm run build
~~~

Construa os pacotes Linux em ambiente Ubuntu 22.04 x86_64 com as dependências de empacotamento:

~~~bash
python -m pip install . "pyinstaller==6.16.0"
sudo apt install ruby ruby-dev rpm
sudo gem install --no-document fpm
bash packaging/build-linux.sh
~~~

O CI cobre Python 3.8 e 3.13, testes Python, testes/build Web e smoke build dos pacotes Linux. O workflow de release é acionado por tags v*.

## Roadmap

1. Concluir estabilização, auditoria e hardening dos parsers.
2. Ampliar fuzzing/property tests e concluir a Issue #2.
3. Definir contratos e backend local com fronteiras seguras.
4. Expandir a aplicação Web e integrar o Desktop via Tauri.
5. Evoluir Binary & Logic e implementar Architecture Lab.
6. Implementar Compiler, Operating Systems, Network e Security Labs.
7. Adicionar computação científica, dados e IA local opcional.
8. Introduzir persistência de experimentos e projetos reproduzíveis.
9. Fortalecer releases com builds reproduzíveis, SBOM e attestations.

O status detalhado está em [docs/ROADMAP.md](docs/ROADMAP.md). Itens planejados não devem ser interpretados como funcionalidades disponíveis.

## Documentação e suporte

- [Site institucional](website/README.md)
- [Roadmap](docs/ROADMAP.md)
- [Arquitetura geral](docs/architecture/overview.md)
- [Arquitetura Web](docs/architecture/web-application.md)
- [Contratos](docs/contracts/README.md)
- [Modelo de ameaças](docs/security/threat-model.md)
- [Auditoria técnica — 04/11/2026](docs/audit/2026-11-04-code-review.md)
- [Política de segurança](SECURITY.md)
- [Privacidade](docs/legal/PRIVACY.md)
- [Contribuição](CONTRIBUTING.md)
- [Histórico de alterações](CHANGELOG.md)
- [Issues e solicitações](https://github.com/mnl-nox/BinLab/issues)

Antes de abrir uma issue, verifique se já existe uma solicitação semelhante. Para vulnerabilidades, não publique detalhes exploráveis em issue pública; siga o processo de reporte privado descrito em [SECURITY.md](SECURITY.md).

## Contribuição

Contribuições são bem-vindas. Para manter o histórico auditável:

1. Abra ou comente uma issue descrevendo o problema ou a proposta.
2. Crie uma branch focada em uma única entrega.
3. Inclua testes, documentação, limitações e riscos no pull request.
4. Execute os testes e verificações aplicáveis antes de solicitar revisão.
5. Não exponha credenciais, dados pessoais ou arquivos de terceiros nos commits e logs.

Leia [CONTRIBUTING.md](CONTRIBUTING.md) antes de enviar alterações. O projeto usa Conventional Commits e Semantic Versioning.

## Comunidade e suporte

- [Código de conduta](CODE_OF_CONDUCT.md)
- [Suporte](SUPPORT.md)
- [Como contribuir](CONTRIBUTING.md)
- [Citação acadêmica e técnica](CITATION.cff)

## Licenças e autoria

- **Código-fonte:** MIT — consulte [LICENSE](LICENSE).
- **Identidade visual original:** CC BY 4.0 — consulte [branding/LICENSE](branding/LICENSE) e [branding/README.md](branding/README.md).
- **Autoria:** Copyright © 2026 Manoel E. S. S. (mnl-nox).

A licença MIT do software não se aplica automaticamente aos ativos visuais. CC BY 4.0 exige atribuição e não concede direitos de marca registrada.
