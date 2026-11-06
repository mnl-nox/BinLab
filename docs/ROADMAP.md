# BinLab Engineering — plano de entregas

## Objetivo

Evoluir o BinLab para um laboratório de engenharia computacional local-first, com interfaces Web e desktop, preservando o domínio Python existente. A arquitetura inicial será um **monólito modular**: um único backend implantável, módulos internos com fronteiras explícitas e contratos versionados. Microserviços não fazem parte do escopo inicial.

## Princípios de engenharia

1. O domínio não importa FastAPI, Tkinter, React, Tauri, banco de dados ou sistema operacional.
2. Casos de uso coordenam domínio e portas; adaptadores implementam portas.
3. Toda entrada externa é validada na fronteira correspondente.
4. Nenhum artefato importado é executado automaticamente.
5. Persistência e rede são explícitas; o modo local não depende de serviços em nuvem.
6. Cada entrega possui testes, documentação, critérios de aceite e migração reversível.
7. Dependências só entram quando resolvem uma necessidade demonstrada.
8. APIs são versionadas e descritas por OpenAPI; modelos internos não são expostos diretamente.

## Entregas

| Etapa | Entrega | Resultado verificável |
|---|---|---|
| 0 | Fundação e auditoria | Contratos, threat model, CI, qualidade e baseline documentados |
| 1 | Backend de aplicação | Serviços desacoplados e API HTTP local versionada |
| 2 | Aplicação Web | React/TypeScript, navegação por laboratórios e consumo da API |
| 3 | Desktop | Tauri integrado ao serviço local com lifecycle e autenticação |
| 4 | Binary & Logic Lab | Conversões, operações, análise de bits e circuitos simulados |
| 5 | Architecture Lab | ISA, CPU, memória, cache, pipeline e visualizações |
| 6 | Compiler & OS Labs | Toolchain, ELF, ABI, processos, memória virtual e sistemas de arquivos |
| 7 | Network & Security Labs | Protocolos, análise estática, diagnóstico e experimentos controlados |
| 8 | Scientific + AI/Data Labs | Computação científica, dados e inferência local opcional |
| 9 | Persistência e projetos | SQLite, experimentos reproduzíveis, evidências e exportação |
| 10 | Release e distribuição | Builds reproduzíveis, instaladores, SBOM e pipeline de publicação |

As etapas podem ter subentregas menores. Uma etapa só é considerada concluída quando seus critérios de aceite passam no CI e a documentação descreve limitações conhecidas.

## Estado atual — 2026-11-06

- [x] Branch isolada para a fundação Web.
- [x] Estrutura inicial React + TypeScript + Vite + Tailwind em \`apps/web/\`.
- [x] Navegação responsiva e tema independente.
- [x] Conversão de bases e operações binárias locais com BigInt.
- [x] Testes de domínio e job de CI para testes/build Web adicionados.
- [x] CI de Python, Web e pacote Linux concluído na integração da versão 0.3.2.
- [ ] Revisão funcional, acessibilidade e responsividade em navegador.
- [ ] Cliente HTTP tipado e contratos de integração, somente após definição da API.
- [ ] Backend FastAPI: bloqueado pela Issue #2 até fuzz/property tests, testes de fronteira e revisão complementar.
- [x] Site institucional documentado com versão 0.3.2, capacidades reais, identidade visual canônica e distribuição Linux.
- [x] Workflow GitHub Pages e validação de links configurados.
- [ ] Habilitar GitHub Pages em Settings → Pages e confirmar o primeiro deploy/URL pública.
- [ ] Criar a tag `v0.3.2` para publicar a GitHub Release e anexar os pacotes Linux; os artefatos atuais do CI são temporários.
- [ ] Integração Tauri e persistência: etapas posteriores.

## Etapa 0 — critérios de aceite

- [ ] Branch de trabalho isolada da branch principal.
- [x] Arquitetura alvo e decisões registradas.
- [x] Contratos de domínio, aplicação e API documentados.
- [x] Ameaças e controles mínimos documentados.
- [x] CI executa testes, valida compilação e constrói distribuição Python.
- [x] Testes existentes preservados.
- [ ] Nenhuma mudança quebra CLI/GUI legadas (validar no CI desta PR).
- [x] Riscos e débitos técnicos registrados.

## Etapa 1 — Backend

- FastAPI fica em adaptador HTTP, fora de \`domain/\`.
- \`application/\` define casos de uso e portas.
- Rotas chamam serviços; não implementam regras de negócio.
- API começa em \`/api/v1\`, com OpenAPI gerado e exemplos de contrato.
- Erros seguem Problem Details (RFC 9457).
- Limites de tamanho, timeout, CORS restrito e autenticação local são obrigatórios antes de expor operações sensíveis.
- **Bloqueio:** não expor o leitor nem operações irrestritas até encerrar a [Issue #2](https://github.com/mnl-nox/BinLab/issues/2).

## Etapa 2 — Web

- React + TypeScript com cliente API tipado.
- Componentes de interface não acessam banco nem filesystem diretamente.
- Estados de carregamento, erro, vazio e sucesso definidos.
- Acessibilidade por teclado e semântica HTML testadas.
- A aplicação Web é servida localmente pelo backend ou por origem de desenvolvimento explicitamente permitida.
- A primeira fundação está em \`apps/web/\`; não representa integração HTTP concluída.

## Etapa 3 — Desktop

- Tauri é o shell; não duplica lógica de domínio.
- O backend é iniciado e encerrado pelo processo desktop com lifecycle supervisionado.
- Porta local dinâmica, segredo efêmero e verificação de origem são preferidos a porta fixa aberta.
- Não habilitar shell genérico, acesso irrestrito a arquivos ou permissões amplas.
- Falha ao iniciar o backend deve ser visível e recuperável.

## Contrato de entrega

Cada pull request informa: etapa, escopo, decisões, arquivos alterados, testes executados, riscos, documentação atualizada e passos de rollback. Não se marca uma etapa como pronta apenas porque o código compila.
