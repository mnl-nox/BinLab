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
- `src/data/`: definições estáticas dos laboratórios e metadados de navegação.
- `src/components/`: shell compartilhado, sidebar e topbar.
- `src/labs/`: módulos funcionais isolados por laboratório.
- `src/styles.css`: tokens visuais, temas e responsividade.
- `src/main.tsx`: bootstrap da aplicação.

O domínio numérico não importa React. O estado de tema pertence ao shell visual e não compartilha estado, eventos ou dependências com agentes de IA.

## Limites desta entrega

- Não existe backend FastAPI integrado.
- Não existe persistência de projetos ou experimentos.
- Não existe execução de código C, Assembly ou binários.
- Os demais laboratórios ainda não estão implementados.
- O cliente HTTP será introduzido junto com um contrato de API revisado e seguro. Não configure endpoints fictícios.
- As operações BigInt usam semântica de inteiros com sinal e extensão de sinal; não simulam automaticamente registradores de largura fixa.

A API de inspeção de artefatos permanece bloqueada pela Issue #2 até a conclusão dos testes de fronteira/fuzzing e revisão de segurança.
