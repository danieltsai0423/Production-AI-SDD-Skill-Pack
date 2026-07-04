# Production AI SDD Skill Pack（繁體中文）

> 為 Codex、Claude Code 及相容 Agent Skills 的工具，提供規格驅動的工作流程、生產級架構審查、
> AI 契約、評估、可靠性閘門與人類控制模式。

English: [README.md](README.md)

## 這是什麼

一套可跨代理重複使用的 [Agent Skills](https://agentskills.io) 技能包，把真實的生產級 AI 工程判斷
轉換為**可觸發的程序與可重複的模板**，並搭配逐步擴充的**確定性閘門**（目前為多個 validator、
secret scan 與 spec 檢查；hooks 與 CI 持續擴充）。它設計為讓同一套 canonical skills 同時在
**Codex** 與 **Claude Code** 上運作，並採用**依風險分級的 Spec-Driven Development（SDD）**生命週期：
小修改保持輕量，高風險 AI 行為則需契約、評估、人工審查與回滾。

> **成熟度：** 核心 skills + 模板 + 初步 validator/gates。尚未達到 Master Spec 定義的
> production-grade v1.0（詳見下方「狀態」）。

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
python scripts/validate_skills.py     # 格式、參照、重複名稱、硬編路徑、非 ASCII
python scripts/validate_specs.py      # specs/ 下的規格（尚無規格時為 no-op）
python scripts/run_trigger_evals.py   # 觸發案例：schema + 參照 + 關鍵字 smoke（靜態）
python scripts/run_workflow_evals.py  # workflow 案例：routing + artifact + gate contract smoke（靜態）
python scripts/scan_secrets.py        # 有 gitleaks/detect-secrets 則優先使用，否則採 stdlib fallback
```

## 狀態

**本次已包含：** 17 個核心 skills、SDD 與契約模板、複製式安裝器、擴充後的 skill validator、
spec validator、secret 掃描、靜態 trigger/workflow 評估骨架與 CI。

**尚未實作（追蹤中）：** Codex/Claude hooks、含 live-agent 評分與 precision/recall 門檻的完整
output/workflow 評估、JSON schemas、fixtures、各 AI 系統類型的 `profiles/` 與 `references/`、
`examples/`、`docs/`、hash 式 adapter drift check，以及來自 SOP 的 source-synthesis 產物。

本專案為**具初步強制力的核心技能包**，尚非 Master Spec Definition of Done（sec. 25）所定義的
production-grade v1.0。

## 授權

MIT - 見 [LICENSE](LICENSE)。
