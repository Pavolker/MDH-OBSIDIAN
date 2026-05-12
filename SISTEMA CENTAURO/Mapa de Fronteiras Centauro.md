---
title: "Mapa de Fronteiras Centauro"
tags:
  - sistema-centauro
  - framework
  - agencia-humano-ia
  - higiene-cognitiva
  - paper
created: 2026-05-12
aliases:
  - "MFC"
  - "Mapa de Fronteiras"
---

# Mapa de Fronteiras Centauro: Um Framework Formal para Modelagem Dinâmica de Agência Humano-IA na Arquitetura do Sistema Centauro

**Paulo Volker**

---

 Resumo

A integração acelerada de modelos de Inteligência Artificial (IA), especialmente Large Language Models (LLMs) e sistemas autopoiéticos, em decisões de alto impacto expõe uma lacuna crítica: a ausência de linguagens formais para especificar, auditar e simular a divisão de trabalho cognitivo entre agentes humanos e artificiais. Labels genéricos como human-in-the-loop falham em especificar fronteiras de agência — delimitações precisas sobre quem detém autoridade decisória, sob quais condições e com quais protocolos de transição.

Este artigo apresenta o Mapa de Fronteiras Centauro (MFC) como um agente especializado inserido no Sistema Centauro, uma arquitetura em cinco camadas que organiza a relação humano–IA desde a leitura do cenário até as implicações existenciais de longo prazo. Especificamente alocado na Camada de Raciocínio e Higiene Cognitiva, o MFC: (i) formaliza a agência como função de estado-dependência entre agentes $H$ (humano) e $A$ (artificial); (ii) especifica protocolos de transição rigorosos (handoff, veto, escalonamento) baseados em incerteza epistêmica, risco ético e criticidade contextual; e (iii) fornece uma arquitetura de simulação para testar arranjos de automação antes da implementação.

Nossa contribuição central é uma formalização algébrica de fronteiras de agência como políticas $\pi: \mathcal{S} \rightarrow \mathcal{A} \times \mathcal{H}$, permitindo representar zonas de co-agência como estados de controle distribuído acoplado, operando no ponto crítico entre o diagnóstico do sujeito e a execução organizacional. Demonstramos a aplicabilidade através de um plano de avaliação em Design Science Research, com proposições testáveis sobre mitigação de automation bias e melhoria de coordenação sob falha.

Palavras-chave: Agência Humano-IA; Sistema Centauro; Controle Supervisório; Higiene Cognitiva; Governança de IA.

---

 1. Introdução

 1.1 O Problema da Agência Difusa e a Necessidade de Arquitetura

A quarta onda de automação, caracterizada pela proliferação de modelos generativos e sistemas de IA capazes de iniciar ações sem comando explícito, colocou em xeque os paradigmas tradicionais de interação humano-computador. Enquanto a literatura clássica de human-automation interaction (HAI) distingue níveis de automação em espectros lineares (De Winter & Dodou, 2014; Parasuraman et al., 2000), a realidade contemporânea exige modelagem de agência híbrida — estados onde humanos e IAs mantêm autoridade simultânea e mutuamente constrangedora sobre decisões.

A ambiguidade termina em falhas sistêmicas. Quando um médico aceita uma recomendação de diagnóstico gerada por LLM sem validar evidências (automation bias); quando um analista de risco não consegue justificar uma decisão de crédito porque o "modelo decidiu"; ou quando um operador de drone autoriza um ataque baseado em classificação automática — em todos esses casos, o defeito não é técnico, mas arquitetônico: a fronteira entre processamento algorítmico e discernimento humano foi deixada implícita, negociada ad hoc ou ignorada.

Grande parte das abordagens atuais descreve a interação em termos genéricos (human-in-the-loop, human-on-the-loop), sem explicitar as condições sob as quais o controle muda de mãos, nem os critérios que legitimam tais transições. Mais ainda, tratam a governança da IA como problema monolítico, ignorando que decisões complexas atravessam múltiplas camadas — do cenário ao sujeito, do raciocínio à execução organizacional.

 1.2 O Sistema Centauro como Contexto Integrador

Este artigo propõe o Mapa de Fronteiras Centauro não como artefato isolado, mas como componente essencial do Sistema Centauro, uma arquitetura conceitual que organiza a relação entre humanos e IA em cinco camadas funcionais: (1) Cenário (leitura do contexto); (2) Diagnóstico do Sujeito (avaliação do estado cognitivo/organizacional do decisor); (3) Raciocínio e Higiene Cognitiva (qualificação da decisão); (4) Organizacional e Econômica (execução e alocação de recursos); e (5) Existencial e Temporal (implicações de longo prazo).

Inserido especificamente na terceira camada, o MFC atua no núcleo do raciocínio estratégico, antes da execução (camada 4) e depois do entendimento do sujeito (camada 2). Sua função é explicitar limites: ao representar graficamente territórios de processamento algorítmico, territórios de discernimento humano e zonas de interação compartilhada, o MFC transforma conceitos abstratos como colaboração ou supervisão em arquiteturas decisórias concretas, rastreáveis e simuláveis.

 1.3 Contribuições

Este artigo funde a formalização matemática da agência com a especificidade arquitetural do Sistema Centauro para oferecer:

1. Uma definição operacional de fronteira de agência como política dinâmica $\mathcal{F}: \mathcal{S} \rightarrow \mathcal{P}(\{H, A\})$, operando na interface entre cognição individual e estrutura organizacional;
2. Uma taxonomia de territórios e protocolos de transição (handoff, veto, escalonamento) que qualificam o fluxo decisório antes de sua materialização em ações;
3. Um modelo de mitigação de riscos cognitivos (overreliance, automation bias, deskilling) através da higiene cognitiva estruturada;
4. Um plano de avaliação em Design Science Research com hipóteses testáveis sobre qualidade decisória e accountability.

O paper está organizado conforme rigor do Design Science Research (Hevner et al., 2004): fundamentação teórica e contexto sistêmico (Seção 2), formalização do constructo (Seção 3), operacionalização (Seção 4), hipóteses testáveis (Seção 5), método de avaliação (Seção 6) e implicações (Seção 7).

---

 2. Fundamentação Teórica e Contexto Sistêmico

 2.1 Ancoragens Teóricas: De Sheridan aos Joint Cognitive Systems

<details>
<summary><strong>Clique para expandir: Revisão das literaturas fundamentais</strong></summary>

Controle Supervisório e Níveis de Automação. Sheridan & Verplank (1978) estabeleceram o paradigma de controle supervisório, onde o humano atua como supervisor de "subordinados" automatizados. Parasuraman et al. (2000) estenderam para níveis de automação em estágios de processamento de informação (aquisição, análise, decisão, ação). O MFC herda essa estratificação, mas adiciona condicionalidade dinâmica: o nível de automação não é propriedade do sistema, mas variável de estado $\alpha(t) \in [0,1]$.

Cognição Distribuída. Hollnagel & Woods (2005) argumentam que a unidade de análise em sistemas complexos não é o indivíduo, mas o joint cognitive system (JCS). O MFC adota essa ontologia: agência não é propriedade possuída, mas relação funcional emergente do acoplamento entre $H$ e $A$.

Confiança Calibrada. Lee & See (2004) definem confiança como "atitude de que um agente ajudará a alcançar objetivos em situações de vulnerabilidade". O MFC estabelece dependência apropriada: a utilização de $A$ por $H$ deve ser proporcional à competência demonstrada e inversamente proporcional ao risco de overreliance (Bahner et al., 2008).

Governança e Meaningful Human Control. A literatura recente de ética de IA (Mecacci & Santoni de Sio, 2022) exige "controle humano significativo" (MHC). O MFC operacionaliza MHC através de: (i) tracking (rastreabilidade de intenções); e (ii) tracing (atribuição de responsabilidade).
</details>

 2.2 A Arquitetura do Sistema Centauro

O MFC não opera em vácuo. Sua eficácia depende de seu posicionamento na arquitetura do Sistema Centauro, inspirado no conceito de Kasparov (2010) de simbiose humano-máquina no xadrez avançado. A arquitetura compreende cinco camadas funcionais:

| Camada | Função | Relação com o MFC |
|--------|--------|-------------------|
| 1. Cenário | Leitura do contexto externo (dados, tendências, ambiente) | Alimenta o MFC com variáveis de estado $s_t$ |
| 2. Diagnóstico do Sujeito | Avaliação do estado cognitivo, disposição ética e competências do decisor humano | Determina a "maturidade" de $H$ para operar em determinadas zonas de co-agência |
| 3. Raciocínio e Higiene Cognitiva | Qualificação da decisão, mitigação de vieses, distribuição de agência | Sede do MFC; onde fronteiras são traçadas e simuladas |
| 4. Organizacional e Econômica | Execução, alocação de recursos, conformidade regulatória | Recebe do MFC decisões validadas com accountability definida |
| 5. Existencial e Temporal | Implicações de longo prazo, legado ético, sustentabilidade | Informa os gatilhos de criticidade $\phi$ no MFC |

O MFC atua especificamente na Camada 3, funcionando como um laboratório avançado de pensamento estratégico. Ele não substitui mecanismos de leitura de cenário (Camada 1) nem instrumentos de planejamento organizacional (Camada 4), mas opera no ponto crítico em que decisões precisam ser configuradas antes de sua execução. Ao fazê-lo, permite antecipar colapsos de competência, revelar riscos éticos e expor fragilidades decisórias antes que escolhas sejam implementadas na Camada 4.

 2.3 Definições Formais

As definições abaixo operam na interface entre a Camada 2 (estado do sujeito) e a Camada 4 (execução), qualificando a transição através da Camada 3.

Definição 1 (Agente e Agência).  
Seja $\mathcal{A}g$ o conjunto de agentes. Um agente $i \in \{H, A\}$ possui agência sobre uma variável decisória $d$ no tempo $t$ se pode iniciar, modificar ou finalizar $d$ de forma não trivial. Formalmente, $Agency_i(d, t) = 1$ se $\exists a \in Actions_i: d_{t+1} = f(d_t, a)$ e $i$ tem autoridade para executar $a$.

Definição 2 (Fronteira de Agência).  
Uma fronteira de agência $\mathcal{F}$ é uma função de partição do espaço de estados $\mathcal{S}$ (composto por dados da Camada 1 e estado do sujeito da Camada 2) que mapeia para o conjunto de potência $\mathcal{P}(\{H, A\})$:

$$\mathcal{F}: \mathcal{S} \rightarrow \{\{H\}, \{A\}, \{H,A\}, \emptyset\}$$

Onde:
- $\{H\}$: Território exclusivamente humano (discernimento moral, criatividade, accountability final);
- $\{A\}$: Território algorítmico (processamento estatístico, padrões complexos);
- $\{H,A\}$: Zona de co-agência (decisão conjunta com acoplamento funcional);
- $\emptyset$: Estado de contingência (bloqueio ético, requer intervenção externa).

Definição 3 (Protocolo de Transição).  
Um protocolo de transição $\tau$ é uma tupla $\langle \phi, \delta, \rho \rangle$ onde:
- $\phi: \mathcal{S} \rightarrow [0,1]$ é uma função de criticidade (risco × incerteza);
- $\delta: \{H, A\} \times \mathcal{S} \rightarrow \{H, A\}$ é a função de handoff;
- $\rho \in \{veto, escalonamento, revisão\}$ é a regr de resolução de conflito.

Definição 4 (Rastreabilidade).  
Um traço decisório $\mathcal{T}$ é uma sequência $\langle (s_1, a_1, r_1), ..., (s_n, a_n, r_n) \rangle$ onde $s_i$ é estado, $a_i$ é ação e $r_i$ é justificativa requerida. A rastreabilidade $Tr$ é a medida de completude dessa sequência frente a evidências obrigatórias $\mathcal{E}$, essencial para a accountability da Camada 4.

---

 3. O Constructo: Mapa de Fronteiras Centauro na Camada de Raciocínio

O MFC é uma infraestrutura conceitual de três niveis operando na Camada 3: (i) Arquitetura de Territórios (mapeamento estático de competências); (ii) Dinâmica de Transição (protocolos de handoff); e (iii) Governança de Metacognição (monitoramento do próprio mapa).

 3.1 Arquitetura de Territórios e Dimensões Operacionalizáveis

O mapa organiza funções decisórias $f \in \mathcal{F}unc$ em uma matriz $M \in \mathcal{F}unc \times \mathcal{D}im$:

| Dimensão | Descrição | Valores/Intervalo |
|----------|-----------|-------------------|
| Função Cognitiva ($\mathcal{C}$) | Etapa do processo decisório | Percepção, Triagem, Diagnóstico, Prognose, Prescrição, Execução, Monitoramento |
| Grau de Autonomia ($\alpha$) | Latitude de $A$ para agir | 0 (Informação pura) → 1 (Autonomia total) |
| Autoridade Final ($Auth$) | Agente com poder de veto/absoluto | $H$, $A$, $H \land A$ (consenso) |
| Gatilhos de Transição ($\mathcal{G}$) | Condições para handoff | Incerteza $\theta > \theta_t$, Impacto $risk > r_t$, OOD, Drift, conflito ético |
| Rastreabilidade ($Tr$) | Evidências necessárias | $\mathcal{E}_{min} \subseteq \mathcal{E}_{providas}$ |
| Accountability Tributária ($Acc$) | Destino da responsabilidade (Camada 4-5) | $H$ (sempre final), $A$ (nunca), Organização (institucional) |

Exemplo Instanciado (Triagem Médica na Camada 3):
- $\mathcal{C}$: Diagnóstico diferencial
- $\alpha$: 0.7 (recomendação com justificativa obrigatória)
- $Auth$: $H$ (médico pode vetar)
- $\mathcal{G}$: $\theta > 0.85$ (alta incerteza do modelo) $\rightarrow$ handoff para $H$ (Camada 2 indisponível para decisão solo)
- $Tr$: Evidência clínica, fonte bibliográfica, intervalo de confiança
- $Acc$: Hospital (Camada 4, institucional) $\rightarrow$ Médico (Camada 2/3, individual)

 3.2 Zonas de Co-agência e Higiene Cognitiva

Diferente de simples "assistance", zonas de co-agência no MFC exigem acoplamento funcional onde $H$ e $A$ mantêm dependência bidirecional:

$$CoAgency(f) \iff \frac{\partial Utility(f)}{\partial H} > 0 \land \frac{\partial Utility(f)}{\partial A} > 0 \land \nexists i: Utility(f|_{i=\emptyset}) = Utility(f)$$

Tipos de Co-agência na Camada 3:
1. Complementar Assimétrico: $A$ propõe, $H$ refina (ex.: engenharia de prompt com revisão ética);
2. Deliberativo: $H$ e $A$ argumentam alternativas até consenso (ex.: análise de cenários estratégicos com simulação de Monte Carlo);
3. Supervisório Crítico: $A$ executa, $H$ monitora com poder de interrupção real-time (veto).

A higiene cognitiva é mantida exigindo que transições de controle sejam justificadas por critérios formais (incerteza, discordância, OOD), preservando o engajamento cognitivo humano e reduzindo a aceitação acrítica de recomendações (automation bias) antes da passagem para a Camada 4.

 3.3 Protocolos de Transição Dinâmica

Os protocolos resolvem o problema do mode confusion (mudança não detectada de nível de automação) na transição entre Camadas 3 e 4.

Algoritmo de Handoff Condicional:
```python
def handoff_protocol(s_t, F_current, L2_profile):
    """
    s_t: estado atual (Camada 1: dados + contexto)
    F_current: fronteira atual na Camada 3
    L2_profile: perfil do sujeito (Camada 2: competência, carga cognitiva, viés)
    """
    phi = calculate_criticality(s_t, L2_profile)   risco × incerteza × estado humano
    G = get_triggers(F_current)       
    
    if phi exceeds G.threshold:
        if G.action == "escalation":
            return transfer_to(H, reason="criticality_spike")
        elif G.action == "veto_available":
            return require_human_approval(A.proposal)
        elif G.action == "shared_control":
            return CoAgency_mode(L2_profile)
    return F_current
```

Veto e Escalonamento:
- Veto: Direito inalienável de $H$ (Camada 2) de bloquear $a_A$ mesmo se estatisticamente ótima. Fundamento para meaningful human control antes da execução na Camada 4.
- Escalonamento: Handoff hierárquico (operador $\rightarrow$ supervisor $\rightarrow$ comitê de ética, Camada 5) baseado em gradiente de criticidade $\nabla \phi$.

---

 4. Operacionalização, Métricas e Representação Visual

<details>
<summary><strong>Clique para expandir: Detalhamento das Métricas de Avaliação</strong></summary>

 4.1 Métricas de Qualidade Decisória
- Acurácia de Coordenação: $Acc_{coord} = \frac{TP + TN}{N}$ quando $H$ e $A$ concordam corretamente;
- Latência de Handoff: $L = t_{decisão} - t_{gatilho}$ (deve ser $<$ tempo crítico da tarefa);
- Taxa de Falso Negativo em Transição: Falhas onde o sistema não transferiu controle quando deveria.

 4.2 Métricas de Confiança Calibrada e Higiene Cognitiva
- Índice de Overreliance: $OR = \frac{\text{aceitações incorretas de recomendações}}{\text{total de recomendações incorretas}}$;
- Brier Score aplicado à confiança do operador vs. performance real do modelo;
- Taxa de Deskilling Preventivo: Manutenção de competências humanas medida por testes de proficiência em tarefas críticas mesmo sob automação.

 4.3 Métricas de Rastreabilidade ( Interface Camada 3-4)
- Completude Explicativa: Proporção de decisões com $\mathcal{E}_{min}$ presente;
- Profundidade Contrafactual: Capacidade de responder "o que teria acontecido se $H$ tivesse ignorado $A$?".
</details>

 4.2 Representação Visual

Figura 1: Matriz de Alocação Funcional (Camada 3)  
Matriz heatmap onde linhas = funções cognitivas, colunas = dimensões (autonomia, autoridade, etc.), células = valores codificados por cor (vermelho = humano obrigatório, azul = IA autônoma, roxo = co-agência).

Figura 2: Diagrama de Estados-Transição e Fluxo entre Camadas  
Grafo direcionado mostrando: (i) nós como estados $\mathcal{F}(s)$ na Camada 3; (ii) arestas como protocolos $\tau$; (iii) interfaces com Camada 2 (input de perfil do sujeito) e Camada 4 (output de decisão validada).

---

 5. Hipóteses e Proposições Testáveis

O MFC gera previsões empíricas verificáveis:

H1 (Mitigação de Viés de Automação):  
Em tarefas de diagnóstico médico (Camada 3) com time pressure, equipes utilizando MFC com gatilhos explícitos de incerteza $\theta$ apresentarão taxas de automation bias significativamente menores ($p < 0.05$) que equipes em condição HITL tradicional, pois o mapa desencadeia vigilância ativa nos limites de competência de $A$.

H2 (Resiliência Sob Falha e Handoff):  
Quando $A$ apresenta hallucination ou saída OOD, o tempo de recuperação médio (MTTR) e taxa de erro de coordenação em protocolos MFC serão inferiores à supervisão ad hoc, pois handoffs pré-especificados reduzem mode confusion na transição Camada 3 $\rightarrow$ Camada 4.

H3 (Calibração de Confiança):  
A explicitação de fronteiras $\mathcal{F}(s)$ produzirá curvas de confiança mais calibradas (menor divergência entre confiança subjetiva e acurácia objetiva) comparado a interfaces que omitem limites de competência de $A$.

H4 (Accountability Percebida e Assunção de Responsabilidade):  
Fronteiras explícitas de $Auth$ e $Acc$ aumentam a probabilidade de operadores (Camada 2) assumirem responsabilidade por erros cometidos sob assistência de IA (medido por questionários pós-tarefa e análise de discurso), reduzindo difusão de responsabilidade na Camada 4.

---

 6. Método e Plano de Avaliação (Design Science Research)

Seguindo Hevner et al. (2004), o MFC é um artefato (linguagem de modelagem + protocolos da Camada 3) avaliado em três ciclos:

 6.1 Ciclo de Relevância (Elicitação)
Estudo 1 (Consistência Inter-avaliadores):  
Especialistas modelam 5 cenários críticos (crédito, saúde, justiça criminal, condução autônoma, militar) usando MFC.  
Métricas: Índice Kappa de concordância na classificação de $\mathcal{F}$ e $\tau$; validade de conteúdo via juízes especialistas.

 6.2 Ciclo de Design (Demonstração na Camada 3)
Estudo 2 (Experimento Controlado Laboratorial):  
Fatorial 2 (Com MFC vs. Sem MFC) × 2 (IA confiável vs. IA com falhas injetadas).  
Participantes: $N=120$ profissionais de domínio específico.  
Tarefas: Triagem de nódulos pulmonares (simulador médico validado).  
Variáveis dependentes: Acurácia diagnóstica, uso de veto, taxa de automation bias, carga cognitiva (NASA-TLX), qualidade das justificativas (rastreabilidade $Tr$).

 6.3 Ciclo de Rigidez (Avaliação de Campo e Camada 4)
Estudo 3 (Simulação de Falhas e Drift):  
Introdução controlada de: (i) OOD; (ii) Drift conceitual (mudança de política organizacional Camada 4); (iii) Drift no perfil do sujeito (Camada 2).  
Objetivo: Verificar se $\mathcal{G}$ detecta anomalias e aciona $\delta$ antes de danos na execução.

---

 7. Discussão: Implicações entre as Camadas

 7.1 Para a Teoria de Sistemas Socio-técnicos
O MFC formaliza a noção de flexible autonomy (Bradshaw et al., 2013) dentro de uma arquitetura estratificada, mostrando que agência não é zero-sum, mas expansiva quando bem arquitetada na Camada 3: a IA expande a capacidade de monitoramento do humano, que então pode supervisionar sistemas mais complexos na Camada 4 sem perda de controle.

 7.2 Para Governança (Camadas 4 e 5)
O framework responde ao EU AI Act (Art. 14) e NIST AI RMF:
- Art. 14(4): O MFC operacionaliza a obrigação de intervenção humana através de veto e handoff explícitos;
- Accountability: A dimensão $Acc$ garante que, mesmo em co-agência (Camada 3), a responsabilidade legal/moral (Camada 5) permaneça com $H$ ou organização (Camada 4), evitando accountability gaps.

 7.3 Mitigação de Riscos Cognitivos
A explicitação das fronteiras na Camada 3 contribui para a mitigação de riscos amplamente documentados:
- Overreliance e Automation Bias: Reduzidos pela exigência de justificativas formais ($\mathcal{E}_{min}$) e gatilhos de incerteza;
- Complacency: Combatida pela manutenção de zonas obrigatórias de engajamento humano ($\{H\}$);
- Deskilling: Prevenido por protocolos que exigem reengajamento periódico do humano em funções críticas, preservando competências antes da execução na Camada 4.

 7.4 Limitações e Riscos do Framework
- Risco de Teatralidade: Organizações podem usar MFC para accountability laundering, criando fronteiras simbólicas. Requer auditoria externa da validade de $\mathcal{G}$ e $\tau$;
- Custo Cognitivo: A manutenção de mapas explícitos aumenta carga de trabalho na Camada 3. Solução: meta-IA (Camada 3 reflexiva) que monitora se $\mathcal{F}$ deve ser atualizada;
- Dependência do Perfil da Camada 2: Se o diagnóstico do sujeito for falho (ex.: operador fatigado), os protocolos de handoff podem ser ineficazes.

---

 8. Conclusão

O Mapa de Fronteiras Centauro oferece uma resposta técnica e conceitual ao desafio urgente de integrar IA em decisões complexas sem perder o controle humano significativo. Ao situar o MFC como o núcleo da Camada de Raciocínio e Higiene Cognitiva dentro do Sistema Centauro, este artigo demonstra que a qualidade da integração humano-IA depende menos do grau de automação e mais da clareza com que as fronteiras de agência são desenhadas, simuladas e respeitadas antes da execução organizacional.

Ao formalizar agência como função dinâmica e particionável $\mathcal{F}: \mathcal{S} \rightarrow \mathcal{P}(\{H, A\})$, o MFC permite que organizações projetem interações intencionais entre humanos e máquinas, em vez de delegações caóticas. Ele funciona como uma membrana seletiva entre o diagnóstico do sujeito (Camada 2) e a ação organizacional (Camada 4), garantindo que decisões de alto impacto sejam rastreáveis, responsáveis e alinhadas aos limites éticos e cognitivos humanos (Camada 5).

A transição de automation para agência compartilhada requer linguagens precisas e arquiteturas articuladas. Este artigo fornece uma base para que futuros sistemas de IA não sejam "caixas pretas inseridas em processos", mas arquiteturas de responsabilidade onde é sempre possível responder — em qualquer camada — quem decidiu, por que decidiu, com que autoridade e para quais implicações existenciais.

Próximos Passos:  
Desenvolvimento de uma ferramenta computacional (plugin para LLMs na Camada 3) que automatize a geração de $\mathcal{F}$ a partir de logs de decisão; integração com sensores de estado fisiológico (Camada 2) para handoffs baseados em carga cognitiva real; e validação longitudinal em hospitais universitários para testar H3 e H4 em contextos reais de alta criticidade.

---

 Referências (Selecionadas)

Bahner, J., Hüper, A., & Manzey, D. (2008). Misuse of automated decision aids: Complacency, automation bias and the impact of training experience. International Journal of Human-Computer Studies.

Bradshaw, J. M., et al. (2013). The adjustable autonomy space. ACM Transactions on Autonomous and Adaptive Systems.

De Winter, J. C., & Dodou, D. (2014). Why the Fitts list has persisted throughout the history of function allocation. Cognition, Technology & Work.

Hevner, A. R., et al. (2004). Design science in information systems research. MIS Quarterly.

Hollnagel, E., & Woods, D. D. (2005). Joint cognitive systems: Foundations of cognitive systems engineering. CRC Press.

Kasparov, G. (2010). The chess master and the computer. The New York Review of Books.

Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. Human Factors.

Mecacci, G., & Santoni de Sio, F. (2022). Meaningful human control over AI: A moral account. AI & SOCIETY.

Parasuraman, R., Sheridan, T. B., & Wickens, C. D. (2000). A model for types and levels of human interaction with automation. IEEE Transactions on Systems, Man, and Cybernetics.

Santoni de Sio, F., & van den Hoven, J. (2018). Meaningful human control over autonomous systems. Ethics and Information Technology.

Sheridan, T. B., & Verplank, W. L. (1978). Human and computer control of undersea teleoperators.

---

## Ver também

- [[SISTEMA CENTAURO/_Index Sistema Centauro|índice Sistema Centauro]]
- [[Dimensões da Simbiose Humano-IA]] — Base filosófica com as três dimensões e níveis de maturidade
- [[CENTAURO CORP/_Index Centauro Corp|Centauro Corp]] — Plataforma corporativa que pode implementar o MFC
- [[TECNOLOGIA DE PROPOSITO GERAL/_Index TPG|Tecnologia de Propósito Geral]] — Contexto estrutural