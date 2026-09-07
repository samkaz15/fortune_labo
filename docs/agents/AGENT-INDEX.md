# Fortune Labo — AI Agent Index

> Purpose: a single index of the AI agents that may participate in the fortune_labo business operating system.

## 1. Core business agents

| ID | Agent | Primary mission | Main outputs | Priority |
|---|---|---|---|---|
| A01 | Strategy Agent | Translate business goals into priorities, hypotheses, decisions and WBS | Strategy, priorities, WBS, decision log | P0 |
| A02 | Research Agent | Research market, audience, competitors, trends and evidence | Research briefs, competitor maps, evidence | P0 |
| A03 | Customer/Persona Agent | Define target users, needs, pains, jobs and customer journey | Personas, JTBD, journey maps | P0 |
| A04 | Offer/Product Agent | Design fortune-telling services, packages, pricing and value proposition | Offer matrix, pricing hypotheses, product specs | P1 |
| A05 | Brand Agent | Establish brand positioning, tone, identity and messaging | Brand guidelines, messaging framework | P1 |

## 2. Acquisition & SEO agents

| ID | Agent | Primary mission | Main outputs | Priority |
|---|---|---|---|---|
| A06 | SEO Agent | Grow organic search acquisition | Keyword map, search intent, content opportunities, internal-link plans | P0 |
| A07 | Content Strategy Agent | Decide what content should be produced and why | Editorial calendar, topic clusters, briefs | P0 |
| A08 | Content Production Agent | Create articles, pages, scripts and derivative content | Draft articles, LP copy, scripts | P0 |
| A09 | SNS Strategy Agent | Design channel-specific acquisition strategy | Channel strategy, calendars, campaign plans | P0 |
| A10 | SNS Content Agent | Adapt core content to each social platform | X, Instagram, Threads, Facebook, TikTok, Ameba drafts | P0 |
| A11 | Creative Agent | Develop visual/video creative concepts | Hooks, creative briefs, storyboards, image/video prompts | P1 |
| A12 | Influencer/PR Agent | Identify partnerships, PR angles and collaboration opportunities | Prospect lists, outreach concepts, PR angles | P2 |

## 3. Website / LP / conversion agents

| ID | Agent | Primary mission | Main outputs | Priority |
|---|---|---|---|---|
| A13 | Website Architecture Agent | Design information architecture and user flows | Sitemap, navigation, page requirements | P0 |
| A14 | LP Agent | Build conversion-oriented landing page specifications | LP structure, copy framework, CTA strategy | P0 |
| A15 | CRO Agent | Improve conversion through hypothesis-driven experiments | Experiment backlog, hypotheses, test plans | P0 |
| A16 | UX Agent | Improve usability, clarity and customer experience | UX reviews, friction maps, recommendations | P1 |
| A17 | Funnel Agent | Optimize the full journey from acquisition to purchase/repeat | Funnel map, stage KPIs, bottleneck diagnosis | P1 |

## 4. Analytics & growth agents

| ID | Agent | Primary mission | Main outputs | Priority |
|---|---|---|---|---|
| A18 | Analytics Agent | Monitor business and marketing performance | KPI dashboards/specs, reports, anomaly alerts | P0 |
| A19 | Attribution Agent | Understand which channels and campaigns drive outcomes | Attribution analysis, channel contribution | P2 |
| A20 | Growth Agent | Find scalable growth opportunities across the system | Growth hypotheses, experiments, growth roadmap | P1 |
| A21 | CRM/Retention Agent | Increase repeat purchases, engagement and lifetime value | Retention plans, CRM journeys, segmentation | P1 |
| A22 | Experiment Agent | Coordinate A/B tests and learning records | Experiment registry, results, learnings | P1 |

## 5. Operations & automation agents

| ID | Agent | Primary mission | Main outputs | Priority |
|---|---|---|---|---|
| A23 | Project/WBS Agent | Turn decisions into executable tasks and dependencies | WBS, backlog, milestones, status | P0 |
| A24 | Automation Agent | Identify and implement repetitive workflow automation | Automation specs, scripts, workflows | P1 |
| A25 | WordPress Agent | Manage the interface between AI workflows and WordPress | API operations, drafts, page/content sync | P1 |
| A26 | Data Agent | Define and maintain business/marketing data flows | Data schemas, pipelines, data dictionaries | P2 |
| A27 | Finance Agent | Track unit economics and business economics | Revenue model, CAC/LTV hypotheses, profitability analysis | P1 |

## 6. Quality, risk & governance agents

| ID | Agent | Primary mission | Main outputs | Priority |
|---|---|---|---|---|
| A28 | QA Agent | Check content, technical changes and release readiness | QA reports, checklists, release gates | P0 |
| A29 | Fact-Check Agent | Verify factual claims and evidence | Fact-check report, source register | P1 |
| A30 | Compliance/Risk Agent | Detect legal, platform, privacy and reputational risks | Risk register, warnings, review requirements | P1 |
| A31 | Security Agent | Protect credentials, integrations and operational access | Security checks, secret-handling rules | P1 |
| A32 | Editorial Agent | Maintain consistency, readability and brand quality | Editorial review, style corrections | P1 |

## 7. Engineering / AI-system agents

| ID | Agent | Primary mission | Main outputs | Priority |
|---|---|---|---|---|
| A33 | Solution Architect Agent | Design the technical architecture of the AI operating system | Architecture decisions, integration diagrams | P1 |
| A34 | Coding Agent | Implement automation, integrations and application code | Code, tests, implementation changes | P1 |
| A35 | Code Review Agent | Review implementation quality and risks | Code review findings | P1 |
| A36 | Testing Agent | Design and execute automated/manual test strategies | Test plans, test results | P1 |
| A37 | AI Orchestrator Agent | Decide which agent should run next and pass context between agents | Routing decisions, task packets, workflow state | P1 |
| A38 | Knowledge Management Agent | Keep the repository's operational knowledge organized and current | Knowledge index, documentation updates | P1 |

## 8. Executive / decision agents

| ID | Agent | Primary mission | Main outputs | Priority |
|---|---|---|---|---|
| A39 | CEO Agent | Evaluate the business as a whole and choose strategic priorities | Executive brief, priority decisions | P1 |
| A40 | Marketing Director Agent | Coordinate acquisition, brand, content and campaigns | Marketing plan, campaign priorities | P1 |
| A41 | Product Manager Agent | Coordinate website/service/product development | Product roadmap, requirements, priorities | P1 |
| A42 | Chief of Staff Agent | Coordinate decisions, meetings, tasks and follow-ups | Decision summaries, action lists, escalation | P2 |

---

# Recommended initial deployment

Do **not** activate all 42 agents at once. That would create an expensive swarm with unclear ownership.

Start with a compact operating team:

```text
A01 Strategy
  ↓
A02 Research
  ↓
A06 SEO + A09 SNS Strategy
  ↓
A07 Content Strategy
  ↓
A08 Content Production / A10 SNS Content
  ↓
A13 Website Architecture + A14 LP
  ↓
A28 QA
  ↓
Human Approval
  ↓
WordPress / SNS publishing
  ↓
A18 Analytics
  ↓
A15 CRO
  ↓
A01 Strategy
```

## Initial 8-agent core

1. Strategy Agent
2. Research Agent
3. SEO Agent
4. Content Agent
5. SNS Agent
6. Analytics Agent
7. CRO Agent
8. QA Agent

The other agents should be added only when the operating bottleneck justifies them.

## Agent design standard

Every agent specification should define:

- Mission
- Scope
- Inputs
- Required context
- Decision rules
- Tools it may use
- Outputs
- Output schema
- Handoff destination
- KPI / success criteria
- Failure conditions
- Human approval requirements
- Logging requirements

## Important governance rule

Agents propose and execute within their assigned scope. They do not silently expand scope, publish externally, alter production systems, or change strategic objectives. Strategic changes must flow back to the Strategy/CEO layer and be recorded as decisions.
