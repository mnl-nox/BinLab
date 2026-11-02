# Website institucional

Site estático do BinLab Engineering. O conteúdo é servido diretamente pelo GitHub Pages; não utiliza backend, analytics, cookies ou serviços externos de fontes.

## Estrutura

- `index.html`: página institucional e documentação resumida.
- `styles.css`: identidade visual, temas, responsividade e acessibilidade.
- `main.js`: navegação móvel e alternância de tema.
- `assets/`: recursos estáticos locais.
- `404.html`: página de rota não encontrada.

## Publicação

O workflow `.github/workflows/pages.yml` empacota a pasta `website/` e publica em GitHub Pages. As actions externas estão fixadas em SHAs completos. O gatilho de push monitora alterações em `website/**` e no próprio arquivo do workflow; pushes em caminhos não monitorados não iniciam o deploy.

**Ação manual necessária:** em GitHub, abra **Settings → Pages → Build and deployment → Source** e selecione **GitHub Actions**. O token de CI não possui permissão administrativa para habilitar Pages automaticamente.

Depois de habilitar Pages, publique por uma destas formas:
- Em **Actions**, abra uma execução existente do workflow **Deploy GitHub Pages** e selecione **Re-run all jobs**; ou
- Faça uma alteração legítima em `website/**` ou em `.github/workflows/pages.yml` e envie-a para `main`, para acionar o gatilho de push.

A URL esperada é `https://mnl-nox.github.io/BinLab/`; ela só estará disponível após o primeiro deploy bem-sucedido.

## Limites

O site documenta o estado real do produto. A aplicação Web está em desenvolvimento; o site não executa nem hospeda o frontend da aplicação, não expõe uma API e não representa funcionalidades planejadas como disponíveis.
