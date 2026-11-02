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

## Limites do leitor de artefatos

| Entrada/operação | Limite |
|---|---:|
| Fonte C/Assembly | 2 MiB |
| Arquivo binário | 8 MiB |
| Texto HEX/Intel HEX | 4 MiB |
| Saída decodificada HEX | 1 MiB |
| Lacuna Intel HEX entre registros | 64 KiB |
| Strings ASCII retornadas | 30, com até 160 caracteres cada |
| Saída combinada do objdump | 64 KiB durante a drenagem dos pipes |
| Timeout do objdump | 20 segundos |
| Sequência binária analisada | 4096 bits |
| Operandos inteiros das operações | 4096 bits |
| Largura do NOT | 4096 bits |
| Distância de shift | 4096 posições |
| Texto numérico | 4096 dígitos |

Os limites são constantes internas do código, não parâmetros controláveis por entrada não confiável. Leitura de arquivos é limitada no próprio fluxo de leitura (limite + 1), e não apenas por uma verificação posterior de tamanho.

O parser Intel HEX exige EOF único e terminal, valida contagem, checksum, endereço e campos dos tipos de registro suportados, rejeita sobreposição e não materializa intervalos esparsos acima dos limites. A reconstrução final é uma região contígua limitada a 1 MiB.

O subprocesso usa argv sem shell, stdin fechado, ambiente reduzido, timeout e drenagem concorrente de stdout/stderr com teto combinado de memória. O limite de saída não depende de truncamento posterior a capture_output.

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

## Validação e limites residuais

A suíte de regressão cobre entradas excessivas, endereços esparsos, EOF, checksum, tipos, sobreposição, strings, tipos de runtime e flood/timeout de subprocesso. Testes determinísticos de abuso não substituem fuzzing contínuo nem revisão independente.

O leitor permanece estático: não executa nem compila os arquivos importados. A API não deve expor o leitor até que a suíte completa e a matriz de Python suportada passem no CI e a revisão da implementação seja concluída.

Este documento é um modelo inicial, não uma certificação nem uma garantia de segurança. Deve ser revisado a cada novo laboratório e fronteira de execução.
