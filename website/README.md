# Website institucional — BinLab Engineering

Site estático oficial do projeto, publicado via GitHub Pages a partir de website/. O conteúdo documenta o produto e seu estado real; não é a aplicação React, não hospeda API e não executa os laboratórios.

## Conteúdo e identidade

- index.html: visão do produto, módulos, arquitetura, segurança, versão 0.3.2, pacotes Linux e roadmap.
- styles.css: sistema visual responsivo, temas e componentes de release.
- main.js: navegação móvel, acessibilidade por teclado e alternância de tema/logo.
- assets/binlab-logo.svg: logotipo horizontal oficial para tema escuro.
- assets/binlab-logo-light.svg: variante para tema claro.
- assets/binlab-mark.svg: símbolo vetorial usado como favicon.
- 404.html: página de rota não encontrada.

Os logotipos são cópias de distribuição dos ativos canônicos em branding/. A licença dos ativos visuais é CC BY 4.0; consulte [branding/LICENSE](../branding/LICENSE).

## Versão e distribuição

O site documenta BinLab 0.3.2. Os pacotes Linux x86_64 (.deb, .rpm e .tar.gz) foram construídos pelo CI; o DEB passou por instalação e smoke test no runner Ubuntu 22.04. O RPM foi construído e inspecionado, mas não instalado em Fedora/RHEL. A tag v0.3.2 e a GitHub Release pública ainda precisam ser criadas. O site aponta para o artefato temporário do workflow, não para URLs de download fictícias.

## Validação local

Na raiz do repositório:

~~~bash
python website/validate.py
node --check website/main.js
~~~

Abra website/index.html em um navegador ou sirva a pasta com um servidor HTTP estático local. Não é necessário instalar dependências externas.

## Publicação

O workflow .github/workflows/pages.yml valida e publica a pasta website/ em GitHub Pages. Actions externas estão fixadas em SHAs completos. O gatilho de push monitora website/** e o workflow.

**Configuração administrativa necessária:** em GitHub, abra **Settings → Pages → Build and deployment → Source** e selecione **GitHub Actions**. A integração de CI não possui permissão administrativa para alterar essa configuração.

Após habilitar Pages, um push em main que altere website/** dispara a publicação. URL esperada: [https://mnl-nox.github.io/BinLab/](https://mnl-nox.github.io/BinLab/). Ela só deve ser anunciada como publicada depois de um deploy bem-sucedido no workflow.

## Limites

O site institucional é uma camada de documentação e apresentação. A aplicação Web em apps/web/ é uma experiência separada e ainda não está integrada ao núcleo Python. API FastAPI, persistência, Tauri e os demais laboratórios permanecem planejados.
