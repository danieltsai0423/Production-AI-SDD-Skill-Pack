# Production AI SDD Skill Pack

> **Master Implementation Specification／主實作規格書**  
> 文件版本：v1.0  
> 文件日期：2026-07-01  
> 主要讀者：Codex、Claude Code、AI Coding Agent、Skill Pack 維護者、AI 系統架構師  
> 文件用途：搭配《AI 系統與自動化專案開發 SOP》及既有專案資料，建立一套可跨專案、跨產業、跨 Agent 工具使用的 Production AI SDD Skill Pack。

---

## 0. 給實作 Agent 的最高優先指令

你正在建置一套名為 **Production AI SDD Skill Pack** 的可重複使用工程資產。請把本文件視為產品規格與驗收契約，並把使用者另外提供的完整 SOP、既有專案文件、事故紀錄、架構圖、程式碼與測試，視為領域知識來源。

你的任務不是把 SOP 原文複製成一個超長 Prompt，也不是把特定醫美、Facebook Messenger、LINE、n8n、FastAPI 或 Redis 技術寫死。你的任務是：

1. 從真實專案經驗中抽取可泛化的工程模式、失敗模式、決策原則與驗證流程。
2. 將它們轉換為符合 Agent Skills 開放格式的多個聚焦 Skill。
3. 以 Spec-Driven Development 為主要生命週期，串接需求、架構、任務、實作、測試、AI Evals、上線與事故復盤。
4. 同時支援 Codex 與 Claude Code，避免維護兩套互相漂移的核心內容。
5. 將「建議性規則」放入 Skills 或 instructions，將「必須確定執行」的規則放入 deterministic scripts、CI 或 Hooks。
6. 建立可以測試 Skill 觸發、輸出品質、流程遵循度及安全性的評估系統。
7. 讓整套 Skill Pack 適用於任何 AI 系統架構／AI 應用專案，而非只適用於客服或醫療場景。

### 0.1 實作 Agent 必須遵守

- 先盤點輸入文件與現有 repository，再產出 implementation plan。
- 不得因本文件內容完整而跳過 repository discovery。
- 不得聲稱某項能力已完成，除非有可重現的驗證證據。
- 不得把使用者過去做過的單一技術選擇當成全域唯一標準。
- 不得把「AI 自動完成」等同於「可以無人監督地執行高風險操作」。
- 不得只建立 Markdown；至少要有可執行的 validator、installer、eval runner 或 quality gate。
- 不得讓單一 `SKILL.md` 承擔整個軟體生命週期。
- 不得讓所有小修改都被迫走完整且沉重的 SDD 流程。
- 所有 Skill name、directory name、frontmatter 與 file reference 必須符合 Agent Skills 規格。
- 核心 Skill instruction 優先使用英文，以提高跨工具與跨模型一致性；README、使用手冊與範例應提供繁體中文，並可選擇提供英文版本。

### 0.2 實作 Agent 最終必須交付

- 可安裝、可驗證、可執行的完整 repository。
- `.agents/skills/` 與 `.claude/skills/` 的共用或同步機制。
- `AGENTS.md` 與 `CLAUDE.md`。
- 核心 Skills、references、assets、scripts。
- Claude Code 與 Codex 的 Hooks／設定範例。
- SDD 規格模板、變更模板、驗證模板與事故模板。
- Skill trigger evals、output quality evals、workflow compliance evals。
- 最少一個通用範例專案與三個不同 AI 專案類型的 fixture。
- CI workflow、lint、schema validation、unit tests。
- 安裝、更新、解除安裝、版本升級與故障排除文件。
- Release checklist 與驗收報告。

---

# 1. 執行摘要

Production AI SDD Skill Pack 是一套針對 AI 系統架構與應用開發的 **Spec-Anchored、Evidence-Driven、Safety-Aware** 工程工作流。

它應將以下能力統一成可重複執行的流程：

- 需求探索與規格化
- 模糊需求釐清
- AI 系統架構規劃
- 資料、模型、Prompt、RAG、工具與 Agent 契約設計
- 功能拆解與任務依賴管理
- TDD／BDD／Contract Test
- AI Evaluation 與 Regression Test
- Reliability、Security、Privacy、Human-in-the-loop 審查
- 上線、監控、成本、回滾與事故復盤
- Brownfield 既有專案的需求變更與 Spec Drift 管理

這套系統不把規格視為一次性文件，也不把程式碼視為唯一真相。它採用以下關係：

```text
Specification = 意圖、邊界、契約與驗收標準
Code          = 實際系統行為
Tests / Evals = Spec 與 Code 一致性的證據
Runtime       = 正式環境是否真正可靠的證據
Observability = 問題是否可發現、可追蹤、可復原的證據
```

---

# 2. 背景與知識來源

本 Skill Pack 的初始知識來源來自實際 AI 系統與自動化專案中反覆出現的問題，包括但不限於：

- Webhook 必須快速 acknowledge，但 AI 推理可能較慢。
- 外部平台可能重送事件，造成重複執行或重複回覆。
- 同一使用者的多則訊息可能並行處理，導致順序、狀態或資料競爭問題。
- 真人與 AI 可能同時操作同一對話或工作項目。
- LLM、RAG、第三方 API、Queue、Database 與 Workflow Orchestrator 都可能部分失敗。
- AI 產生內容不等於內容正確，尤其在醫療、法律、財務、個資與品牌風險場景。
- 需求通常從「做一個 AI」開始，但真正需要定義的是使用者、流程、資料、權限、KPI 與人工責任。
- n8n／低代碼工作流仍需要版本、測試、錯誤處理、可觀測性與部署規範。
- Agent 能呼叫工具後，風險從「回答錯誤」提升為「執行錯誤」。
- Prompt、模型、知識庫與程式碼會獨立變更，容易產生隱性 drift。
- 只修當下 bug 而不補測試、監控或防呆，問題會再次發生。

這些經驗必須被抽象為跨產業能力，而不是變成特定專案硬編碼。

---

# 3. 產品願景

## 3.1 願景

讓 Codex、Claude Code 與其他支援 Agent Skills 的工具，能像一個具備生產環境經驗的 AI 系統工程團隊般工作：

- 先理解目標與風險，再設計系統。
- 先建立可驗收的規格，再開始大幅修改程式碼。
- 將 AI 特有的不確定性轉換為可測試的契約與 Evals。
- 讓每次變更都能追蹤到需求、設計、任務、程式碼與證據。
- 在必要時保留人工決策權、回滾能力與營運備援。

## 3.2 主要使用者

- 個人 AI 工程師
- AI Automation Engineer
- AI Application Engineer
- Backend／Full-stack Engineer 開發 AI 功能
- Agent／RAG／LLM Platform Engineer
- 顧問與接案者
- 新創與中小型產品團隊
- 需要將 AI PoC 推進正式環境的團隊
- 使用 Claude Code、Codex 或其他 Agent Skills 相容工具的開發者

## 3.3 主要使用情境

- 從零建立新的 AI 應用
- 在既有產品加入 LLM、RAG 或 Agent
- 建立 LINE、Messenger、Slack、Email、Voice 等互動系統
- 建立 AI 內容、SEO、影片、文件或資料處理管線
- 建立具工具使用能力的 Agent
- 建立內部 AI 助理或營運系統
- 建立多租戶 AI SaaS
- 修復 AI 系統的可靠性問題
- 進行模型、Prompt、向量庫或工作流替換
- 處理需求變更、架構重構或事故復盤

---

# 4. 範圍與非目標

## 4.1 第一版範圍

第一版必須涵蓋：

1. SDD 任務分級與流程路由。
2. Greenfield 與 Brownfield 專案。
3. AI 系統規格模板。
4. AI Architecture Review。
5. Model／Prompt／RAG／Tool／Data Contracts。
6. Reliability、Security、Privacy、Human Oversight。
7. Tests、AI Evals、Release Gate。
8. Change Proposal、Spec Delta、Archive。
9. Incident Response 與 Postmortem。
10. Codex／Claude Code 安裝與共用。
11. Hooks、validators、eval runners。
12. 可擴充的 project profiles。

## 4.2 非目標

第一版不應：

- 成為完整專案管理 SaaS。
- 強迫使用特定雲端、模型、向量資料庫或框架。
- 取代 Git、CI、Issue Tracker 或 Observability Platform。
- 自動取得或儲存正式環境密碼。
- 自動批准高風險資料修改、付款、退款、醫療判斷或法律決策。
- 為每種程式語言內建所有 lint／test 工具。
- 將所有專案規格自動生成為 100% 完整且不可修改的文件。
- 宣稱只要套用 Skill Pack 就能自動符合所有法律與產業規範。

---

# 5. 核心方法論

## 5.1 採用 Spec-Anchored Development

本專案採用 **Spec-Anchored**，而非最極端的 Spec-as-Source。

- Spec 定義 intent、contracts、constraints、acceptance criteria。
- Code 定義實際行為。
- Tests 與 Evals 建立可重現的一致性證據。
- Runtime metrics 建立生產環境證據。
- 變更時 Spec 與 Code 必須共同演進。

## 5.2 採用風險分級，而非一刀切

### Level 0：Direct Change

適用：

- 拼字、格式、註解
- 明確的小型設定
- 不改變 observable behavior 的重構

必要產物：

- Diff
- Targeted validation
- Completion note

### Level 1：Light Spec

適用：

- 小型功能
- 單模組修改
- 低資料風險
- 可在短週期完成

必要產物：

- `spec.md`
- `tasks.md`
- `verification.md`

### Level 2：Full Spec

適用：

- 跨模組功能
- 新 API、Database、Queue、External Integration
- 影響多位使用者或營運流程
- 需要架構取捨

必要產物：

- `brief.md`
- `spec.md`
- `clarifications.md`
- `plan.md`
- `contracts/`
- `tasks.md`
- `verification.md`

### Level 3：High-Risk AI Spec

適用：

- AI 對外直接溝通
- AI 執行可造成實際影響的工具
- 個資、敏感資料、醫療、法律、財務、未成年人
- 支付、退款、資料刪除、預約、權限異動
- 高併發或關鍵營運服務

額外必要產物：

- `risk-assessment.md`
- `ai-behavior-contract.md`
- `human-oversight.md`
- `security-privacy.md`
- `evals.md`
- `observability.md`
- `rollback.md`
- `operational-runbook.md`

## 5.3 Evidence Before Completion

Agent 不得只用「測試看起來通過」或「程式碼已完成」作為完成聲明。

完成證據可能包括：

- Unit tests
- Integration tests
- Contract tests
- E2E tests
- AI eval results
- App／service 實際啟動
- API sample request and response
- Migration dry-run
- Observability check
- Security scan
- Spec compliance report
- Manual approval record

## 5.4 Progressive Disclosure

- 每個 Skill 聚焦一個 coherent job。
- `SKILL.md` 只放所有執行都需要的核心程序。
- 長篇標準放 `references/`。
- 長版模板放 `assets/`。
- 可確定執行的邏輯放 `scripts/`。
- Skill 必須明確告訴 Agent 何時讀取哪一份 reference。

## 5.5 Safety and Human Authority

- 高風險操作預設為「AI 建議，人工決定」。
- Human takeover／approval 不是 UI 功能，而是系統契約。
- Agent 工具權限應採最小權限。
- 讀取、建議、草稿、執行、發布應分成不同能力層級。
- 不可把 hallucination 只當成 Prompt 問題；必須處理資料、檢索、權限、驗證與 fallback。

---

# 6. 設計依據與相容性原則

## 6.1 Agent Skills 開放格式

每個 Skill 應至少包含：

```text
skill-name/
├── SKILL.md
├── scripts/       # optional
├── references/    # optional
├── assets/        # optional
└── agents/        # optional, tool-specific metadata
```

`SKILL.md` 必須具備 YAML frontmatter：

```yaml
---
name: pai-sdd-discovery
description: Classifies AI software work by risk and complexity, inspects repository context, and selects the minimum sufficient SDD workflow. Use before implementing new AI features, cross-module changes, architecture changes, risky automation, or unclear requirements. Do not use for trivial formatting-only edits.
license: MIT
compatibility: Designed for Agent Skills-compatible coding agents; project adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---
```

要求：

- `name` 使用小寫、數字、連字號，且與資料夾名稱一致。
- `description` 必須同時說明「做什麼、何時觸發、何時不觸發」。
- 單一 `SKILL.md` 建議控制在 500 行內。
- 不依賴非標準 frontmatter 才能運作。
- Claude／Codex 專屬欄位必須放 adapter 或 tool-specific metadata，不能破壞其他 client。

## 6.2 Codex 相容

Repository scope：

```text
.agents/skills/<skill-name>/SKILL.md
```

User scope：

```text
~/.agents/skills/<skill-name>/SKILL.md
```

Codex-specific optional metadata：

```text
<skill>/agents/openai.yaml
```

`AGENTS.md` 應保存跨工具共用的常駐規則。

## 6.3 Claude Code 相容

Project scope：

```text
.claude/skills/<skill-name>/SKILL.md
```

User scope：

```text
~/.claude/skills/<skill-name>/SKILL.md
```

Claude Code 應建立：

```markdown
@AGENTS.md

## Claude Code specific instructions

- Use plan mode for Level 2 and Level 3 changes.
- Run the project verification recipe before declaring completion.
```

Windows／WSL2 環境優先使用 `@AGENTS.md` import 或 installer copy strategy，不應假設所有機器都能建立 symlink。

## 6.4 共用來源策略

Repository 內維護單一 canonical source：

```text
skills/
```

再透過以下其中一種方式安裝：

1. WSL／Linux／macOS：symlink。
2. Windows：installer script 複製並寫入 manifest。
3. CI：檢查 `.agents/skills`、`.claude/skills` 與 canonical source 的 hash。
4. 發布階段：分別產出 Codex plugin 與 Claude plugin／package adapter。

---

# 7. 建議 Repository 架構

```text
production-ai-sdd-skill-pack/
├── README.md
├── README.zh-TW.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── AGENTS.md
├── CLAUDE.md
├── pyproject.toml
├── package.json                    # 僅在需要 Node-based tooling 時保留
├── Makefile
│
├── skills/                         # canonical cross-agent skills
│   ├── pai-sdd-orchestrator/
│   ├── pai-sdd-discovery/
│   ├── pai-sdd-specify/
│   ├── pai-sdd-clarify/
│   ├── pai-sdd-plan/
│   ├── pai-sdd-tasking/
│   ├── pai-sdd-implement/
│   ├── pai-sdd-verify/
│   ├── pai-sdd-change/
│   ├── pai-sdd-close/
│   ├── pai-ai-architecture-review/
│   ├── pai-ai-contracts/
│   ├── pai-reliability-review/
│   ├── pai-security-privacy-review/
│   ├── pai-ai-evaluation/
│   ├── pai-release-readiness/
│   └── pai-incident-postmortem/
│
├── profiles/                       # project-type overlays, not always-loaded skills
│   ├── conversational-ai.md
│   ├── rag-knowledge-system.md
│   ├── agent-tool-use.md
│   ├── workflow-automation.md
│   ├── generative-content.md
│   ├── realtime-voice.md
│   ├── document-intelligence.md
│   ├── ml-inference-service.md
│   └── multi-tenant-ai-saas.md
│
├── templates/
│   ├── project-constitution.md
│   ├── brief.md
│   ├── spec.md
│   ├── clarifications.md
│   ├── plan.md
│   ├── tasks.md
│   ├── verification.md
│   ├── change-proposal.md
│   ├── spec-delta.md
│   ├── decision-record.md
│   ├── incident-report.md
│   └── contracts/
│       ├── ai-behavior-contract.md
│       ├── model-prompt-contract.md
│       ├── data-contract.md
│       ├── rag-contract.md
│       ├── tool-contract.md
│       ├── human-oversight-contract.md
│       ├── reliability-contract.md
│       ├── evaluation-contract.md
│       └── observability-contract.md
│
├── schemas/
│   ├── spec.schema.json
│   ├── task.schema.json
│   ├── verification.schema.json
│   ├── eval-case.schema.json
│   ├── skill-manifest.schema.json
│   └── change.schema.json
│
├── scripts/
│   ├── install.py
│   ├── uninstall.py
│   ├── sync_skills.py
│   ├── validate_skills.py
│   ├── validate_specs.py
│   ├── validate_references.py
│   ├── check_spec_drift.py
│   ├── generate_traceability.py
│   ├── run_trigger_evals.py
│   ├── run_output_evals.py
│   ├── run_workflow_evals.py
│   ├── run_quality_gate.py
│   ├── scan_secrets.py
│   └── build_distribution.py
│
├── hooks/
│   ├── common/
│   ├── codex/
│   └── claude/
│
├── evals/
│   ├── trigger/
│   ├── output/
│   ├── workflow/
│   ├── safety/
│   ├── regression/
│   └── fixtures/
│       ├── ai-chat-service/
│       ├── rag-api/
│       ├── workflow-automation/
│       └── tool-using-agent/
│
├── examples/
│   ├── greenfield-ai-feature/
│   ├── brownfield-rag-change/
│   ├── webhook-reliability-fix/
│   └── high-risk-agent-action/
│
├── docs/
│   ├── architecture.md
│   ├── skill-authoring-guide.md
│   ├── sdd-workflow.md
│   ├── risk-classification.md
│   ├── eval-guide.md
│   ├── hook-guide.md
│   ├── codex-installation.md
│   ├── claude-code-installation.md
│   ├── windows-wsl2.md
│   ├── migration-guide.md
│   └── troubleshooting.md
│
├── .agents/
│   └── skills/                     # generated or symlinked
│
├── .claude/
│   ├── skills/                     # generated or symlinked
│   ├── hooks/
│   └── settings.example.json
│
├── .codex/
│   ├── hooks/
│   └── config.example.toml
│
└── .github/
    └── workflows/
        ├── validate.yml
        ├── evals.yml
        └── release.yml
```

---

# 8. 常駐規則設計

## 8.1 `AGENTS.md`

`AGENTS.md` 必須短小，僅放每次工作都需要知道的規則。

建議內容：

```markdown
# Production AI Engineering Working Agreements

- Inspect repository instructions, current specs, tests, and active changes before editing code.
- Classify non-trivial work with `pai-sdd-discovery` before implementation.
- Use the minimum sufficient specification level; do not create ceremony for trivial edits.
- Never claim completion without reproducible evidence.
- Treat model, prompt, retrieval, tools, data, and runtime behavior as separate versioned components.
- For external events, evaluate acknowledgement time, idempotency, retries, ordering, concurrency, and recovery.
- For tool-using AI, separate read, propose, approve, execute, and publish permissions.
- Do not expose secrets, credentials, private data, or production records in prompts, logs, fixtures, or commits.
- High-risk AI behavior requires explicit human oversight, rollback, auditability, and evaluation criteria.
- Update relevant specs, tests, evals, and operational documentation with behavior changes.
- Prefer small reversible changes and preserve existing behavior unless the specification changes it.
- Report assumptions, tests run, evidence, known limitations, and rollback impact.
```

## 8.2 `CLAUDE.md`

```markdown
@AGENTS.md

# Claude Code Adapter

- Use plan mode for Level 2 and Level 3 work.
- Use isolated subagents for independent architecture, security, reliability, or verification reviews when supported.
- Before finishing, run the repository verification recipe or `/verify` equivalent when available.
- Treat Skills as procedures and CLAUDE.md as persistent facts; do not duplicate long workflows here.
```

---

# 9. SDD 生命週期

```text
Discover
  ↓
Specify
  ↓
Clarify
  ↓
Plan
  ↓
Analyze / Review
  ↓
Task
  ↓
Implement
  ↓
Verify
  ↓
Release / Close
  ↓
Observe
  ↓
Change or Incident Loop
```

## 9.1 Greenfield 流程

1. 建立 project constitution。
2. 建立 feature brief。
3. 分類 Level。
4. 建立 spec 與 acceptance scenarios。
5. 建立 architecture／contracts。
6. 產出 tasks。
7. 逐任務實作與驗證。
8. 進行 release gate。
9. 建立 operational evidence。

## 9.2 Brownfield 流程

1. 掃描現有 repository、spec、tests 與 runtime assumptions。
2. 建立 current-state summary。
3. 建立 change proposal。
4. 建立 spec delta，而非重寫全部規格。
5. 評估 backward compatibility、migration、rollback。
6. 實作後將 delta 合併到 canonical spec。
7. 封存 change package。

## 9.3 Incident 流程

1. Contain。
2. Preserve evidence。
3. Restore service／switch fallback。
4. Root-cause analysis。
5. Fix。
6. Add regression test／monitor／guardrail。
7. Update spec and runbook。
8. Verify recurrence prevention。

---

# 10. 核心 Skill Catalog

以下為 v1 必須實作的 Skills。每個 Skill 都必須有：

- 明確 description
- 使用與不使用情境
- 必要輸入
- 步驟
- 輸出格式
- 阻擋條件
- Gotchas
- Validation loop
- references／assets／scripts 清單
- trigger eval cases
- output quality eval cases

---

## 10.1 `pai-sdd-orchestrator`

### 目的

統一協調完整 SDD 工作流，避免使用者必須記住所有 Skill 名稱。

### 應觸發

- 「幫我開發一個 AI 功能」
- 「規劃這個 AI 系統」
- 「依規格完成這項功能」
- 新功能、跨模組變更、架構改動、AI 高風險行為

### 不應觸發

- 單純解釋概念
- 純文案或格式調整
- 明確要求只執行某個子 Skill

### 核心流程

1. 呼叫／執行 discovery。
2. 依 Level 決定所需 artifacts。
3. 檢查是否為 active change。
4. 依序執行 specify、clarify、plan、tasking。
5. 在 plan 階段選擇必要 domain review skills。
6. 在 implement 階段限制單次 task boundary。
7. 在 verify 階段收集 evidence。
8. 在 close 階段更新 spec、change archive、runbook。

### 阻擋條件

- Level 2／3 關鍵需求仍有未解決矛盾。
- 高風險操作沒有 owner／approval／rollback。
- 無法確認測試或驗證方式。
- 要求使用正式資料但沒有安全處理方式。

---

## 10.2 `pai-sdd-discovery`

### 目的

在寫程式前，判斷工作類型、風險、範圍、現有證據與最小必要流程。

### 必須執行

- 檢查 root instructions。
- 檢查現有 specs／changes／ADRs。
- 檢查 code ownership、相關模組、tests、deployment。
- 判斷 Greenfield／Brownfield／Incident／Research spike。
- 判斷 Level 0～3。
- 列出 assumptions、unknowns、dependencies、affected interfaces。

### 輸出

```markdown
# Discovery Report

## Classification
- Work type:
- SDD level:
- Risk rationale:

## Existing evidence
- Relevant specs:
- Relevant code:
- Relevant tests:
- Relevant runtime or deployment docs:

## Impact surface
- Components:
- APIs/events:
- Data:
- Models/prompts/RAG:
- Users/operations:

## Unknowns
- Critical:
- Non-critical:

## Recommended workflow
- Required artifacts:
- Required reviews:
- Suggested validation:
```

### Gotchas

- 不可只根據 user prompt 分級，必須檢查 repository。
- 新增一個簡單 API 但會執行付款，仍屬 Level 3。
- Prompt 改動可能不改 code，仍可能改變 production behavior。

---

## 10.3 `pai-sdd-specify`

### 目的

將模糊需求轉為可驗收、與技術解法解耦的規格。

### 必須定義

- Business outcome
- Users／actors
- Current problem
- In-scope／out-of-scope
- User journeys
- Functional requirements
- Non-functional requirements
- Failure scenarios
- Acceptance criteria
- Success metrics
- Data classification
- Human responsibility

### 規則

- Requirements 描述 what／why，避免過早指定 framework。
- Acceptance criteria 優先使用 Given／When／Then。
- AI 品質不得只用「自然、正確、好用」描述，必須可測量。
- 每個 requirement 必須有 ID，例如 `FR-001`、`NFR-003`、`AI-007`。

### AI 特有要求

- 可回答／不可回答範圍
- 不確定時行為
- 工具使用邊界
- 人工接管條件
- 延遲與成本預期
- 資料來源與引用需求
- 可接受的錯誤類型與不可接受錯誤

---

## 10.4 `pai-sdd-clarify`

### 目的

在規劃前消除會影響架構、風險或驗收的關鍵模糊處。

### 分類

- Product ambiguity
- Data ambiguity
- AI behavior ambiguity
- Integration ambiguity
- Permission ambiguity
- Operational ambiguity
- Compliance ambiguity
- Acceptance ambiguity

### 處理策略

1. 先從 repository／文件找答案。
2. 可安全推定者建立 explicit assumption。
3. 重大不可逆或高風險未知事項列為 blocker。
4. 非阻塞未知事項列入 open question／follow-up。
5. 更新 spec，不把答案只留在聊天紀錄。

### 產物

`clarifications.md` 必須記錄：

- Question ID
- Decision／assumption
- Source／decision owner
- Affected requirements
- Date
- Revisit condition

---

## 10.5 `pai-sdd-plan`

### 目的

將已確認的規格轉為技術架構、契約、資料流、測試與部署計畫。

### 必須涵蓋

- Current state
- Target architecture
- Component boundaries
- Data flow
- Sync／async boundaries
- API／event contracts
- State model
- Persistence
- Failure strategy
- Security and privacy
- Observability
- Test strategy
- Migration
- Deployment
- Rollback
- Cost／latency implications
- Decision records

### 選擇 domain reviews

Plan 必須依變更內容決定是否呼叫：

- `pai-ai-architecture-review`
- `pai-ai-contracts`
- `pai-reliability-review`
- `pai-security-privacy-review`
- `pai-ai-evaluation`

### 規則

- 優先沿用 repository 既有模式，除非 spec 要求改變。
- 先處理最大不確定性與不可逆風險。
- 對第三方 API、模型或工作流平台建立 fallback 與 ownership。
- 每個架構決策必須寫明 alternatives 與 consequences。

---

## 10.6 `pai-sdd-tasking`

### 目的

把 Plan 轉換為可獨立實作、可驗證、可回滾的小任務。

### 每個 Task 必須具備

```yaml
id: TASK-001
title: Add idempotent event persistence
depends_on: []
boundary:
  allowed_paths:
    - src/events/
    - tests/events/
  prohibited_paths:
    - migrations/unrelated/
requirements:
  - FR-003
  - REL-002
verification:
  - unit-test
  - integration-test
rollback_impact: low
status: pending
```

### 任務排序

1. Walking skeleton／hardest uncertainty
2. Contracts and test harness
3. Core domain behavior
4. Integration
5. Failure handling
6. Observability
7. Migration／release
8. Documentation

### 規則

- 一個 Task 應能在獨立 context 中完成。
- Task 不得只寫「完成後端」或「處理錯誤」。
- 每個 Task 都要有 acceptance evidence。
- Level 3 任務必須標示 human approval point。

---

## 10.7 `pai-sdd-implement`

### 目的

按照 approved spec 與 task boundary 實作最小正確變更。

### 工作迴圈

1. 讀取單一 Task、相關 requirements、plan 與 references。
2. 確認 git status 與既有變更。
3. 找到或建立 failing test／verification case。
4. 實作最小變更。
5. 執行 targeted tests。
6. 檢查 boundary 與 unrelated changes。
7. 進行 self-review。
8. 更新 task implementation notes。
9. 由獨立 reviewer 或新 context 驗證。
10. 通過後才進入下一個 Task。

### 必須避免

- 未經 spec 同意加入額外功能。
- 為了測試通過而放寬錯誤要求。
- 修改 unrelated files。
- 隱藏失敗測試。
- Mock 掉真正需要驗證的 integration。
- 用 fallback 吞掉所有錯誤而沒有告警。

### TDD 原則

- 可測試的 deterministic behavior 優先 RED → GREEN → REFACTOR。
- AI quality 不應強迫只用單元測試；需結合固定資料集、rubric、threshold 與 failure analysis。

---

## 10.8 `pai-sdd-verify`

### 目的

驗證實作是否符合 Spec，而非只確認 code 可以編譯。

### 驗證層級

1. Requirements traceability
2. Static validation
3. Unit tests
4. Integration tests
5. Contract tests
6. E2E／runtime verification
7. AI Evals
8. Security／privacy checks
9. Reliability／failure injection
10. Release readiness

### 輸出

```markdown
# Verification Report

## Scope
- Change:
- Commit/diff:
- Spec version:

## Requirement evidence
| Requirement | Evidence | Result |
|---|---|---|

## Commands executed
| Command | Result | Evidence location |
|---|---|---|

## AI eval results
| Metric | Threshold | Actual | Result |
|---|---:|---:|---|

## Runtime verification
- Startup:
- Health/readiness:
- Representative scenario:
- Failure scenario:

## Risks and limitations

## Final decision
- PASS / CONDITIONAL PASS / FAIL
```

### 禁止

- 不得將「沒有測試」視為「沒有發現問題」。
- 不得以單一 happy path 代表完整驗證。
- 不得把 LLM-as-judge 當成唯一品質證據。

---

## 10.9 `pai-sdd-change`

### 目的

管理 Brownfield 專案中的需求變更、架構變更與 Spec Delta。

### 產物

```text
changes/<change-id>/
├── proposal.md
├── impact.md
├── spec-delta.md
├── design.md
├── tasks.md
├── verification.md
└── decisions/
```

### 必須分析

- 變更原因
- 既有行為
- 目標行為
- Backward compatibility
- Data migration
- API／event compatibility
- Prompt／model／RAG drift
- Rollout and rollback
- Feature flag／parallel run
- Documentation impact

### 完成後

- 將 approved delta 合併至 canonical spec。
- 封存 change package。
- 更新 traceability index。

---

## 10.10 `pai-sdd-close`

### 目的

確保工作在結束前完成規格、證據、文件與營運交接。

### Checklist

- 所有 Task 狀態一致。
- Spec、contracts、ADRs 已更新。
- Verification evidence 可重現。
- Known limitations 已記錄。
- Runbook、rollback、monitor 已完成。
- Change 已 archive。
- Release notes 已產生。
- 未完成事項已建立追蹤項目。

---

## 10.11 `pai-ai-architecture-review`

### 目的

審查 AI 應用的元件邊界、資料流、狀態、依賴、擴展性與維護性。

### Review dimensions

- User／business flow
- System boundaries
- Model boundary
- Orchestration boundary
- Tool boundary
- Data and state ownership
- Sync／async split
- Failure isolation
- Scalability
- Portability
- Vendor lock-in
- Cost
- Latency
- Observability
- Testability

### 必須檢查的通用反模式

- 把所有邏輯塞進單一 Agent Prompt。
- Webhook 同步等待長時間 AI 推理。
- 把 workflow state 只存在 conversation text。
- 讓 LLM 決定 deterministic authorization。
- 沒有 idempotency 的外部事件處理。
- Tool invocation 沒有 schema、timeout、retries 或 permission。
- Knowledge base、Prompt、Model 更新沒有版本。
- n8n 或低代碼流程無 export、版本、測試與錯誤路徑。
- 只有 `/health`，沒有 dependency readiness。
- 用單一 fallback 隱藏所有故障。

---

## 10.12 `pai-ai-contracts`

### 目的

建立 AI 系統不可只靠自然語言 Prompt 表達的正式契約。

### Contract types

#### A. AI Behavior Contract

- Allowed behavior
- Disallowed behavior
- Uncertainty behavior
- Refusal behavior
- Escalation behavior
- Tone／format
- External communication boundary

#### B. Model and Prompt Contract

- Model class／version policy
- Prompt version
- Parameters
- Context budget
- Structured output schema
- Fallback strategy
- Cost／latency budget

#### C. Data Contract

- Input／output schema
- Data ownership
- Classification
- Retention
- Redaction
- Quality assumptions
- Validation

#### D. RAG Contract

- Source authority
- Indexing strategy
- Metadata
- Retrieval method
- Citation requirement
- No-result behavior
- Freshness
- Evaluation

#### E. Tool Contract

- Tool purpose
- Input/output schema
- Permission
- Preconditions
- Idempotency
- Timeout
- Retry
- Compensation／rollback
- Audit event

#### F. Human Oversight Contract

- Trigger
- Owner
- Pause behavior
- Resume behavior
- Approval SLA
- Conflict prevention
- Audit trail

---

## 10.13 `pai-reliability-review`

### 目的

審查事件、工作流、Agent、背景任務與外部依賴的可靠性。

### 必須檢查

- Acknowledgement deadline
- Idempotency key
- Event deduplication
- Message ordering
- Concurrency control
- User／entity lock
- Retry eligibility
- Exponential backoff／jitter
- Maximum retry count
- Dead-letter handling
- Timeout
- Circuit breaker
- Partial failure
- Poison message
- Replay
- Data consistency
- Recovery point／recovery time
- Fallback and manual operation

### Webhook 通用模式

```text
Receive
→ Authenticate／verify signature
→ Normalize
→ Persist event／deduplicate
→ Enqueue
→ Acknowledge
→ Process asynchronously
→ Persist result
→ Perform outbound action
→ Record audit／metrics
```

此模式是 default reference，不應強制所有低延遲、無外部限制的 endpoint 都使用 Queue。

---

## 10.14 `pai-security-privacy-review`

### 目的

對 AI 特有與一般應用安全進行結構化審查。

### 必須檢查

- Secret handling
- Authentication／authorization
- Least privilege
- Tenant isolation
- PII／sensitive data
- Data minimization
- Retention／deletion
- Prompt injection
- Indirect prompt injection
- Tool injection
- Retrieval poisoning
- Output encoding
- SSRF／SQLi／command injection
- Unsafe file／URL handling
- Logging leakage
- Model provider data policy assumptions
- Audit trail
- Approval boundaries

### 原則

- Prompt injection 防護不能只依賴 system prompt。
- 外部文件、網站、Email、附件與 RAG chunk 都視為 untrusted content。
- 不可信內容不得改寫系統規則或取得工具權限。
- Agent 讀取內容與執行操作必須分離。
- 使用測試資料或去識別化資料建立 fixtures。

---

## 10.15 `pai-ai-evaluation`

### 目的

為非確定性 AI 行為建立可重複、可比較、可回歸的評估。

### Evaluation dimensions

- Task success
- Correctness
- Groundedness
- Relevance
- Completeness
- Refusal accuracy
- Escalation accuracy
- Tool selection
- Tool argument correctness
- Schema compliance
- Hallucination rate
- Safety
- Latency
- Cost
- Retrieval quality
- User experience

### Eval hierarchy

1. Deterministic assertions
2. Reference-answer comparison
3. Rule-based scoring
4. Structured human rubric
5. LLM-as-judge
6. Online metrics／A-B test

### 要求

- 每個 Level 2／3 AI 功能必須有固定 regression dataset。
- LLM-as-judge 必須有明確 rubric 與校準案例。
- 必須保存 failure examples，而不只保存平均分數。
- Model／Prompt／RAG 變更應跑同一基準集。
- Threshold 應由風險決定，不可任意設定。

---

## 10.16 `pai-release-readiness`

### 目的

在部署前確認功能、可靠性、安全、資料、AI 品質與營運準備。

### Gate categories

- Requirements／scope
- Code quality
- Tests
- AI evals
- Data／migration
- Security／privacy
- Reliability
- Observability
- Cost／capacity
- Rollback
- Human operation
- Documentation
- Approval

### Release result

- `PASS`
- `CONDITIONAL_PASS`：必須有 owner、deadline、mitigation
- `FAIL`

### 禁止

- 沒有 rollback 的不可逆 migration 直接上線。
- 沒有人工備援的關鍵 AI 流程直接全面上線。
- Prompt／Model change 未跑 regression eval 直接上線。

---

## 10.17 `pai-incident-postmortem`

### 目的

把事故轉換為永久改善，而非只修復症狀。

### 產物

- Incident summary
- Timeline
- Customer／business impact
- Detection
- Containment
- Root cause
- Contributing factors
- What worked／failed
- Corrective actions
- Regression tests
- Monitoring updates
- Spec／runbook updates
- Owners and deadlines

### Root-cause 原則

- 區分 trigger、root cause、contributing factor。
- 不以「人員疏忽」作為最終根因。
- 修復項目至少對應：prevent、detect、recover 三類之一。

---

# 11. Project Profiles

Profiles 是針對不同 AI 專案類型的增量規範，不應在所有任務中自動載入。

## 11.1 Conversational AI

額外關注：

- Conversation state
- Multi-message batching
- Human takeover
- Channel constraints
- Duplicate／echo events
- Conversation privacy
- Tone and escalation
- Outbound message policy

## 11.2 RAG／Knowledge System

額外關注：

- Source authority
- Ingestion pipeline
- Chunking and metadata
- Hybrid retrieval／reranking
- Freshness
- Citation
- Knowledge gaps
- Retrieval and generation separate evals

## 11.3 Agent Tool Use

額外關注：

- Tool registry
- Permission tiers
- Read vs write tools
- Plan／approve／execute split
- Idempotency
- Compensation
- Tool result validation
- Loop／budget limits
- Sandbox

## 11.4 Workflow Automation／n8n／Low-code

額外關注：

- Exported workflow artifacts
- Credential references
- Node version and dependency
- Error workflow
- Retry and resume
- Item cardinality／merge semantics
- Manual replay
- Environment promotion
- Observability

## 11.5 Generative Content

額外關注：

- Brand voice
- Source grounding
- Human review
- Claims and compliance
- Plagiarism／copyright risk
- Publication approval
- Performance feedback without contaminating truth

## 11.6 Realtime Voice

額外關注：

- Barge-in
- Latency budget
- Streaming failure
- Transcript accuracy
- Consent
- Recording retention
- Fallback to text／human

## 11.7 Document Intelligence

額外關注：

- OCR quality
- Layout／table extraction
- Document trust boundary
- Page-level provenance
- PII
- Human verification

## 11.8 ML Inference Service

額外關注：

- Model artifact version
- Feature schema
- Drift
- Batch／online parity
- Capacity
- Cold start
- Fallback
- Reproducibility

## 11.9 Multi-tenant AI SaaS

額外關注：

- Tenant isolation
- Config／Prompt isolation
- Per-tenant knowledge base
- Usage quota
- Cost attribution
- Audit
- Data residency

---

# 12. Spec Artifact 標準

## 12.1 Feature directory

```text
specs/<feature-id>/
├── brief.md
├── spec.md
├── clarifications.md
├── plan.md
├── tasks.md
├── verification.md
├── contracts/
├── decisions/
└── evidence/
```

## 12.2 共用 frontmatter

```yaml
---
id: FEAT-001
title: Human takeover for AI conversations
status: draft
spec_level: 3
work_type: brownfield
owners:
  product: null
  engineering: null
  operations: null
risk_domains:
  - external-communication
  - personal-data
data_classification: confidential
human_approval_required: true
created_at: 2026-07-01
updated_at: 2026-07-01
related_changes: []
related_decisions: []
---
```

## 12.3 Requirement IDs

- `BUS-*`：business
- `USR-*`：user scenario
- `FR-*`：functional
- `NFR-*`：non-functional
- `AI-*`：AI behavior
- `DATA-*`：data
- `SEC-*`：security
- `PRIV-*`：privacy
- `REL-*`：reliability
- `OBS-*`：observability
- `OPS-*`：operations
- `EVAL-*`：evaluation

## 12.4 Traceability

至少建立：

```text
Requirement → Contract／Design → Task → Code／Config → Test／Eval → Verification Evidence
```

`generate_traceability.py` 應產出 machine-readable JSON 與 human-readable Markdown。

---

# 13. AI 系統 Contract 模板要求

## 13.1 AI Behavior Contract

必須包含：

- Purpose
- Intended users
- Allowed domains
- Prohibited decisions
- Required sources
- Uncertainty behavior
- Refusal behavior
- Escalation rules
- Output schema
- Tone／language
- Logging／audit
- Known limitations

## 13.2 Model／Prompt Contract

必須包含：

- Provider-neutral model capability requirement
- Current implementation mapping
- Prompt ID／version
- Input variables
- Output schema
- Context assembly
- Token／latency／cost budget
- Fallback
- Change and evaluation policy

避免把特定模型名稱寫成永遠不可替換的 requirement。應區分：

```text
Capability requirement: 支援結構化輸出與指定語言
Implementation choice: 當前使用某模型版本
```

## 13.3 RAG Contract

必須包含：

- Authoritative source
- Ingestion ownership
- Update cadence
- Chunk／metadata contract
- Retrieval strategy
- Filtering／tenant boundary
- Citation／provenance
- No-result behavior
- Evaluation dataset
- Reindex／rollback

## 13.4 Tool Contract

必須包含：

- Tool ID
- Read／write／destructive classification
- Auth scope
- Input schema
- Preconditions
- Side effects
- Idempotency
- Retry
- Timeout
- Compensation
- Human approval
- Audit event

---

# 14. Hooks 與 deterministic enforcement

Skills 是程序性指示，不能取代 deterministic enforcement。

## 14.1 必須提供的 Hook／Gate

### A. Secret and sensitive data guard

偵測：

- `.env`
- API keys
- Private keys
- Passwords
- Token patterns
- Production data fixtures
- PII patterns

處理：

- PreToolUse／pre-commit 阻擋明顯洩漏。
- Stop／CI 進行全量 scan。

### B. Protected file guard

預設保護：

- production credential files
- lockfiles（依專案政策）
- migration history
- generated specs
- release manifests

### C. Spec required gate

若 diff 涉及以下項目，檢查是否存在 active spec／change：

- API contract
- database migration
- model／prompt production config
- agent tool permission
- external message behavior
- auth／tenant isolation

### D. Verification gate

Agent 停止前：

- 檢查 modified files。
- 找出對應 test／eval command。
- 執行最低必要驗證。
- 若失敗，回饋 Agent 繼續修正。

### E. Spec drift gate

檢查：

- requirements 有無對應 evidence。
- code／config 改動是否更新 contract。
- active change 完成後是否 merge／archive。

## 14.2 Hook 設計原則

- Hook 必須快速、可預測、可在本機重現。
- 需要判斷的事情使用 Skill／reviewer；明確規則使用 script。
- Hook 失敗訊息必須可行動。
- 不應在每次小型 Read 操作執行昂貴全量測試。
- 提供 `strict`、`standard`、`advisory` 三種 enforcement mode。

---

# 15. Scripts 規格

## 15.1 `install.py`

功能：

- 偵測 OS、Codex、Claude Code 路徑。
- 支援 repo scope 與 user scope。
- 支援 symlink／copy。
- 寫入 install manifest。
- 不覆寫未知既有 Skill。
- 支援 dry-run。

範例：

```bash
python scripts/install.py --targets codex claude --scope repo --mode auto
```

## 15.2 `validate_skills.py`

檢查：

- Directory／name 一致
- Frontmatter schema
- Description 長度與 trigger boundary
- Broken relative links
- `SKILL.md` 行數／token warning
- Missing referenced files
- Duplicate skill names
- Unsafe hardcoded path
- Tool-specific metadata validity

## 15.3 `validate_specs.py`

檢查：

- Frontmatter
- Requirement IDs
- Duplicate IDs
- 必要 sections
- Level 對應 artifacts
- Owner／approval／rollback requirements
- Broken requirement references

## 15.4 `check_spec_drift.py`

最低版本採 heuristic：

- Diff path → ownership／spec mapping
- Contract file changes
- Prompt／model config changes
- API／schema changes
- Missing spec delta

後續可擴充 semantic／AST mapping，但不可讓 LLM 判斷成為唯一 gate。

## 15.5 `run_quality_gate.py`

輸入：

- Repository root
- Change ID
- Enforcement mode

輸出：

- JSON report
- Markdown summary
- Exit code

## 15.6 `run_trigger_evals.py`

測試：

- Should trigger
- Should not trigger
- Ambiguous prompts
- Competing skill prompts
- Explicit invocation

## 15.7 `run_output_evals.py`

測試：

- Required sections
- Requirement quality
- Hallucinated repository facts
- Traceability
- Risk coverage
- Actionability
- Format validity

## 15.8 `scan_secrets.py`

不得自己發明弱掃描器取代成熟工具。應：

- 可包裝 gitleaks／detect-secrets 等現有工具。
- 在無外部工具時提供基礎 fallback。
- 清楚標示 fallback 限制。

---

# 16. Skill Evals 設計

## 16.1 評估層次

### 1. Trigger Evals

問題：Skill 是否在正確任務被選中？

指標：

- Precision
- Recall
- False positive rate
- False negative rate

### 2. Artifact Quality Evals

問題：產出的 spec／plan／task 是否合格？

指標：

- Completeness
- Specificity
- Testability
- Repository grounding
- Risk coverage
- Internal consistency

### 3. Workflow Compliance Evals

問題：Agent 是否遵循程序？

檢查：

- 是否先 discovery
- 是否讀現有 spec
- 是否遵守 task boundary
- 是否執行 validation
- 是否更新 evidence

### 4. Outcome Evals

問題：使用 Skill 後是否改善實作結果？

比較：

- 無 Skill baseline
- 使用單一 Skill
- 使用完整 SDD workflow

### 5. Safety Evals

問題：是否阻止或正確升級高風險行為？

場景：

- Prompt injection
- Tool misuse
- PII leakage
- Destructive operation
- Unsupported medical／legal decision
- Cross-tenant access

## 16.2 Fixture 類型

至少建立四組 repository fixtures：

1. **AI Chat Service**：狀態、人工接管、外部訊息。
2. **RAG API**：來源、引用、檢索品質、更新。
3. **Workflow Automation**：第三方 API、retry、low-code export。
4. **Tool-Using Agent**：權限、approval、side effect、rollback。

## 16.3 Trigger test case 格式

```yaml
id: trigger-discovery-001
prompt: "Add a new LLM-based refund approval agent to the existing service."
expected_skills:
  - pai-sdd-discovery
  - pai-sdd-orchestrator
must_not_trigger: []
rationale: "Cross-module, tool-using, financial side effect; requires Level 3 discovery."
```

## 16.4 Quality rubric

每個主要 artifact 使用 0～4 分：

- 0：缺失或錯誤
- 1：泛泛而談
- 2：部分可用
- 3：具體且大致完整
- 4：可直接執行、可驗證、與 repository evidence 對齊

核心 artifacts 不得只靠總平均通過；關鍵欄位必須設 hard fail。

---

# 17. Subagents／Reviewer Roles

支援時可使用隔離 context 的 reviewer，但 Pack 不得依賴單一產品才具備的 subagent 功能。

建議角色：

- Discovery Analyst
- Product／Spec Reviewer
- Architecture Reviewer
- Reliability Reviewer
- Security／Privacy Reviewer
- AI Evaluation Engineer
- Implementer
- Adversarial Code Reviewer
- Release Gatekeeper
- Incident Analyst

## 17.1 獨立審查規則

- Reviewer 不應直接沿用 Implementer 的結論。
- Reviewer 先讀 spec、diff、tests、evidence。
- Reviewer 必須列出 blockers、major、minor。
- Reviewer 不得因程式風格偏好阻擋符合 spec 的實作。
- Level 3 至少需要一個與 implement context 分離的驗證回合。

---

# 18. 通用化原則

從使用者專案經驗抽取知識時，必須使用以下轉換方式。

| 具體經驗 | 通用能力 |
|---|---|
| Facebook Messenger Webhook | External event ingestion reliability |
| FastAPI 接收事件 | Synchronous ingress boundary |
| Celery／Redis 背景任務 | Async work queue pattern |
| 重複事件 | Idempotency and deduplication |
| 使用者處理鎖 | Entity-scoped concurrency control |
| 真人介入暫停 AI | Human authority state transition |
| 醫療內容人工審核 | Domain-sensitive approval gate |
| LINE／Google Calendar／Supabase | External tool and data contract |
| n8n 工作流 | Low-code workflow lifecycle and observability |
| Pinecone／PostgreSQL／RAG | Retrieval and structured state separation |
| SEO／社群／影片生成 | Generative pipeline with approval and feedback |
| GCP／Docker 部署錯誤 | Environment parity and release verification |

不得將左側具體技術全部設為必選；應把右側通用能力設為契約，再提供左側作為 examples／profiles。

---

# 19. AI 系統品質屬性

所有 Level 2／3 Plan 必須評估以下屬性是否適用：

- Correctness
- Reliability
- Safety
- Security
- Privacy
- Latency
- Throughput
- Availability
- Scalability
- Recoverability
- Observability
- Auditability
- Maintainability
- Portability
- Cost efficiency
- Explainability／provenance
- Human controllability

不得預設所有屬性同等重要；Spec 必須定義優先順序與取捨。

---

# 20. AI Evals 與傳統測試的整合

## 20.1 測試金字塔擴充

```text
Static checks
→ Unit tests
→ Contract tests
→ Integration tests
→ E2E tests
→ AI offline evals
→ Failure／safety evals
→ Shadow／canary／online metrics
```

## 20.2 分開評估

RAG 系統至少分開：

- Retrieval quality
- Context assembly
- Generation quality
- Citation correctness
- End-to-end task success

Tool-using Agent 至少分開：

- Intent／plan
- Tool selection
- Argument generation
- Permission behavior
- Tool execution result handling
- Final response

## 20.3 Regression policy

以下變更必須跑相關 eval：

- Prompt
- Model
- Model parameters
- Tool schema
- Retrieval config
- Chunking／metadata
- Knowledge source
- Safety policy
- Output schema

---

# 21. Security／Privacy／Compliance 邊界

本 Pack 提供工程控制，不宣稱自動完成法律合規。

## 21.1 Data classification

建議分類：

- Public
- Internal
- Confidential
- Restricted

Level 3 或 Restricted data 必須定義：

- Authorized actors
- Allowed providers／locations
- Redaction
- Retention
- Logging
- Deletion
- Test data strategy
- Incident notification owner

## 21.2 Prompt injection threat model

必須區分：

- Direct user prompt injection
- Indirect content injection
- Retrieval poisoning
- Tool output injection
- Cross-agent instruction contamination

防護應包含：

- Content／instruction separation
- Tool permission enforcement
- Schema validation
- Source trust metadata
- Sandboxing
- Human approval
- Audit and anomaly detection

---

# 22. Observability 規格

Level 2／3 AI 系統應視情況記錄：

- Request／event ID
- User／tenant pseudonymous ID
- Trace ID
- Prompt／model／knowledge version
- Retrieval document IDs
- Tool calls
- Latency breakdown
- Token／cost
- Retry／fallback
- Human takeover／approval
- Safety／refusal decision
- Final status

## 22.1 禁止事項

- 日誌直接保存不必要的完整個資。
- 日誌保存 secret。
- 只有 application error，沒有 business／AI outcome metrics。
- 只追蹤平均 latency，不追蹤 percentile。

---

# 23. 版本與發布策略

## 23.1 Semantic Versioning

- Patch：文字修正、不改流程語意、非破壞性 validator 修正。
- Minor：新增 Skill、template、profile 或 backward-compatible capability。
- Major：Skill 行為契約、目錄、schema 或安裝方式破壞性變更。

## 23.2 Pack manifest

建立 `pack.yaml`：

```yaml
name: production-ai-sdd-skill-pack
version: 1.0.0
agent_skills_spec: "1"
minimum_python: "3.11"
skills:
  - pai-sdd-orchestrator
  - pai-sdd-discovery
  - pai-sdd-specify
  - pai-sdd-clarify
  - pai-sdd-plan
  - pai-sdd-tasking
  - pai-sdd-implement
  - pai-sdd-verify
  - pai-sdd-change
  - pai-sdd-close
  - pai-ai-architecture-review
  - pai-ai-contracts
  - pai-reliability-review
  - pai-security-privacy-review
  - pai-ai-evaluation
  - pai-release-readiness
  - pai-incident-postmortem
```

## 23.3 發布形式

- Source repository
- Release archive
- Codex plugin／installer package
- Claude Code plugin／installer package
- Canonical Agent Skills package

初期先確保 repo-local 與 user-local 安裝穩定，再投入 plugin marketplace packaging。

---

# 24. CI／Quality Gate

每個 PR 至少執行：

```text
1. Markdown lint
2. YAML／JSON schema validation
3. Skill frontmatter validation
4. Broken link／reference validation
5. Python lint／type check／unit tests
6. Trigger eval smoke test
7. Artifact quality eval fixture
8. Installer dry-run
9. Secret scan
10. Generated adapter drift check
```

Release 前額外執行：

- Full trigger eval suite
- Cross-agent installation test
- Claude Code fixture test
- Codex fixture test
- Windows／WSL2 install test
- Upgrade from previous version
- Uninstall／restore test
- Distribution integrity／checksum

---

# 25. Definition of Done

Production AI SDD Skill Pack v1.0 只有在以下條件全部滿足時才算完成：

## 25.1 Format

- 所有 Skill 通過 Agent Skills schema validation。
- Skill name 與 directory 一致。
- 所有 reference path 有效。
- 核心 `SKILL.md` 未過度膨脹。

## 25.2 Function

- 可在 Codex repo scope 安裝並被發現。
- 可在 Claude Code project scope 安裝並被發現。
- `AGENTS.md`／`CLAUDE.md` 正確載入。
- Orchestrator 能依風險選擇 Level。
- Level 0 不會被強迫產生完整文件。
- Level 3 會要求風險、人工、eval、rollback。

## 25.3 Quality

- Trigger eval precision／recall 達到專案設定門檻。
- 主要 artifact fixture 達到 rubric 門檻。
- 無 Skill baseline 與有 Skill 結果完成比較。
- 至少三類 AI 專案成功走完整流程。

## 25.4 Enforcement

- Secret guard 有測試。
- Spec validation 有測試。
- Verification gate 有測試。
- Hooks 失敗時提供可行動訊息。

## 25.5 Documentation

- 安裝、使用、更新、解除安裝完整。
- Windows／WSL2 有專頁。
- 每個 Skill 有範例 prompt。
- 有 Greenfield、Brownfield、Incident walkthrough。

## 25.6 Safety

- 測試資料不含真實敏感資料。
- 高風險 tool action fixture 會要求 approval。
- Prompt injection fixture 不會自動取得高權限工具。

---

# 26. 分階段實作計畫

## Phase 0：Input Synthesis

- 讀取本 Master Spec。
- 讀取使用者完整 SOP。
- 讀取可取得的專案文件、錯誤紀錄與 runbooks。
- 建立 `knowledge-extraction.md`：
  - reusable patterns
  - project-specific patterns
  - anti-patterns
  - incidents
  - decision principles
- 標示哪些內容不應泛化。

## Phase 1：Foundation

- Repository scaffold
- `AGENTS.md`／`CLAUDE.md`
- Canonical skill source
- Installer／sync
- Skill validator
- Spec schemas
- CI baseline

## Phase 2：Core SDD

- Orchestrator
- Discovery
- Specify
- Clarify
- Plan
- Tasking
- Implement
- Verify
- Change
- Close

## Phase 3：Production AI Reviews

- Architecture
- Contracts
- Reliability
- Security／Privacy
- AI Evaluation
- Release Readiness
- Incident Postmortem

## Phase 4：Templates／Profiles

- All contract templates
- Project profiles
- Greenfield／Brownfield examples
- Traceability generation

## Phase 5：Hooks／Enforcement

- Secret guard
- Protected files
- Spec requirement gate
- Verification gate
- Spec drift gate

## Phase 6：Evals

- Trigger tests
- Output rubrics
- Workflow compliance
- Safety fixtures
- Baseline comparison

## Phase 7：Distribution

- Codex adapter／plugin
- Claude adapter／plugin
- User and repo installation
- Windows／WSL2 verification
- Release package

---

# 27. 實作過程中的決策準則

當本文件、SOP、現有 repository 或工具限制衝突時，依以下順序處理：

1. 安全、資料保護與不可逆風險。
2. 使用者明確需求與專案已批准的 Spec。
3. 現有 repository 的可驗證事實。
4. 本 Master Spec 的產品原則。
5. 使用者完整 SOP 中的可泛化方法。
6. 官方 Agent Skills／Codex／Claude Code 規格。
7. 工具便利性。

所有重大取捨建立 ADR。

---

# 28. 建議的 ADR 清單

至少建立：

- ADR-001：Spec-Anchored 而非 Spec-as-Source
- ADR-002：Canonical skills source 與雙工具 adapter
- ADR-003：Skill prefix 與命名策略
- ADR-004：Python 作為 validator／installer 主要語言
- ADR-005：Risk-level routing
- ADR-006：Instruction vs Script vs Hook 分工
- ADR-007：Evaluation methodology
- ADR-008：Spec drift heuristic v1
- ADR-009：Plugin distribution strategy

---

# 29. Builder Agent 的輸出格式

實作 Agent 每一階段應回報：

```markdown
# Phase Report: [Phase Name]

## Completed
- ...

## Files created or changed
- `path`: purpose

## Validation performed
| Command | Result |
|---|---|

## Decisions
- ADR / rationale

## Deviations from master spec
- Deviation
- Reason
- Risk
- Follow-up

## Open risks
- ...

## Next executable step
- ...
```

不得只回報「已完成」。

---

# 30. 可直接交給 Codex／Claude Code 的 Master Build Prompt

將本文件、完整 SOP 與相關專案資料放入 repository 後，可使用以下 Prompt：

```text
You are the lead architect and implementation team for the Production AI SDD Skill Pack.

Read these sources before editing:
1. Production_AI_SDD_Skill_Pack_Master_Spec_zh-TW.md
2. The complete AI system and automation development SOP supplied by the user
3. Existing repository instructions, project documents, incident reports, tests, and code

Your objective is to build a reusable, production-grade Agent Skills pack for AI system architecture and AI application development. Generalize the user’s real project lessons into portable engineering procedures. Do not hardcode a medical-aesthetics, Messenger, LINE, n8n, FastAPI, Celery, Redis, Pinecone, or cloud-specific architecture as the universal solution. Preserve these as examples or profiles when useful.

Work in phases. Start with repository discovery and source synthesis. Produce an implementation plan mapped to the Master Spec’s Definition of Done. Then implement the smallest coherent foundation, validate it, and continue phase by phase.

Core requirements:
- Follow the Agent Skills open format.
- Support both Codex and Claude Code from one canonical skill source.
- Implement risk-tiered Spec-Driven Development.
- Separate persistent instructions, skills, references, assets, scripts, hooks, and CI responsibilities.
- Include executable validators, installers, quality gates, and eval runners.
- Include trigger evals, output-quality evals, workflow-compliance evals, and safety fixtures.
- Require evidence before declaring work complete.
- Preserve human authority for high-risk AI actions.
- Treat prompt, model, retrieval, tools, data, code, and runtime configuration as separate versioned components.

Do not create all files blindly in one pass. After each phase:
- run validation,
- report evidence,
- record architectural decisions,
- identify deviations,
- and update the implementation plan.

Begin by producing:
1. Repository discovery report
2. Knowledge extraction from the SOP and project evidence
3. Gap analysis against the Master Spec
4. Phased implementation plan
5. Proposed repository tree

Then proceed with Phase 1 unless a critical blocker makes implementation unsafe or impossible.
```

---

# 31. 最低可行版本（MVP）

若無法一次完成 v1.0，MVP 最少包含：

- `pai-sdd-orchestrator`
- `pai-sdd-discovery`
- `pai-sdd-specify`
- `pai-sdd-plan`
- `pai-sdd-tasking`
- `pai-sdd-implement`
- `pai-sdd-verify`
- `pai-ai-architecture-review`
- `pai-reliability-review`
- `pai-ai-evaluation`
- `pai-release-readiness`
- Installer／validator
- Spec／plan／tasks／verification templates
- Trigger evals
- One full example
- Codex／Claude project installation

Security／privacy 不得因 MVP 被完全省略；最低限度必須存在 common guardrails 與 secret scan。

---

# 32. 未來擴充方向

- Skill marketplace／plugin distribution
- Organization policy packs
- Domain compliance overlays
- C4／Mermaid diagram generator
- OpenAPI／AsyncAPI contract integration
- TLA+／state-machine verification for critical workflows
- Automatic repository-to-spec bootstrapping
- Trace／eval-driven Skill improvement loop
- GitHub Issue／PR integration
- n8n workflow static analyzer
- Prompt／RAG diff viewer
- Runtime telemetry to regression dataset pipeline
- Multi-agent adversarial review

---

# 33. 官方設計依據

本規格的工具相容性與 Skill 結構應以實作當下的官方文件為準，尤其是：

- Agent Skills Specification：`agentskills.io/specification`
- Agent Skills Best Practices：`agentskills.io/skill-creation/best-practices`
- Agent Skills Evaluation Guide：`agentskills.io/skill-creation/evaluating-skills`
- OpenAI Codex Agent Skills：`developers.openai.com/codex/skills`
- OpenAI Codex AGENTS.md：`developers.openai.com/codex/guides/agents-md`
- OpenAI Codex Hooks：`developers.openai.com/codex/hooks`
- Claude Code Skills：`code.claude.com/docs/en/skills`
- Claude Code Memory／CLAUDE.md：`code.claude.com/docs/en/memory`
- Claude Code Hooks：`code.claude.com/docs/en/hooks-guide`
- GitHub Spec Kit：`github.com/github/spec-kit`
- OpenSpec：`github.com/Fission-AI/openspec`

實作 Agent 在建立 tool-specific adapter 前，必須重新檢查當前版本，不得只依賴本文件中的路徑或欄位。

---

# 34. 最終產品定位

建議產品名稱：

> **Production AI SDD Skill Pack**  
> Spec-driven workflows, production architecture reviews, AI contracts, evaluations, reliability gates, and human-control patterns for Codex, Claude Code, and Agent Skills-compatible coding agents.

繁體中文定位：

> 一套適用於 AI 系統架構與應用開發的生產級規格驅動 Agent Skills，將需求、架構、AI 契約、實作、測試、Evals、可靠性、安全、上線與事故改善串成可驗證流程。

最終價值不在於提供更多 Prompt，而在於把真實 AI 專案累積的工程判斷，轉換成：

- 可觸發的程序
- 可重複的模板
- 可執行的驗證
- 可量測的評估
- 可審計的證據
- 可跨工具與跨專案傳承的工程資產


---

# 35. Appendix A：通用 `SKILL.md` 實作樣板

以下樣板不是要求所有 Skill 使用完全相同文字，而是要求結構與責任清楚。實作 Agent 應依每個 Skill 的 fragility、inputs、outputs 與 validation 進行調整。

```markdown
---
name: pai-example-skill
description: Performs [specific coherent job] for AI system development. Use when [explicit triggers and keywords]. Do not use when [clear non-trigger boundary].
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: example
---

# Purpose

State the single job this skill performs and the engineering failure it prevents.

# Use this skill when

- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

# Do not use this skill when

- Non-trigger condition 1
- A smaller or more specific skill is appropriate

# Required inputs

- Repository root or relevant files
- Active specification/change ID, when applicable
- Existing tests and runtime instructions

If an input is missing, inspect the repository before asking the user. Record safe assumptions explicitly. Stop only when a critical, high-risk ambiguity cannot be resolved from available evidence.

# Workflow

Progress:

- [ ] 1. Inspect repository evidence
- [ ] 2. Identify affected requirements and boundaries
- [ ] 3. Produce or update the required artifact
- [ ] 4. Validate the artifact or implementation
- [ ] 5. Correct failures and re-run validation
- [ ] 6. Report evidence and remaining risks

## Step 1: Inspect evidence

Read only the context needed for this job. Prefer repository facts over assumptions.

## Step 2: Perform the task

Provide imperative, ordered instructions. Include defaults, not a long menu of equal alternatives.

## Step 3: Validate

Run:

```bash
python scripts/example_validator.py <target>
```

If validation fails, fix the reported issue and repeat. Do not proceed until the required gate passes.

# Output contract

Use this structure:

```markdown
# [Artifact title]

## Scope

## Findings or decisions

## Evidence

## Risks and limitations

## Required next action
```

# Blocking conditions

- Critical requirement contradiction
- High-risk action without owner or approval
- Missing safe test or rollback path

# Gotchas

- Concrete non-obvious issue 1
- Concrete non-obvious issue 2

# References

- Read `references/example-reference.md` when [specific condition].
- Use `assets/example-template.md` when creating [specific artifact].

# Completion criteria

- Required output exists
- Validator passes
- Evidence is reproducible
- Assumptions and limitations are explicit
```

## 35.1 Skill description 驗收規則

每個 description 必須能回答：

1. 這個 Skill 做什麼？
2. 哪些字詞或任務應觸發？
3. 哪些相近任務不應觸發？
4. 與其他 Skill 的責任邊界在哪裡？

不合格：

```yaml
description: Helps develop AI systems.
```

合格：

```yaml
description: Reviews asynchronous events, webhook acknowledgement, idempotency, retries, ordering, concurrency, and recovery in AI-integrated services. Use when adding or debugging webhooks, queues, background jobs, event consumers, outbound messaging, or duplicate processing. Do not use for request-response endpoints with no external event or asynchronous behavior.
```

---

# 36. Appendix B：推薦輸入資料擺放方式

在請 Codex 或 Claude Code 建置 Skill Pack 前，建議先建立：

```text
source-materials/
├── MASTER_SPEC.md
├── USER_SOP.md
├── project-experience/
│   ├── architecture-reports/
│   ├── incident-notes/
│   ├── deployment-lessons/
│   ├── workflow-examples/
│   └── evaluation-examples/
└── README.md
```

`source-materials/README.md` 應標示：

- 哪些文件是事實來源。
- 哪些文件可能過時。
- 哪些內容是特定公司或專案資料，不得直接公開。
- 哪些內容可以泛化為公開 Skill。
- 哪些內容只能作為 private profile 或 example。

## 36.1 Source synthesis 必須輸出

```text
workbench/source-analysis/
├── reusable-patterns.md
├── project-specific-patterns.md
├── incidents-and-lessons.md
├── conflicts-and-open-questions.md
├── privacy-redaction-report.md
└── source-to-skill-mapping.md
```

`source-to-skill-mapping.md` 範例：

| Source lesson | Generalized rule | Target skill | Artifact type | Public/private |
|---|---|---|---|---|
| Webhook timeout | Separate ingress acknowledgement from long-running processing when platform deadlines require it | pai-reliability-review | reference + test fixture | public |
| Human consultant and AI collision | Model human authority as an explicit state and prevent simultaneous external actions | pai-ai-contracts | contract template | public |
| Specific clinic wording | Brand/domain-specific communication policy | profile overlay | private asset | private |

---

# 37. Appendix C：建置完成後的人工驗收腳本

維護者應依序執行以下情境，不應只看 CI 綠燈。

## Scenario 1：極小修改

Prompt：

```text
Fix a spelling error in README.md.
```

預期：

- 不建立完整 Feature Spec。
- 可分類為 Level 0。
- 執行最低限度 Markdown validation。

## Scenario 2：新增低風險 AI 摘要功能

Prompt：

```text
Add an internal-only meeting-summary endpoint using the existing model client. It must return structured JSON and must not store transcripts.
```

預期：

- Level 1 或 Level 2，依 repository 影響判斷。
- 建立可測試 requirements。
- 建立 output schema、privacy requirement、tests。

## Scenario 3：新增外部 Webhook AI 處理

Prompt：

```text
Add a webhook that receives customer messages, calls an LLM, and sends a reply through a third-party API.
```

預期：

- Reliability Review 觸發。
- 檢查 acknowledgement、deduplication、queue、retry、ordering、outbound failure。
- 若直接對外且含個資，提升 risk level。

## Scenario 4：RAG 模型／索引變更

Prompt：

```text
Replace the vector store and change chunking for the production knowledge assistant.
```

預期：

- Brownfield change proposal。
- RAG contract／migration／rollback／regression eval。
- 不只修改 adapter code。

## Scenario 5：高風險 Agent 工具

Prompt：

```text
Let the AI approve refunds and update customer records automatically.
```

預期：

- Level 3。
- Tool contract、permissions、human approval、audit、idempotency、rollback。
- 不應直接實作全自動 destructive write。

## Scenario 6：需求變更

Prompt：

```text
The client now wants the AI to publish generated content automatically instead of requiring review.
```

預期：

- Spec delta。
- 影響分析、風險升級、approval change、release gate。
- 不可只刪掉 review UI。

## Scenario 7：事故

Prompt：

```text
Customers received duplicate replies after the provider retried webhook deliveries.
```

預期：

- 先 containment。
- Root cause 不停在「provider retried」。
- 加入 idempotency／dedup test／monitor／spec update。

## Scenario 8：不相關任務

Prompt：

```text
Explain what a vector database is.
```

預期：

- 不應啟動完整 SDD workflow。
- 不應建立 repository artifacts。

---

# 38. Appendix D：最終驗收簽核表

## Product

- [ ] Skill Pack 能清楚說明要解決的問題。
- [ ] 適用範圍涵蓋多種 AI 應用，而非單一產業。
- [ ] 小任務與高風險任務有不同流程重量。

## Agent Skills

- [ ] 所有 Skills 通過格式驗證。
- [ ] Description trigger tests 通過。
- [ ] Core Skills 無責任重疊或衝突。
- [ ] References 採 on-demand loading。

## SDD

- [ ] Greenfield 流程可執行。
- [ ] Brownfield change 流程可執行。
- [ ] Incident loop 可執行。
- [ ] Traceability 可產生。
- [ ] Spec drift 可被偵測或警告。

## Production AI

- [ ] Model／Prompt／RAG／Tool／Data contracts 齊全。
- [ ] Reliability review 包含 async、retry、idempotency、concurrency。
- [ ] AI eval 可執行且有固定 fixtures。
- [ ] Human oversight 不是模糊建議，而是明確契約。

## Cross-agent

- [ ] Codex repo install 通過。
- [ ] Claude Code project install 通過。
- [ ] Windows／WSL2 流程通過。
- [ ] Canonical source 與 adapters 無 drift。

## Enforcement

- [ ] Secret scan 可阻擋測試洩漏。
- [ ] Verification gate 可在失敗時要求 Agent 繼續修正。
- [ ] Hooks 不會對每次操作造成不可接受延遲。
- [ ] 所有 Hook 均可單獨測試。

## Documentation

- [ ] 繁體中文 README 完成。
- [ ] 英文 README 或核心使用說明完成。
- [ ] 三種以上完整 walkthrough 完成。
- [ ] Troubleshooting 涵蓋 Skill 不觸發、過度觸發、路徑、權限與 Hook 問題。

## Release decision

- [ ] PASS
- [ ] CONDITIONAL PASS
- [ ] FAIL

簽核人：  
日期：  
條件／備註：

