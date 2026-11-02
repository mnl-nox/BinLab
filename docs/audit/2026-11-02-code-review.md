# Auditoria técnica e de segurança — 2026-11-02

## Escopo e método

Revisão estática dos arquivos da branch principal `main` e da estrutura da entrega de fundação: `artifact_reader.py`, domínio numérico/lógico, CLI, GUI Tkinter, `pyproject.toml`, testes e workflows GitHub Actions.

Esta revisão não executou o código, não rodou fuzzing, não fez análise dinâmica, não validou o comportamento em todas as versões de Python e não é auditoria formal de segurança. Os achados abaixo são evidências do código-fonte e riscos a reproduzir/corrigir. A aprovação do CI ainda é necessária.

## Resumo executivo

O domínio matemático é pequeno e tem testes unitários básicos. O principal risco está no leitor de artefatos: entrada sem limites de tamanho, reconstrução Intel HEX com alocação baseada no maior endereço e captura integral da saída de subprocessos. Essas rotas não devem ser expostas por API antes do hardening.

## Achados

### BL-SEC-001 — Leitura de arquivos sem limite de tamanho

- **Severidade:** Alta
- **Arquivo:** `src/binlab/artifact_reader.py`
- **Evidência:** `inspect_file()` usa `Path.read_bytes()`; `inspect_source()` usa `Path.read_text()`. Não há limite máximo antes da leitura.
- **Impacto:** um arquivo grande pode consumir memória e CPU, degradando ou encerrando o processo.
- **Correção requerida:** impor limite configurável e documentado antes da leitura; ler em blocos ou validar tamanho de forma segura; testar arquivos acima do limite, arquivos que crescem durante a leitura e arquivos especiais/symlinks conforme a política de acesso.
- **Bloqueia:** exposição do leitor pela API e processamento em lote.

### BL-SEC-002 — Intel HEX esparso pode provocar alocação desproporcional

- **Severidade:** Alta
- **Arquivo:** `src/binlab/artifact_reader.py::parse_hex_text`
- **Evidência:** para um registro de dados cujo endereço absoluto excede `len(result)`, o parser estende o `bytearray` com zeros até esse endereço.
- **Impacto:** poucos bytes de entrada podem solicitar uma região de memória enorme.
- **Correção requerida:** impor limites independentes para bytes de entrada, endereço máximo, extensão total e lacunas; preferir representação esparsa por segmentos e só materializar quando o consumidor solicitar dentro de um limite.
- **Bloqueia:** exposição do parser por API.

### BL-SEC-003 — Validação incompleta do protocolo Intel HEX

- **Severidade:** Média
- **Arquivo:** `src/binlab/artifact_reader.py::parse_hex_text`
- **Evidência:** o parser interrompe no primeiro tipo EOF sem validar todos os campos do EOF; aceita arquivo sem EOF; ignora linhas posteriores ao EOF; tipos de início 03/05 não validam comprimento; registros sobrepostos são sobrescritos silenciosamente.
- **Impacto:** entrada malformada pode ser aceita com interpretação ambígua ou incompleta.
- **Correção requerida:** validar rigorosamente comprimento, endereço, tipo, checksum, EOF obrigatório e único, sequência de registros e política para sobreposição. Rejeitar dados após EOF.
- **Testes requeridos:** EOF ausente/duplicado/malformado, registro após EOF, tipo desconhecido, contagem incompatível, checksum incorreto, sobreposição e endereços de fronteira.

### BL-SEC-004 — Saída de objdump só é limitada depois de capturada

- **Severidade:** Média/Alta
- **Arquivo:** `src/binlab/artifact_reader.py::_objdump_file` e `disassemble_hex_bytes`
- **Evidência:** `subprocess.run(..., capture_output=True)` captura stdout e stderr integralmente; o corte em 16.000 caracteres ocorre depois.
- **Impacto:** arquivo que provoque saída extensa pode consumir memória antes do truncamento. Timeout de 20 segundos limita duração, não tamanho de saída.
- **Correção requerida:** limitar stdout/stderr durante a execução, impor tamanho de entrada, timeout, ambiente mínimo e política para binário `objdump`. Considerar sandbox para análise de artefatos hostis.
- **Nota:** a invocação atual usa lista de argumentos e não usa `shell=True`, o que reduz risco de injeção de shell; não elimina riscos no parser nativo chamado.

### BL-SEC-005 — Operações de bits sem limites de largura/deslocamento

- **Severidade:** Média
- **Arquivos:** `src/binlab/domain/operations.py`, `src/binlab/domain/analysis.py`, CLI e GUI
- **Evidência:** `calculate()` permite largura arbitrária em NOT e deslocamento arbitrário; `analyze_bits()` aceita sequências sem limite.
- **Impacto:** entradas locais muito grandes podem provocar consumo elevado de memória/CPU. O risco torna-se remoto se essas funções forem expostas sem limites na API.
- **Correção requerida:** definir limites explícitos de bits, tamanho de entrada e deslocamento na camada de aplicação; validar tipos inteiros estritos e rejeitar booleanos/floats quando o contrato exigir inteiro.
- **Nota arquitetural:** preservar domínio puro é possível; os limites de produto devem ser aplicados em serviços de aplicação e também nas interfaces locais.

### BL-SEC-006 — Extração de strings materializa todos os resultados

- **Severidade:** Média
- **Arquivo:** `src/binlab/artifact_reader.py::printable_strings`
- **Evidência:** regex cria uma lista de todas as sequências imprimíveis e só depois o relatório seleciona as primeiras 30.
- **Impacto:** custo de memória desnecessário em arquivos grandes.
- **Correção requerida:** extrair incrementalmente e parar após o limite de resultados ou impor limite de bytes analisados.

### BL-ENG-001 — Contratos de domínio dependem de type hints, não de validação de runtime

- **Severidade:** Média
- **Arquivos:** `domain/numeric.py`, `domain/operations.py`, `domain/analysis.py`
- **Evidência:** funções assumem que recebem `str` ou `int`; chamadas com tipos incompatíveis podem resultar em `AttributeError` ou comportamento inesperado em vez de erro de domínio consistente.
- **Correção requerida:** validar tipos na fronteira pública de domínio ou garantir DTOs estritos nos serviços de aplicação. Definir se `bool` é aceito como `int` (recomendação: não).

### BL-CI-001 — Actions referenciadas por tags mutáveis

- **Severidade:** Média (supply chain)
- **Arquivos:** `.github/workflows/*.yml`
- **Evidência original:** os workflows usavam tags mutáveis para `actions/checkout` e `actions/setup-python`.
- **Impacto:** uma tag de action pode mudar e alterar código executado no pipeline.
- **Status:** corrigido nesta branch para `actions/checkout` e `actions/setup-python` nos workflows de CI e release, com SHAs completos e comentários de versão; Dependabot semanal permanece habilitado. Revalidar periodicamente as referências e incluir qualquer action externa futura.
- **Referência:** GitHub recomenda pinning por SHA completo como a forma imutável de referenciar uma action: https://docs.github.com/en/actions/reference/security/secure-use

### BL-CI-002 — Workflow de release não repetia a suíte de testes

- **Severidade:** Média
- **Arquivo:** `.github/workflows/release.yml`
- **Status:** corrigido nesta branch; as etapas de compilação, instalação, importação, testes e build passaram na matriz Python 3.8/3.13 da execução CI #27.
- **Evidência original:** o workflow de tag verificava versão e construía distribuições, mas não compilava fontes nem executava testes.
- **Correção aplicada:** agora executa compileall, instalação, importação, unittest e build antes de criar o GitHub Release.

### BL-META-001 — Dados de autoria e contato

- **Severidade:** Baixa / documental
- **Status:** Resolvido nesta branch em 2 de novembro de 2026.
- **Correção aplicada:** titularidade declarada por Manoel E. S. S (mnl-nox), copyright atualizado em `LICENSE`, metadados `authors` atualizados em `pyproject.toml` e contato de privacidade publicado em `docs/legal/PRIVACY.md` (`ghostnether28@gmail.com`).
- **Arquivos:** `LICENSE`, `pyproject.toml`, README
- **Evidência original:** copyright usava “BinLab contributors” e metadados de autoria eram genéricos; não havia contato de privacidade.
- **Impacto:** atribuição legal e canal de solicitações ficam pouco específicos.
- **Resultado:** a confirmação foi fornecida pelo mantenedor. O endereço informado é publicado como contato do projeto e poderá ser coletado por crawlers/spam.

## Controles positivos observados

- O domínio numérico não depende de Tkinter ou CLI.
- O runtime Python atual não declara dependências de terceiros.
- A invocação de objdump usa lista de argumentos, não shell.
- O leitor não executa nem compila o artefato importado.
- CI declara `contents: read` no workflow de validação.
- Testes existentes cobrem conversão, operações básicas, análise de bits, HEX e leitura de fonte, mas ainda não cobrem os casos de abuso acima.

## Privacidade — observações do código

Na revisão das fontes consultadas não foram identificadas chamadas explícitas a HTTP, sockets, analytics ou telemetria na aplicação Python. A aplicação atual é local-first: arquivos são lidos localmente; objdump, quando habilitado, é executado localmente. Isso não equivale a uma auditoria de tráfego de todo o ambiente operacional.

O README carregava badges remotos de shields.io; eles foram removidos nesta branch para evitar requisições desnecessárias a esse terceiro ao visualizar a página do repositório. A hospedagem do repositório e seus logs continuam sob operação do GitHub e suas políticas.

## Estado da entrega documental

- Política de privacidade e documento de licenciamento adicionados em `docs/legal/`.
- README agora apresenta metadados estáticos, sem badges remotos.
- Metadados do pacote incluem URLs de projeto, issues e segurança.
- Workflow de release passou a executar testes antes da publicação.
- O arquivo `LICENSE` mantém a licença MIT válida e agora identifica o titular declarado pelo mantenedor: Manoel E. S. S (mnl-nox).
- O contato de privacidade informado pelo mantenedor foi publicado em `docs/legal/PRIVACY.md`; o endereço é público e não há SLA de resposta declarado.
- As actions usadas nos workflows de CI e release foram fixadas em SHAs completos verificados; Dependabot semanal está configurado em `.github/dependabot.yml`. A issue #3 permanece para governança adicional, revisão de permissões, SBOM/attestations e demais controles de supply chain.
- Correção de parser e limites de recursos está rastreada em [issue #2](https://github.com/mnl-nox/BinLab/issues/2).

## Resultado de validação CI

Na execução GitHub Actions #27, os dois jobs (Python 3.8 e 3.13) concluíram com `success`, incluindo compilação, instalação, importação, testes, build e limpeza pós-job. Essa execução antecede os commits finais de metadados legais e pinning de actions; a revisão final desta branch ainda exige execução CI associada ao HEAD atualizado.

## Portão de segurança antes da API

Não iniciar a etapa FastAPI até que BL-SEC-001 a BL-SEC-004 tenham correção e testes. Não aceitar upload, caminho de arquivo arbitrário ou análise de binário remoto antes de controles de tamanho, tempo, saída, isolamento e autenticação local. BL-SEC-005 e BL-SEC-006 devem ser resolvidos antes de publicar as operações do domínio como serviço.
