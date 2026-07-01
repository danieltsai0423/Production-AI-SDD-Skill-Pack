# Production AI SDD Skill Pack 審查報告

日期：2026-07-01

## 審查範圍

本報告根據以下來源審查目前 repository 的 Production AI SDD Skill Pack 實作：

- Master Spec：`Production_AI_SDD_Skill_Pack_Master_Spec_zh-TW.md`
- 原始完整 SOP：`AI 系統與自動化專案開發 SOP.docx`
- Agent Skills 格式要求：以 Master Spec 中的 Agent Skills 開放格式與 description 驗收規則為準
- Repository 現有實作：`skills/`、`templates/`、`scripts/`、`AGENTS.md`、`CLAUDE.md`、`README.md`、`pack.yaml`

本次審查未修改既有程式碼、Skill、template 或設定檔。

## 已執行驗證

```powershell
python scripts\validate_skills.py
```

結果：

```text
PASS: 17 skill(s) valid.
```

注意：此 validator 目前只代表基本格式檢查通過，不代表符合 Master Spec 的完整 Definition of Done。

## 總體結論

目前 repository 可視為「核心 Skill 初稿加上少量模板與基本 validator」，尚不能視為 Master Spec 定義的 production-grade Skill Pack。

現有 17 個 core skills 的方向大致正確，且多數內容已避免把醫美、Messenger、LINE、n8n、FastAPI、Redis 等專案經驗寫死成唯一架構。但 repo 缺少 installer、hooks、CI、schema validation、spec validation、eval runners、fixtures、security gates、contract templates、profiles、examples 與跨代理 drift check，因此目前大量規則仍停留在 Markdown/prompt 層，無法被穩定驗證或強制執行。

## Critical

### C-001：v1 交付範圍嚴重不足

Master Spec 要求最終交付至少包含：

- 核心 Skills、references、assets、scripts
- Codex 與 Claude Code 的 Hooks / 設定範例
- SDD 規格模板、變更模板、驗證模板、事故模板
- Skill trigger evals、output quality evals、workflow compliance evals
- CI workflow、lint、schema validation、unit tests
- Release checklist 與驗收報告

現有 repo 只有：

- `skills/`
- `templates/`
- `scripts/validate_skills.py`
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `pack.yaml`

缺少 Master Spec 目標樹中的 `references/`、`assets/`、`profiles/`、`hooks/`、`evals/`、`schemas/`、`examples/`、`docs/`、`.agents/`、`.claude/`、`.codex/`、`.github/` 等主要交付物。

影響：

- 無法證明 Skill Pack 完整符合 Master Spec。
- 無法支援可重複安裝、可測試觸發、可驗證輸出品質或可阻擋高風險變更。
- README 宣稱的 production-grade gates 目前沒有實作支撐。

### C-002：deterministic enforcement 幾乎缺席

Master Spec 明確區分：

- Skills / instructions：提供建議性工作程序。
- Scripts / CI / Hooks：負責必須確定執行的規則。

目前 repo 缺少以下 gate：

- Secret and sensitive data guard
- Protected file guard
- Spec required gate
- Verification gate
- Spec drift gate
- CI quality gate

影響：

- 「不得暴露 secrets / PII」、「Level 3 必須有人審、eval、rollback」、「不得無 spec 修改外部訊息行為」等規則，目前主要依賴 agent 自覺遵守。
- 對高風險 AI 行為來說，這是不可接受的完成狀態。

### C-003：description trigger 無法證明正確

現有 `validate_skills.py` 對 description 的檢查只有簡單 heuristic：

- 長度是否太短
- 是否包含 `Use`
- 是否包含 `Do not`

但 Master Spec 要求：

- trigger eval cases
- output quality eval cases
- workflow compliance evals
- trigger precision / recall 達到門檻
- should-trigger / should-not-trigger 場景

目前 repo 沒有 `evals/`、沒有 trigger eval runner，也沒有 fixtures。

影響：

- 無法證明 `pai-sdd-orchestrator`、`pai-sdd-discovery`、`pai-sdd-plan`、`pai-ai-contracts` 等 skill 在真實 prompt 下會被正確觸發。
- 無法量化 skill 責任邊界是否清楚。
- validator PASS 容易造成 false confidence。

### C-004：Codex 與 Claude Code 支援目前只是文件宣稱

README 寫明安裝方式是手動 copy / symlink，且 cross-agent installer 是 planned follow-up。

Master Spec 要求：

- Codex repo scope 安裝可被發現
- Claude Code project scope 安裝可被發現
- installer / sync strategy
- install manifest
- `.agents/skills`、`.claude/skills` 與 canonical source hash drift check
- Codex / Claude adapter 或 plugin package

目前缺少：

- `scripts/install.py`
- `scripts/sync_skills.py`
- `.agents/skills`
- `.claude/skills`
- `.codex/hooks`
- `.claude/hooks`
- generated adapter drift check

影響：

- 無法驗證「同一 canonical skill source 同時供 Codex 與 Claude Code 使用」。
- Windows / WSL2 copy strategy 沒有自動化。
- 長期容易產生 Codex 與 Claude Code 版本漂移。

### C-005：安全、Evals、測試閘門缺失

Master Spec 將 tests、AI evals、release gate、安全隱私、rollback、人類 oversight 視為 Level 2/3 AI 系統的必要完成條件。

目前缺少：

- `scan_secrets.py`
- `validate_specs.py`
- `check_spec_drift.py`
- `run_quality_gate.py`
- `run_trigger_evals.py`
- `run_output_evals.py`
- `run_workflow_evals.py`
- eval schemas
- eval fixtures
- CI workflow
- unit tests

影響：

- 無法阻擋 secrets、PII、正式資料 fixture 被提交或放入 prompts/logs。
- 無法驗證 prompt/model/RAG/tool schema 變更是否跑過 regression eval。
- 無法驗證 release readiness 是否只是文字填寫。

## High

### H-001：Contract templates 缺失

`pai-ai-contracts` 要求輸出以下 contract：

- AI Behavior Contract
- Model / Prompt Contract
- Data Contract
- RAG Contract
- Tool Contract
- Human Oversight Contract

Master Spec 另列出 reliability、evaluation、observability contract。

目前 `templates/contracts/` 不存在。

影響：

- `pai-ai-contracts` 雖然要求「one file per applicable contract」，但 agent 沒有標準模板可用。
- 高風險 AI 行為很容易退回自然語言 prompt rule，而不是 versioned contract。

### H-002：SDD templates 不完整

現有 templates：

- `spec.md`
- `clarifications.md`
- `plan.md`
- `tasks.md`
- `verification.md`
- `change-proposal.md`

Master Spec 目標樹另要求：

- `project-constitution.md`
- `brief.md`
- `spec-delta.md`
- `decision-record.md`
- `incident-report.md`
- `templates/contracts/*`

影響：

- Level 2 / Level 3 的 artifact set 不完整。
- Brownfield、incident、ADR、contract-driven planning 無法被一致執行。

### H-003：`validate_skills.py` 覆蓋不足

現有 validator 檢查：

- skill dir 是否有 `SKILL.md`
- frontmatter 是否有 required fields
- name 是否等於 directory name
- description 是否有基本 what/when/not heuristic
- 行數是否小於 500
- `pack.yaml` skill list 是否一致

Master Spec 要求 validator 還需檢查：

- frontmatter schema
- description trigger boundary
- broken relative links
- missing referenced files
- duplicate skill names
- unsafe hardcoded path
- tool-specific metadata validity
- token warning

影響：

- 目前 validator PASS 不足以支持 release gate。
- `SKILL.md` references 指向不存在 template 或 section 時無法被攔截。

### H-004：Level 1 workflow 與 `pai-sdd-tasking` trigger 有矛盾

`pai-sdd-orchestrator` 定義：

- Level 1：specify -> tasking -> implement -> verify

但 `pai-sdd-tasking` description 寫：

- Use after `pai-sdd-plan` for Level 1-3 work.

問題：

- Level 1 是否必須產生 `plan.md` 不清楚。
- 如果 Level 1 不跑 plan，`pai-sdd-tasking` 的 trigger 條件會和 orchestrator 衝突。

影響：

- Agent 可能對 Level 1 小功能產生不必要 ceremony。
- 或相反地，因為沒有 plan 而不觸發 tasking。

### H-005：README 與實作狀態不一致

README 將此 pack 描述為：

- triggerable procedures
- repeatable templates
- enforceable gates
- runs same canonical skills on both Codex and Claude Code

但實作上：

- enforceable gates 尚未存在。
- installer 尚未存在。
- eval runner 尚未存在。
- README 也在 Status 裡說 profiles、hooks、eval runners、fixtures、cross-agent installer 是 planned follow-ups。

影響：

- 對使用者來說，目前 README 的產品定位容易被理解為已完成。
- 應明確標示目前是 scaffold / core skill draft，而非完整 production-grade release。

## Medium

### M-001：Skill 責任邊界大致合理，但仍有重疊

主要重疊點：

- `pai-sdd-orchestrator` 與 `pai-sdd-discovery` 都負責 routing / Level 判斷。
- `pai-sdd-plan` 會 select and run domain reviews，但 review skills 本身也有 planning trigger。
- `pai-sdd-verify` 和 `pai-release-readiness` 都涉及 evidence / gate。
- `pai-ai-architecture-review` 與 `pai-reliability-review` 都會檢查 async、idempotency、external events。
- `pai-ai-contracts` 與 `pai-security-privacy-review` 都會觸及 tool permissions、人類核准、audit。

建議責任切分：

- `pai-sdd-orchestrator`：只做生命周期路由。
- `pai-sdd-discovery`：只做 work type / risk / artifact classification。
- `pai-sdd-plan`：只選擇需要哪些 review，不直接取代 review。
- domain review skills：只產出 findings、blocking risks、mitigations。
- `pai-sdd-verify`：驗證 implementation 是否符合 spec。
- `pai-release-readiness`：只做 deploy go/no-go。

### M-002：沒有明顯過度綁定醫美、Messenger、LINE、n8n，但缺少 profile 隔離

審查結果：

- 核心 Skills 中沒有把醫美、Messenger、LINE、n8n 當作唯一架構。
- `n8n / low-code` 只作為 anti-pattern example，屬於可接受的 generalized lesson。
- `medical` 主要出現在 Level 3 風險分類，屬於風險例子，不是硬綁定。

問題：

- Master Spec 要求把特定 clinic wording、domain-specific communication policy 放入 profile overlay 或 private asset。
- 目前 repo 沒有 `profiles/`，也沒有 examples / private overlay strategy。

影響：

- 雖然 core skills 暫時通用，但缺少正式機制隔離 project-specific SOP 內容。

### M-003：通用 AI 系統架構方向正確，但場景覆蓋不足

Master Spec 要求支援或提供 profiles / references 給多種 AI system types：

- Conversational AI
- RAG / Knowledge System
- Agent Tool Use
- Workflow Automation / Low-code
- Generative Content
- Realtime Voice
- Document Intelligence
- ML Inference Service
- Multi-tenant AI SaaS

現有 repo 沒有 `references/` 或 `profiles/`。

影響：

- 核心 skills 可以通用，但缺少不同 AI 應用場景的 on-demand guidance。
- 實務使用時 agent 仍可能回到泛泛而談，或把 SOP 例子套成單一架構。

### M-004：多處文件與模板出現 mojibake / 亂碼

觀察到亂碼位置：

- `README.md`
- `CLAUDE.md`
- `templates/spec.md`
- `templates/plan.md`
- `templates/tasks.md`
- Master Spec 部分段落

影響：

- Claude Code / Codex 讀取時可能誤解指令、章節或符號。
- 中文使用者文件品質不足。
- Template 產出的 artifact 可能直接帶入亂碼。

### M-005：原始 SOP 的 reusable lessons 尚未形成 source synthesis artifact

Master Spec Appendix B 要求 source synthesis 產出：

- `reusable-patterns.md`
- `project-specific-patterns.md`
- `incidents-and-lessons.md`
- `conflicts-and-open-questions.md`
- `privacy-redaction-report.md`
- `source-to-skill-mapping.md`

目前 repo 沒有 `workbench/source-analysis/` 或等價文件。

影響：

- 無法追蹤哪些 SOP lesson 被通用化、哪些被判定為 project-specific。
- 無法證明醫美/LINE/Messenger/n8n 經驗已被正確 generalize。

## Low

### L-001：`pack.yaml` 基本合理，但缺少更完整 package metadata

現有 `pack.yaml` 已列出 17 個 skills，與目錄一致。

可補強：

- repository URL
- docs URL
- supported agents
- install mode
- checksum / release metadata
- generated adapter manifest location

### L-002：每個 skill 的 compatibility 文字過於泛用

目前所有 skill 都使用類似：

```text
Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
```

這符合基本格式，但資訊量有限。

若未來加入 tool-specific metadata，應把 Codex / Claude 差異放 adapter，不要混入 core skill。

### L-003：README 的中文連結與 Methodology 文字有亂碼

README 中有：

- 中文 README link 亂碼
- `Spec?Code consistency` 亂碼
- `MIT ??see LICENSE` 亂碼

影響較低，但會降低可信度與可讀性。

### L-004：現有 skills 都在 500 行內，適合作為 core draft

這是正向觀察：

- 17 個 skill 都有 frontmatter。
- skill name 與 directory name 一致。
- description 大多包含 what / when / do-not-use。
- skills 沒有明顯一個檔案過度膨脹。

但仍需補 eval 與 enforcement 才能達到 production-grade。

## 針對使用者指定問題的直接回答

### 是否遺漏規格

是，且屬於 Critical。

主要遺漏：

- references
- assets
- profiles
- hooks
- evals
- schemas
- installer / sync scripts
- quality gates
- CI
- contract templates
- examples
- docs
- source synthesis artifacts

### Skills 是否責任重疊

有中度重疊。

重疊不致命，但需要明確 handoff 和 owner boundary，尤其是 orchestrator / discovery / plan / verify / release-readiness 之間。

### description 是否能正確觸發

目前無法證明。

description 形式大致合格，但缺少 trigger evals、should-trigger / should-not-trigger fixtures、precision / recall 門檻。

### 是否過度綁定醫美、Messenger、LINE 或 n8n

目前核心 skills 沒有明顯過度綁定。

但 repo 缺少 `profiles/`，所以還沒有正式機制把 domain-specific 內容隔離成 overlay / example / private asset。

### 是否真正通用於 AI 系統架構與應用專案

方向上是，但完成度不足。

核心 skills 的語言大多通用；但缺少 profiles、references、examples、contract templates、eval fixtures，導致不同 AI system type 的可操作性不足。

### Scripts、Hooks、Skills 的責任是否混淆

目前主要問題不是混淆，而是 scripts/hooks 缺席。

Skills 內寫了許多應該由 scripts/hooks/CI enforcement 的規則，但實作上沒有對應 gate。

### Claude Code 與 Codex 是否都能使用

目前只能說理論上可手動 copy 使用，不能說已可驗證支援。

缺少 installer、adapter、generated path、hash drift check、Codex/Claude fixture test。

### 是否有無法驗證或過度依賴提示詞的規則

有。

高風險要求、secret / PII 防護、spec-required gate、verification gate、eval regression、human oversight 等目前多靠 Markdown 指令，而不是 executable enforcement。

### 是否缺少測試、Evals 或安全閘門

是，且屬於 Critical。

目前沒有 eval runner、fixtures、CI、secret scan、spec validator、verification gate、security gate 測試。

## 建議修正順序

### 1. 先定義 v1 最小可驗收範圍

不要一次追完整 Master Spec。

建議先把 v1 定義為：

- 17 個 core skills 可安裝
- description trigger 可被 smoke eval 驗證
- templates 與 references 不缺檔
- basic quality gate 可跑
- Codex / Claude Code repo-scope install 可測

### 2. 修復 encoding / mojibake

優先修：

- README
- CLAUDE
- templates
- Master Spec 顯示亂碼段落

理由：

- 這是所有 agent 後續讀取與執行的基礎。

### 3. 補 installer / sync / drift check

新增：

- `scripts/install.py`
- `scripts/sync_skills.py`
- install manifest
- `.agents/skills` dry-run
- `.claude/skills` dry-run
- canonical source hash drift check

### 4. 擴充 validators

優先擴充 `validate_skills.py` 或拆出：

- frontmatter schema validation
- broken link validation
- referenced file existence
- unsafe hardcoded path detection
- duplicate skill name detection
- description trigger boundary checks
- tool-specific metadata validation

### 5. 補 trigger evals 與 output/workflow smoke evals

先用 Master Spec Appendix C 的 8 個人工驗收 scenarios 做最小 eval suite：

- 極小修改
- 低風險 AI 摘要功能
- 外部 Webhook AI 處理
- RAG 模型 / 索引變更
- 高風險 Agent 工具
- 需求變更
- 事故
- 不相關概念解釋

### 6. 補 hooks / quality gates

先做最小可執行版本：

- secret scan
- spec required gate
- verification gate
- spec drift gate

每個 gate 都要能單獨測試。

### 7. 補 contract templates、schemas、incident/report templates

補齊：

- `templates/contracts/ai-behavior-contract.md`
- `templates/contracts/model-prompt-contract.md`
- `templates/contracts/data-contract.md`
- `templates/contracts/rag-contract.md`
- `templates/contracts/tool-contract.md`
- `templates/contracts/human-oversight-contract.md`
- `templates/contracts/reliability-contract.md`
- `templates/contracts/evaluation-contract.md`
- `templates/contracts/observability-contract.md`
- `templates/brief.md`
- `templates/spec-delta.md`
- `templates/decision-record.md`
- `templates/incident-report.md`

### 8. 修正 Skill handoff 與 Level 1 tasking 矛盾

明確定義：

- Level 1 是否允許 `tasks.md` without `plan.md`
- `pai-sdd-tasking` 的 trigger 是否應改成「after plan or Level 1 light spec」
- `pai-sdd-plan` 是否只 select reviews，而不是暗示直接執行所有 review

### 9. 補 profiles / examples / references

最後再補：

- Conversational AI
- RAG
- tool-using agent
- workflow automation / low-code
- generative content
- realtime voice
- document intelligence
- ML inference service
- multi-tenant AI SaaS

同時把醫美、Messenger、LINE、n8n 經驗放到 examples/profile，而不是 core rules。

## 建議 release 判定

目前判定：`FAIL`

理由：

- core skill draft 存在，但 Master Spec 的 enforcement、eval、installer、contract templates、cross-agent verification 都尚未完成。
- 目前不應標示為 production-grade v1.0 完成品。

可接受的短期標示：

```text
Status: Core skill draft / scaffold
Not yet production-grade
Missing installer, hooks, evals, gates, CI, profiles, contract templates
```
