<p align="center">
  <img src="images/binlab-logo.svg" alt="BinLab monogram" width="112">
</p>

<h1 align="center">BinLab Engineering</h1>
<p align="center">Computational Science & Technology Laboratory</p>

<p align="center">
  <strong>Python core · React + TypeScript Web · Local-first · MIT</strong>
</p>

BinLab é um laboratório de engenharia computacional em evolução. O projeto combina ferramentas para representação numérica, lógica digital e inspeção estática de artefatos com uma arquitetura modular preparada para laboratórios de arquitetura de computadores, compiladores, sistemas operacionais, redes, segurança e computação científica.

> **Estado do produto:** a versão Python 0.3.1 (CLI e GUI Tkinter) é a base funcional. A aplicação Web está em desenvolvimento ativo; nesta primeira entrega, o Binary & Logic Lab funciona localmente no navegador. API FastAPI, persistência e desktop Tauri ainda não estão integrados.

## Aplicações

| Aplicação | Estado | Tecnologia |
|---|---|---|
| CLI | Disponível | Python 3.8+ |
| Desktop legado | Disponível | Tkinter |
| Web | Fundação em desenvolvimento | React, TypeScript, Vite, Tailwind CSS |
| API local | Bloqueada por hardening de segurança | FastAPI (planejado) |
| Desktop multiplataforma | Planejado | Tauri |

## Recursos disponíveis

### Python 0.3.1
- Aritmética inteira e operações lógicas bit a bit.
- Conversão entre binário, octal, decimal e hexadecimal.
- Análise de largura, sinal, bytes e caracteres ASCII.
- Leitura estática de fontes C/Assembly, dumps HEX e arquivos binários.
- Desassemblagem opcional com GNU \`objdump\`.
- Interface CLI e GUI Tkinter sem dependências Python extras de runtime.

### Web — primeira entrega
- Navegação modular entre laboratórios.
- Tema claro/escuro com estado independente da navegação e de futuras integrações de IA.
- Conversão entre bases com inteiros BigInt.
- Operações AND, OR, XOR e deslocamento à esquerda.
- Layout responsivo para desktop e dispositivos móveis.
- Módulos não implementados identificados explicitamente como planejados.

## Executar a aplicação Python

Requisitos: Python 3.8 ou superior. GNU \`objdump\` é opcional.

\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
binlab
\`\`\`

GUI:

\`\`\`bash
binlab-gui
\`\`\`

Em algumas distribuições Linux, instale \`python3-tk\` pelo gerenciador de pacotes. Para executar a partir do checkout sem instalar:

\`\`\`bash
PYTHONPATH=src python3 -m binlab
PYTHONPATH=src python3 -m binlab.gui
\`\`\`

## Executar a aplicação Web

Requisitos: Node.js 20+ e npm 10+.

\`\`\`bash
cd apps/web
npm install
npm run dev
\`\`\`

O servidor Vite escuta em \`127.0.0.1\`. Para validar:

\`\`\`bash
npm test
npm run build
\`\`\`

Consulte [apps/web/README.md](apps/web/README.md) para detalhes da estrutura e limitações atuais.

## Segurança do leitor de artefatos

O leitor Python realiza inspeção estática: não executa nem compila arquivos importados. Os limites atuais incluem fonte 2 MiB, binário 8 MiB, texto HEX 4 MiB, até 65.536 registros Intel HEX, span decodificado 1 MiB, lacuna 64 KiB, saída combinada do \`objdump\` 64 KiB e timeout de 20 segundos.

O parser Intel HEX exige EOF único e terminal, valida checksum e estrutura, rejeita sobreposições e limita endereços e alocações esparsas. O \`objdump\` é iniciado sem shell, com ambiente reduzido, timeout e saída drenada sob limite.

Esses controles não equivalem a uma sandbox. Não use o BinLab como ambiente de execução de arquivos não confiáveis. A exposição do leitor pela API está bloqueada até a conclusão da Issue #2, incluindo testes de fronteira/fuzzing e revisão complementar.

## Arquitetura

O objetivo é um **monólito modular**, não uma coleção prematura de microserviços:

\`\`\`text
apps/web (React/TS) ──────┐
                         ├── HTTP /api/v1 ── FastAPI adapter
apps/desktop (Tauri) ────┘                         │
                                           Application services
                                                   │
                                            Python domain
                                                   │
                                      Infrastructure adapters
                                      SQLite · filesystem · tools
\`\`\`

O domínio não depende de frameworks, interfaces, banco de dados ou sistema operacional. A aplicação Web não acessa filesystem ou banco diretamente. Contratos HTTP serão versionados e documentados em OpenAPI. A execução local deverá aplicar controles explícitos de origem, autenticação, CSRF, Host e DNS rebinding.

## Estrutura do repositório

\`\`\`text
src/binlab/                 núcleo Python, CLI, GUI e leitor estático
apps/web/                   aplicação React/TypeScript
apps/desktop/               integração Tauri (planejada)
docs/                       arquitetura, contratos, auditoria e roadmap
doc/                        documentação da versão Python atual
tests/                      testes Python
images/                     identidade visual e diagramas
.github/workflows/          CI e automações de release
\`\`\`

## Roadmap

1. Estabilização e auditoria de segurança.
2. Backend de aplicação e contratos HTTP seguros.
3. Aplicação Web modular e responsiva.
4. Integração desktop via Tauri.
5. Binary & Logic Lab e Architecture Lab.
6. Compiler, Operating Systems, Network e Security Labs.
7. Computação científica, dados e IA local.
8. Persistência de experimentos e distribuição.

O avanço de cada etapa depende de testes, documentação, critérios de aceite e revisão. A API permanece bloqueada pela [Issue #2](https://github.com/mnl-nox/BinLab/issues/2).

## Documentação

- [Plano de entregas](docs/ROADMAP.md)
- [Arquitetura alvo](docs/architecture/overview.md)
- [Arquitetura da aplicação Web](docs/architecture/web-application.md)
- [Contratos](docs/contracts/README.md)
- [Modelo de ameaças](docs/security/threat-model.md)
- [Auditoria técnica](docs/audit/2026-11-02-code-review.md)
- [Licenciamento](docs/legal/LICENSING.md)
- [Privacidade](docs/legal/PRIVACY.md)
- [Política de segurança](SECURITY.md)
- [Contribuição](CONTRIBUTING.md)
- [Histórico de alterações](CHANGELOG.md)

## Qualidade

O CI valida Python 3.8 e 3.13, executa testes unitários, verifica compilação e constrói wheel/sdist. O job Web instala dependências, executa testes Vitest e gera build de produção.

## Autoria e licença

Copyright © Manoel E. S. S — mnl-nox. Distribuído sob a licença MIT; consulte [LICENSE](LICENSE).
