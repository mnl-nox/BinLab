# Modelo de ameaças — BinLab local-first

## Escopo

O BinLab inspeciona dados binários e fontes fornecidas pelo usuário. A evolução adicionará um servidor HTTP local, interface Web/Desktop e persistência. O modelo considera entradas não confiáveis, processos locais e origens Web potencialmente hostis.

## Ativos

- Arquivos e diretórios do usuário.
- Integridade do ambiente e do processo BinLab.
- Dados locais de projetos e experimentos.
- Segredos de sessão e configuração.
- Disponibilidade do serviço local.

## Atores e ameaças

| Ameaça | Cenário | Controle requerido |
|---|---|---|
| Arquivo malformado | Parser recebe entrada truncada ou hostil | Limites de tamanho, validação estrita e testes fuzz |
| DoS local | Arquivo enorme ou endereço HEX esparso causa alocação excessiva | Limites de bytes, endereços, memória e tempo |
| Execução indireta | Entrada controla comando externo | subprocess com argv, sem shell, opções validadas e timeout |
| Acesso a arquivos | Caminho manipulado alcança arquivos fora do escopo | Seleção explícita, normalização e política de acesso |
| CSRF/DNS rebinding | Site externo tenta acessar serviço em loopback | Token por sessão, validação Host/Origin, CORS restrito e proteção CSRF |
| Exposição de serviço | API escuta em interface pública | Bind loopback por padrão e firewall não presumido |
| Vazamento em logs | Tokens, conteúdo de arquivo ou caminhos sensíveis são registrados | Redação e minimização de logs |
| Supply chain | Dependência ou action comprometida | Dependências mínimas, versões controladas, revisão e auditoria |

## Requisitos de segurança

1. Nunca executar artefatos importados automaticamente.
2. Limitar tamanho de arquivos, conteúdo decodificado, saída de subprocessos e tempo de execução.
3. Invocar ferramentas externas sem shell e com argumentos validados.
4. Não aceitar bind público por padrão.
5. Autenticar todas as rotas não públicas; CORS sozinho não é autenticação.
6. Validar Host e Origin para serviço loopback.
7. Não persistir tokens em código, URLs, logs ou repositório.
8. Usar permissões mínimas no Tauri e no GitHub Actions.
9. Não expor traceback, segredo, caminho interno ou dados do usuário em respostas HTTP.
10. Adicionar testes de abuso para parsers, rotas e integração com subprocessos.

## Limites conhecidos

O leitor atual tem inspeção estática e chama opcionalmente GNU objdump. A auditoria desta etapa identificou que os caminhos de leitura não declaram limites globais de tamanho e que a reconstrução Intel HEX pode materializar regiões esparsas em memória. Esses pontos devem ser corrigidos e testados antes de expor o leitor por API.

Este documento é um modelo inicial, não uma certificação nem uma garantia de segurança. Deve ser revisado a cada novo laboratório e fronteira de execução.
