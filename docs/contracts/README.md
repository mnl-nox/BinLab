# Catálogo de contratos

Este diretório registra contratos estáveis entre camadas e interfaces. O contrato HTTP público será publicado em OpenAPI na etapa 1; este catálogo não substitui o schema gerado.

## Contratos atuais (baseline)

O domínio existente expõe a API Python em `binlab.domain`:

- `parse_integer(value, base)`
- `format_integer(value, base)`
- `convert_integer(value, source_base, target_base)`
- `calculate(a, operator, b=None, width=None)`
- `analyze_bits(bits)`
- `truth_table_rows()`

As funções e seus tipos de retorno existentes devem ser tratados como compatibilidade pública até uma mudança versionada e coberta por testes. Os objetos de análise não devem ser convertidos em schemas HTTP dentro do domínio.

## Contratos planejados

### Application

Cada caso de uso recebe DTOs explícitos e retorna resultado tipado. Erros de validação, recurso inexistente, limite excedido e falha de infraestrutura são categorias distintas. A camada de aplicação não conhece Request/Response HTTP.

### HTTP

- Prefixo: `/api/v1`.
- Schema: `/api/v1/openapi.json`.
- Health: `GET /api/v1/health` (somente estado do processo; sem revelar configuração sensível).
- Conversão, cálculo e análise serão endpoints separados por caso de uso.
- Erros: `application/problem+json`, conforme RFC 9457.
- Limites e formatos de entrada documentados no OpenAPI.

### Compatibilidade

Não remover nem renomear campos/endpoints sem versionamento. Campos novos devem ser opcionais quando compatível. Erros devem manter um formato previsível, sem traceback ou caminhos internos no payload público.

## Regras de revisão

Toda mudança de contrato exige atualização de schema, exemplos, testes de contrato e notas de compatibilidade no mesmo pull request.
