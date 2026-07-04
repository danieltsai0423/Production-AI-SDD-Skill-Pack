# Production AI SDD Skill Pack（繁體中文）

> 為 Codex、Claude Code 及相容 Agent Skills 的工具，提供規格驅動的工作流程、生產級架構審查、
> AI 契約、評估、可靠性閘門與人類控制模式。

English: [README.md](README.md)

## 這是什麼

一套可跨代理重複使用的 [Agent Skills](https://agentskills.io) 技能包，把真實的生產級 AI 工程判斷
轉換為**可觸發的程序與可重複的模板**，並搭配**確定性閘門**（schema 驗證的產物、多個 validator、
secret 掃描、五道 enforcement hooks 與 CI）。同一套 canonical skills 同時在 **Codex** 與
**Claude Code** 上運作，並採用**依風險分級的 Spec-Driven Development（SDD）**生命週期：小修改保持
輕量，高風險 AI 行為則需契約、評估、人工審查與回滾。

> **成熟度：** production-grade v1.0 —— 已達 Master Spec Definition of Done（sec. 25）。唯一追蹤中的
> 後續工作是 live-agent 的 precision/recall 與校準式 prose 評分；目前 eval runner 已確定性地驗證
> 結構與佈線（詳見下方「狀態」）。

完整產品規格與驗收契約：[`Production_AI_SDD_Skill_Pack_Master_Spec_zh-TW.md`](Production_AI_SDD_Skill_Pack_Master_Spec_zh-TW.md)。

## 核心 Skills（v1）

| Skill | 職責 |
|---|---|
| `pai-sdd-orchestrator` | 以正確的重量，將需求導向正確的 SDD 步驟。 |
| `pai-sdd-discovery` | 在寫程式前分類工作型態、風險（Level 0-3）、範圍與既有證據。 |
| `pai-sdd-specify` | 把模糊需求轉為可測試、與解法解耦的規格。 |
| `pai-sdd-clarify` | 釐清會影響架構、風險或驗收的模糊處。 |
| `pai-sdd-plan` | 把確認後的規格轉為架構、契約、資料流、測試與上線計畫。 |
| `pai-sdd-tasking` | 把計畫拆成可獨立實作、可驗證、可回滾的任務。 |
| `pai-sdd-implement` | 在單一任務邊界內實作最小正確變更。 |
| `pai-sdd-verify` | 以可重現的證據證明實作符合規格。 |
| `pai-sdd-change` | 管理 brownfield 的需求／架構變更與 spec delta。 |
| `pai-sdd-close` | 收斂規格、證據、文件與營運交接。 |
| `pai-ai-architecture-review` | 審查 AI 元件邊界、資料／狀態、故障隔離與擴展性。 |
| `pai-ai-contracts` | 撰寫 AI 行為／模型-提示／資料／RAG／工具／人類監督契約。 |
| `pai-reliability-review` | 審查事件、佇列、冪等、重試、順序、並行與復原。 |
| `pai-security-privacy-review` | 審查 AI 特有與一般安全隱私，含 prompt injection。 |
| `pai-ai-evaluation` | 為非確定性 AI 建立可重複、可比較、可回歸的評估。 |
| `pai-release-readiness` | 從功能、可靠性、安全、資料、AI 品質與營運面把關上線。 |
| `pai-incident-postmortem` | 把事故轉為永久的預防、偵測與復原改善。 |

## 安裝（repo scope）

```bash
python scripts/install.py --targets codex claude --scope repo
python scripts/install.py --targets claude --scope user --dry-run
```

採複製策略，可在 Windows、WSL2、macOS 與 Linux 上運作，並寫入安裝 manifest。

## 驗證

```bash
python scripts/run_quality_gate.py --mode standard   # 一次跑完以下全部 + drift，單一 exit code
```

或個別執行：`validate_skills`、`validate_specs`、`validate_references`、`run_trigger_evals`、
`run_workflow_evals`、`run_output_evals`、`run_safety_evals`、`test_hooks`、`scan_secrets`。

## 狀態

**v1.0 已包含：** 17 個核心 skills、9 個 project profiles、SDD 與 9 份契約模板、6 個接進 validator
的 JSON schemas、複製式安裝器／hooks 安裝器／adapter drift check／uninstall／distribution builder、
五道確定性 enforcement hooks（含測試）、trigger/workflow/output/safety 評估套件與 0-4 rubric 與四組
fixtures、四個實走 examples（真實產物）、十一份 docs（含 Windows/WSL2）、來自 SOP 的 Phase 0
knowledge-extraction，以及 validate/evals/release CI。

**追蹤中的後續工作：** live-agent 的 trigger precision/recall 與校準式 0-4 prose 評分。eval runner
已確定性地驗證結構、佈線與安全；live 評分 harness 是最後一步，且刻意不佯裝完成。

本版本已達 Master Spec Definition of Done（sec. 25）。

## 授權

MIT - 見 [LICENSE](LICENSE)。
