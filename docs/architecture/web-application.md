# Aplicação Web — arquitetura da primeira entrega

## Escopo

A interface Web reside em `apps/web/` e é um projeto React + TypeScript com Vite e Tailwind CSS. Nesta etapa, é executada localmente como aplicação frontend independente. Ela não inicia, presume ou simula um backend.

## Fronteiras

- `src/domain/`: funções puras para parsing, conversão e operações binárias.
- `src/data/`: metadados e definições estáticas dos laboratórios.
- `src/components/`: composição visual compartilhada (sidebar e topbar).
- `src/labs/`: módulos funcionais isolados; cada laboratório possui seu próprio estado e interface.
- `src/App.tsx`: composição do shell e roteamento local inicial.
- `src/styles.css`: sistema visual, temas e breakpoints.
- `src/main.tsx`: ponto de entrada.

O domínio numérico não importa React. Componentes não devem implementar parsing ou regras numéricas diretamente. A alternância de tema é responsabilidade do shell e não depende de agente de IA.

## Contratos e integração futura

A integração HTTP será adicionada em módulo próprio (cliente tipado/adaptador), após a implementação e revisão dos casos de uso no backend. Componentes não acessarão filesystem, SQLite ou endpoints diretamente.

O contrato esperado será versionado em `/api/v1`, com erros Problem Details (RFC 9457), limites explícitos e OpenAPI. Não se deve adicionar fallback silencioso para serviços remotos.

## Segurança

- Vite e preview escutam em loopback (`127.0.0.1`) por padrão.
- Nenhum arquivo é enviado ou executado.
- Parsing numérico limita a entrada a 4096 dígitos e a representação a 4096 bits.
- Deslocamentos são limitados a 4096 posições; o resultado também é limitado a 4096 bits.
- O frontend não implementa autenticação nem substitui controles de origem, CSRF, Host e DNS rebinding que serão exigidos no serviço local.
- Não usar `dangerouslySetInnerHTML` para conteúdo de usuário.

## Precisão e semântica numérica

A implementação usa JavaScript `BigInt` para preservar precisão inteira acima do limite de `Number`. Operações bit a bit de BigInt têm semântica de inteiro com sinal e extensão de sinal; isso não é equivalente a um registrador físico de largura fixa. Simulações de N bits deverão receber largura explícita e aplicar máscaras/overflow documentados.

## Estado de implementação

Implementado: shell responsivo, navegação por laboratórios, tema independente, conversor de bases e operações AND/OR/XOR/shift-left locais.

Planejado: cliente HTTP, estados de rede, persistência, visualizações avançadas, Tauri e integração com API. A interface deve rotular claramente recursos indisponíveis.
