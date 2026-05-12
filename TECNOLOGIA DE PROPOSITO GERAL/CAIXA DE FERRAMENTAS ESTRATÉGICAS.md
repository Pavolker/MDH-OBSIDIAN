---
title: "Caixa de Ferramentas Estratégicas"
tags:
  - tpg
  - hermes
  - ferramentas
  - arquitetura
  - agentes
created: 2026-05-12
aliases:
  - "Hermes"
  - "Arquitetura Hermes"
---

# Caixa de Ferramentas Estratégicas

## 1. Sistema de skills auto-melhorável
Skills são documentos markdown com frontmatter YAML que persistem procedimentos reutilizáveis. Carregadas no prompt via skill_view(), eliminam a necessidade de re-aprender workflows. O Hermes pode criar, corrigir e evoluir skills autonomamente — é um sistema de memória procedural que melhora com o uso.

2. Ferramentas como módulos registráveis
Cada ferramenta é um arquivo Python em tools/ com registry.register(), schema JSON e check_fn para disponibilidade condicional. Não há lista manual — descoberta automática por import. Ferramentas novas aparecem para o LLM automaticamente quando os requisitos são atendidos.

3. Gateway multi-plataforma
Um único loop de agente conectado a 15+ plataformas (Telegram, Discord, Slack, WhatsApp, Signal, Email, Matrix, etc.) via adaptadores modulares em gateway/platforms/. Comandos como /sethome, /approve//deny e /restart operam no runtime do gateway sem modificar o núcleo do agente.

4. Delegacão de subagentes (delegate_task)
Subagentes com contextos isolados, sessões de terminal próprias e toolsets independentes. Suporte a paralelismo (até 3 por vez, configurável) e orchestrators aninhados (profundidade máxima configurável). Útil para pesquisa simultânea, debugging isolado e tarefas que poluiriam o contexto principal.

5. Memória persistente cross-session
Dois alvos: user (perfil, preferências) e memory (fatos ambientais, convenções, lições). Backends plugáveis (built-in, Honcho, Mem0). Memória é injetada automaticamente no prompt a cada turno — o agente não precisa "lembrar" de consultar.

6. Provedor-agnóstico com credential pools
20+ provedores suportados via interface unificada OpenAI-format. Credential pools rotacionam múltiplas chaves API automaticamente. Dá para trocar de modelo/provedor no meio do fluxo sem reiniciar.

7. Cron jobs auto-contidos
Jobs agendados que rodam em sessões limpas (sem contexto do chat atual). Suporte a scripts de coleta pré-execução, encadeamento entre jobs, skills pre-carregadas e override de modelo/provedor. Entrega automática para a plataforma de origem.

8. Compressão de contexto adaptativa
Aciona automaticamente perto do limite de tokens. Taxa de compressão e limiar configuráveis. Sem quebra de prompt caching — a compressão acontece entre turnos, não no meio.

9. ACP (Agent Communication Protocol)
Permite que outros agentes (Claude Code, Codex) se comuniquem com o Hermes via protocolo padronizado. O Hermes também pode atuar como servidor ACP via hermes acp para integração com IDEs.

10. Sistema de checkpoints
Snapshots do filesystem via /rollback — permite restaurar estado anterior após mudanças destrutivas. Até 50 snapshots simultâneos.

---

A capacidade mais distintiva em termos de implementação é o sistema de skills auto-melhorável combinado com memória persistente: o Hermes não apenas executa tarefas, mas acumula conhecimento operacional ao longo do tempo, tornando-se progressivamente mais eficiente no ambiente e nos padrões de trabalho do usuário.

---

## Ver também

- [[TECNOLOGIA DE PROPOSITO GERAL/_Index TPG|índice TPG]]
- [[CONCEITOS|Conceitos]] — Glossário dos conceitos TPG
- [[Fundamentos Estratégicos]] — Os 5 pilares estratégicos
- [[TPG - Educação]] — Aplicação na educação
- [[TPG - Empresa]] — Aplicação nas empresas
- [[SISTEMA CENTAURO/_Index Sistema Centauro|Sistema Centauro]] — Framework conceitual relacionado