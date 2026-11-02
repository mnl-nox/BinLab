# Política de privacidade — BinLab

**Responsável pelo projeto:** Manoel E. S. S (mnl-nox)  
**Contato para privacidade:** [ghostnether28@gmail.com](mailto:ghostnether28@gmail.com)  
**Data de vigência:** 2 de novembro de 2026  
**Versão do produto coberta:** BinLab 0.3.1 (aplicação Python CLI/Tkinter)

## 1. Escopo

Esta política descreve o tratamento de dados pela aplicação BinLab 0.3.1, conforme o código-fonte revisado. Ela não substitui as políticas dos serviços de terceiros usados para hospedar o repositório, distribuir ferramentas ou fornecer recursos externos.

A política deverá ser revisada quando forem adicionados API local, interface Web, Tauri, banco de dados, sincronização, telemetria, autenticação, analytics ou serviços de IA.

## 2. Como a versão atual funciona

A aplicação atual executa localmente no computador do usuário. Na revisão do código Python consultado:

- Não foram identificadas rotinas explícitas de analytics, telemetria, criação de conta ou envio de arquivos para servidores.
- Não foram identificadas chamadas explícitas de rede HTTP ou sockets na aplicação.
- Arquivos selecionados são lidos localmente para produzir relatórios.
- Quando solicitado, GNU `objdump` é iniciado como processo local para inspecionar o arquivo.
- A rotina de desassemblagem de bytes HEX usa arquivo temporário local e o remove ao encerrar o contexto.
- A versão atual não implementa sincronização em nuvem nem banco de dados próprio.

A afirmação acima descreve a implementação revisada, não garante ausência de tráfego originado pelo sistema operacional, Python, ferramentas externas, extensões, ambiente do usuário ou serviços de hospedagem.

## 3. Dados tratados

O usuário pode fornecer conteúdo de arquivos, código-fonte, sequências binárias e caminhos locais. Esses dados são processados para gerar conversões e relatórios. A aplicação pode calcular hash SHA-256 de dados binários para exibição no relatório.

A aplicação atual não mantém uma conta de usuário nem um serviço central do BinLab que receba esses dados. O usuário deve evitar importar arquivos que não tenha autorização para analisar e deve proteger os relatórios que contenham caminhos, strings ou informações confidenciais.

## 4. Armazenamento e retenção

A versão atual não possui armazenamento persistente de projetos ou histórico gerenciado pelo BinLab. Dados de arquivo são mantidos em memória durante o processamento. A rotina de desassemblagem HEX utiliza arquivo temporário local durante a operação.

O sistema operacional pode manter caches, backups, snapshots, logs ou dados de paginação fora do controle do BinLab. O usuário controla esses recursos e deve aplicar as políticas de retenção e criptografia do próprio ambiente.

## 5. Compartilhamento e terceiros

A aplicação atual não implementa envio intencional de conteúdo analisado a terceiros. O GNU `objdump` é executado localmente quando habilitado; ele é software externo instalado no sistema.

O repositório é hospedado pelo GitHub. Ao visitar páginas do repositório, baixar arquivos ou interagir com issues/pull requests, o GitHub pode tratar dados técnicos e de conta segundo sua própria política de privacidade. Recursos externos incorporados na página também podem receber requisições do navegador. A aplicação instalada e a página de hospedagem são contextos distintos.

## 6. Segurança

O usuário deve manter o sistema operacional atualizado e utilizar arquivos de origem confiável. O leitor é estático e não executa nem compila automaticamente os arquivos importados. Ainda assim, parsers e ferramentas nativas podem conter vulnerabilidades.

A auditoria de 2 de novembro de 2026 identificou limites de tamanho, alocação Intel HEX e captura de saída de subprocesso que precisam de correção antes de expor o leitor por API. Consulte [relatório de auditoria](../audit/2026-11-02-code-review.md).

## 7. Direitos e legislação

O responsável pelo projeto é Manoel E. S. S (identificador público: `mnl-nox`). Na versão atual, o mantenedor não opera um serviço central de contas ou coleta intencional de dados pessoais por telemetria. Direitos relacionados a dados tratados pelo GitHub ou por outros provedores devem ser exercidos diretamente junto a esses provedores.

Se uma versão futura passar a tratar dados pessoais, o projeto deverá documentar finalidade, base legal, categorias de dados, retenção, compartilhamentos, canal do titular e medidas de segurança aplicáveis, inclusive conforme a Lei Geral de Proteção de Dados Pessoais (LGPD, Lei nº 13.709/2018), quando aplicável.

## 8. Crianças e dados sensíveis

O BinLab não foi projetado para coletar dados pessoais de crianças ou dados pessoais sensíveis. Não importe tais dados sem necessidade, autorização e salvaguardas apropriadas.

## 9. Mudanças nesta política

Esta política será atualizada quando o comportamento de tratamento de dados mudar. Alterações materiais deverão ser descritas no changelog e associadas à versão do software.

## 10. Contato e solicitações

Para solicitações relacionadas à privacidade e ao tratamento de dados no âmbito do projeto, entre em contato com o responsável:

**Manoel E. S. S (mnl-nox)**  
**E-mail:** [ghostnether28@gmail.com](mailto:ghostnether28@gmail.com)

Não envie senhas, tokens, arquivos privados ou outros dados sensíveis por e-mail sem necessidade. Não publique dados pessoais, arquivos privados ou segredos em issues públicas.

O contato acima é um canal de comunicação do mantenedor; não representa, por si só, um serviço de atendimento com prazo de resposta garantido.
