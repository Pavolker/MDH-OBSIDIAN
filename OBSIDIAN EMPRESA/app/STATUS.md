---
title: "MDH EMPRESA — Status do App"
tags:
  - status
  - app
  - documentacao
created: 2026-05-12
---

# MDH EMPRESA — Status do Aplicativo

## O que existe hoje

### 1. BASE — Modelo Ideal (estrutura documental de referência)

| Item | Status |
|------|--------|
| 9 blocos funcionais definidos | ✅ |
| ~50 fichas documentais mapeadas | ✅ |
| Arquivos `.md` com frontmatter, tags e wikilinks | ✅ |
| Índices nomeados por bloco (ESTRATÉGICO, JURÍDICO, etc.) | ✅ |
| Grafo BASE animado (SVG puro, posições pré-computadas) | ✅ |
| Controles: play/pause, reset, passo, velocidade | ✅ |
| Barra de progresso e legenda com blocos | ✅ |

### 2. REAL — Diagnóstico da Empresa

| Item | Status |
|------|--------|
| Checklist por bloco com 3 estados (Sim / Parcial / Não) | ✅ |
| Persistência via localStorage | ✅ |
| Percentual de completude por bloco | ✅ |
| Alternância visual (checked/strikethrough) | ✅ |

### 3. GAP — Análise Comparativa

| Item | Status |
|------|--------|
| Resumo: OK / Parcial / Falta | ✅ |
| Detalhamento por bloco com barra de progresso | ✅ |
| Lista item a item com status | ✅ |
| Score geral (BASE% · REAL%) na topbar | ✅ |

### 4. App "O Cérebro" (backend FastAPI)

| Item | Status |
|------|--------|
| API REST com FastAPI | ✅ |
| Busca vetorial via pgvector | ✅ |
| Chat RAG com OpenRouter | ✅ |
| Sincronização com GitHub | ✅ |
| Indexação de vault local | ✅ |
| `.env` com chaves de API | 🔴 Removido do git (vazado anteriormente) |
| `.env.example` criado | ✅ |

### 5. Artefatos

| Arquivo | Função |
|---------|--------|
| `MDH_EMPRESA.html` | App unificado (BASE + REAL + GAP) — **front principal** |
| `ANIMACAO_EMPRESA.html` | Grafo animado standalone (legado) |
| `app/ARCHITECTURE.md` | Arquitetura do backend |
| `app/backend/main.py` | API FastAPI |
| `app/backend/index_local_vault.py` | Indexador de vault local |
| `app/frontend/` | SPA do "O Cérebro" |

### 6. GitHub

| Item | Status |
|------|--------|
| Repositório: `Pavolker/MDH-OBSIDIAN` | ✅ |
| Branch: `main` | ✅ |
| Último commit: `9dc0140` | ✅ |
| `.gitignore` com `**/.env` e `.DS_Store` | ✅ |

---

## Arquitetura do MDH EMPRESA (conceitual)

```
┌──────────────────────────────────────────────────────────────┐
│                     MDH EMPRESA (App)                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐          │
│  │      ❶ BASE         │    │      ❷ REAL          │          │
│  │  (modelo ideal)     │    │  (diagnóstico)       │          │
│  │  ┌───────────────┐  │    │  ┌───────────────┐   │          │
│  │  │ 9 blocos      │  │    │  │ checklist     │   │          │
│  │  │ ~50 fichas .md│  │    │  │ localStorage  │   │          │
│  │  │ grafo animado │  │    │  │ grafo real     │   │          │
│  │  └───────────────┘  │    │  └───────────────┘   │          │
│  └─────────┬───────────┘    └──────────┬────────────┘          │
│            │                           │                       │
│            └──────────┬────────────────┘                      │
│                       ▼                                       │
│  ┌──────────────────────────────────────────┐                 │
│  │             ❸ GAP                         │                 │
│  │  BASE ⟷ REAL → o que falta / parcial / ok │                 │
│  │  score geral + plano de ação sugerido     │                 │
│  └──────────────────────────────────────────┘                 │
│                                                              │
│  ┌──────────────────────────────────────────┐                 │
│  │        ❹ O Cérebro (backend opcional)     │                 │
│  │  FastAPI · pgvector · GitHub sync · Chat  │                 │
│  └──────────────────────────────────────────┘                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Próximos passos sugeridos

1. **Testar `MDH_EMPRESA.html`** em diferentes navegadores e tamanhos de tela
2. **Adicionar exportação** do relatório GAP (PDF/CSV)
3. **Melhorar layout dos nós** no grafo BASE (evitar sobreposição)
4. **Adicionar modo escuro/claro** (já está escuro, mas pode ter toggle)
5. **Conectar com "O Cérebro"** — usar o backend para persistir REAL em banco
6. **Deploy** — colocar frontend no Netlify, backend no Railway

---

> *Registro gerado em 2026-05-12 · Commit `9dc0140`*
