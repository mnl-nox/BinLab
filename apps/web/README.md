# BinLab Engineering — Web

Aplicação React + TypeScript executada localmente. Esta entrega é uma fundação de interface: o Binary & Logic Lab executa conversões e operações no navegador usando `BigInt`; os demais laboratórios são marcados explicitamente como planejados.

## Requisitos

- Node.js 20 ou superior.
- npm 10 ou superior.

## Desenvolvimento

Na raiz do repositório:

```bash
cd apps/web
npm install
npm run dev
```

O Vite escuta em `127.0.0.1`. A interface de desenvolvimento normalmente fica disponível em `http://127.0.0.1:5173`.

## Verificação

```bash
npm test
npm run build
```

## Organização

- `src/domain/`: operações numéricas puras, sem dependência de React.
- `src/App.tsx`: composição da experiência e navegação entre laboratórios.
- `src/styles.css`: tokens visuais, temas e responsividade.
- `src/main.tsx`: bootstrap da aplicação.

O tema é estado de apresentação isolado. Não compartilha estado, eventos ou dependências com agentes de IA.

## Limites desta entrega

- Não existe backend FastAPI integrado.
- Não existe persistência de projetos ou experimentos.
- Não existe execução de código C, Assembly ou binários.
- Os laboratórios ainda não implementados aparecem como planejados, sem simular funcionalidades.
- O cliente HTTP será introduzido junto com um contrato de API revisado e seguro. Não configure endpoints fictícios.

A API de inspeção de artefatos permanece bloqueada pela Issue #2 até a conclusão dos testes de fronteira/fuzzing e revisão de segurança.
