# Arquitetura alvo

## Estilo

Monólito modular com separação por camadas. Um único backend local e uma base de código organizada por responsabilidades são mais simples de operar do que microserviços para o estágio atual do produto.

```text
Web (React/TS) ─────┐
                    ├── HTTP /api/v1 ── API adapter (FastAPI)
Desktop (Tauri) ────┘                         │
                                      Application services
                                              │
                                      Domain (Python puro)
                                              │
                                  Ports / interfaces
                                              │
                         Infrastructure adapters (SQLite, filesystem,
                              subprocess control, local config)
```

## Responsabilidades

- **domain/**: tipos, invariantes e regras puras. Sem I/O e sem dependências de framework.
- **application/**: casos de uso, coordenação, políticas e portas necessárias.
- **infrastructure/**: implementações de persistência, filesystem e processos externos.
- **api/**: schemas HTTP, rotas, autenticação, tratamento de erros e composição.
- **engines/**: motores especializados apenas quando houver fronteira funcional real; não criar subpacotes vazios por antecipação.
- **apps/web/**: interface Web e cliente HTTP tipado.
- **apps/desktop/**: shell Tauri e integração com o backend.

A CLI e a GUI Tkinter atuais permanecem adaptadores legados até que equivalentes sejam substituídos e testados. O núcleo existente não será movido em massa sem testes de caracterização.

## Regras de dependência

Dependências permitidas apontam para dentro:

- API → application → domain.
- Infrastructure implementa portas definidas pela application.
- Web/Desktop → API pública.
- Domain não importa qualquer camada externa.

É proibido importar CLI/GUI a partir de domínio ou serviços. A composição de implementações concretas ocorre no ponto de inicialização da aplicação.

## Contratos

- Contratos internos: interfaces/protocolos Python e DTOs de aplicação.
- Contrato HTTP: OpenAPI versionado em `/api/v1/openapi.json`.
- Erros HTTP: Problem Details, RFC 9457.
- Compatibilidade: mudanças incompatíveis exigem nova versão de API ou período de depreciação.
- Schemas HTTP não são reutilizados como entidades de domínio.

## Execução local e segurança

O backend deve escutar somente em loopback por padrão. A origem Web permitida deve ser explícita. CORS não substitui autenticação nem proteção contra CSRF/DNS rebinding. O desktop deve obter um segredo de sessão efêmero por canal privado de inicialização e enviá-lo em cada chamada. Não registrar segredos.

Operações de inspeção de arquivos devem impor limite de bytes, timeout e limite de saída. Processos externos são invocados com lista de argumentos, sem shell. Arquivos de entrada nunca são executados nem compilados automaticamente.

## Persistência

SQLite será introduzido somente na etapa de persistência, atrás de repositórios/portas. Migrações devem ser versionadas. Arquivos de usuário não serão armazenados no banco como blobs por padrão; metadados e referências controladas são preferidos.

## Observabilidade

Logs estruturados sem conteúdo sensível, IDs de correlação por requisição e erros reproduzíveis. Métricas locais só serão adicionadas quando houver consumidor concreto.
