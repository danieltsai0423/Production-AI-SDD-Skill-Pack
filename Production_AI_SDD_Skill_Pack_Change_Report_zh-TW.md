# Production AI SDD Skill Pack 變更報告

回應文件：`Production_AI_SDD_Skill_Pack_Review_Report_zh-TW.md`
日期：2026-07-02
版本：pack 0.1.0（明確標示尚非 Master Spec production-grade v1.0）

## 摘要

逐項驗證審查報告後，先做出 Accept／Partially accept／Reject 判定，再依優先順序修改。
本輪聚焦「可在此回合完成並可驗證」的高價值項目；大型建置項目（hooks 全套、live-agent
評估、profiles/examples/references、source synthesis）明確標為追蹤中的後續工作，而非佯稱完成。

一項關鍵事實查核：審查報告中的「mojibake／亂碼」（M-004、L-003）並非檔案損毀。經 Python
以 UTF-8 解碼所有檔案皆成功；亂碼是**閱讀端**在 Windows cp950（Big5）主控台顯示 UTF-8 標點
（如 `↔`、`—`、`→`）所致。實際的 console 錯誤 `cp950 can't encode ↔` 即為證據。因此
「檔案損毀」的說法 Reject；但底層的跨工具穩健性顧慮成立，故已把英文／結構檔中的非 ASCII 標點
正規化為 ASCII。

## 逐項判定

| ID | 判定 | 理由與處置 |
|---|---|---|
| C-001 交付範圍不足 | Partially accept | 相對於完整 Master Spec 屬實，但「核心 Skills」為使用者明確範圍且對應 MVP（sec. 31）。處置：誠實標示成熟度、補入最高價值可執行檔，其餘列追蹤。 |
| C-002 缺 deterministic enforcement | Partially accept | 正確且重要。處置：新增 `scan_secrets.py`、`validate_specs.py`、擴充 `validate_skills.py`、CI；完整 hook 矩陣列追蹤。 |
| C-003 觸發正確性無法證明 | Partially accept | 合理。處置：新增 `evals/trigger/cases.yaml`（Appendix C 8 場景）與 `run_trigger_evals.py` 靜態檢查；live precision/recall 誠實列為追蹤，不佯裝。 |
| C-004 跨代理僅文件宣稱 | Partially accept | 處置：新增複製式 `install.py`（manifest + dry-run，跨 OS）。hash drift check／plugin packaging 列追蹤。 |
| C-005 安全／評估／測試閘門缺失 | Partially accept | 同 C-002；已補 secret scan 與 CI。完整 eval 套件列追蹤。 |
| H-001 缺 contract templates | Accept | 已補 `templates/contracts/` 共 9 份。 |
| H-002 SDD templates 不完整 | Accept | 已補 brief、spec-delta、decision-record、incident-report、project-constitution。 |
| H-003 validator 覆蓋不足 | Accept | 已擴充：broken link／referenced file、duplicate name、unsafe hardcoded path、non-ASCII 警告。 |
| H-004 Level 1 與 tasking 觸發矛盾 | Accept | 真實矛盾。已改 `pai-sdd-tasking` description 與內文，明訂 Level 1 直接由 light spec 出任務、Level 2-3 由 plan 出任務。 |
| H-005 README 過度宣稱 | Accept | 已弱化「enforceable gates」措辭，並改寫 Status 誠實列出已含／未含項目。 |
| M-001 skill 責任重疊 | Partially accept | description 原已委派而非重複；已為最易混淆的配對加上「Boundary with related skills」說明（verify↔release-readiness、architecture↔reliability）。 |
| M-002 缺 profile 隔離 | Accept，延後 | 有效但屬大型工作；審查報告本身列於最後步驟。已建立追蹤說明。 |
| M-003 場景覆蓋不足 | Accept，延後 | 需 `profiles/`／`references/`；延後。 |
| M-004 檔案亂碼 | Reject（就字面）／Partially accept（底層） | 檔案為合法 UTF-8（已證明），無損毀。已將英文／結構檔標點 ASCII 正規化以提升 Windows 穩健性。 |
| M-005 缺 source-synthesis 產物 | Accept，延後 | 需先萃取 `.docx` SOP，工作量大；延後。 |
| L-001 pack.yaml metadata 偏少 | Partially accept | 已補 repository／homepage／supported_agents／install 區塊，並將 version 由 1.0.0 下修為 0.1.0。 |
| L-002 compatibility 文字泛用 | Reject（本輪不改） | 審查者亦承認符合格式；屬未來 adapter 階段建議，非缺陷。 |
| L-003 README 標點亂碼 | Partially accept | 同 M-004，已由正規化修復。 |
| L-004 skills 皆 < 500 行 | 正向觀察 | 無需處置。 |

## 已做的變更

### 技能措辭與邊界
- `skills/pai-sdd-tasking/SKILL.md`：修正 description 與內文的 Level 1／plan 矛盾（H-004）。
- `skills/pai-sdd-verify/SKILL.md`、`skills/pai-ai-architecture-review/SKILL.md`：新增「Boundary with related skills」（M-001）。
- 全部英文／結構檔：標點 ASCII 正規化（`—→↔·§` 與 box-drawing → ASCII）（M-004／L-003）。

### 模板（H-001、H-002）
- `templates/contracts/`：ai-behavior、model-prompt、data、rag、tool、human-oversight、reliability、evaluation、observability（共 9 份）。
- `templates/`：brief、spec-delta、decision-record、incident-report、project-constitution（共 5 份）。

### 可執行檔與閘門（H-003、C-002/3/4/5）
- `scripts/validate_skills.py`：擴充 broken link／referenced file／duplicate name／hardcoded path／non-ASCII 檢查，區分 error 與 warning，新增 `--strict`。
- `scripts/scan_secrets.py`：優先包裝 gitleaks／detect-secrets，缺工具時採 stdlib fallback 並標示限制。
- `scripts/validate_specs.py`：驗證 spec frontmatter、requirement IDs、Level 對應產物；無 specs/ 時 graceful pass。
- `scripts/install.py`：複製式安裝到 `.agents/skills`／`.claude/skills`，含 manifest 與 `--dry-run`。
- `evals/trigger/cases.yaml` + `scripts/run_trigger_evals.py`：Appendix C 8 場景 + 靜態一致性與 keyword smoke。
- `.github/workflows/validate.yml`：CI 串接以上所有閘門。

### 文件與 metadata（H-005、L-001、broken link）
- `README.md`：弱化宣稱、改寫 Status、更新 Install／Validate／Layout。
- `README.zh-TW.md`：新增（修復 README 的斷連結）。
- `pack.yaml`：version → 0.1.0、新增 maturity／repository／supported_agents／install。

## 驗證結果

```text
python scripts/validate_skills.py     -> PASS: 17 skill(s) valid (0 warning(s))
python scripts/validate_specs.py      -> PASS: no specs/ directory yet
python scripts/run_trigger_evals.py   -> PASS: 8 trigger case(s) well-formed and consistent
python scripts/scan_secrets.py        -> PASS: no secrets (stdlib fallback)
python scripts/install.py --dry-run   -> PASS: dry-run for codex + claude
residual non-ASCII punctuation audit  -> NONE
```

觸發評估的 keyword-smoke 多數顯示 `weak`：這是誠實結果，反映 description 用語（如
「asynchronous events」）與 prompt 用語（如「webhook」）不同。此為靜態訊號，不作為失敗條件；
真正的觸發 precision/recall 需 live-agent 執行，已列追蹤。

## 仍未完成（追蹤中，對應審查報告）

- Codex／Claude hooks（PreToolUse／pre-commit／Stop）與 spec-required／verification／spec-drift gate 的 hook 佈線（C-002）。
- 完整 output-quality／workflow-compliance evals 與 live-agent precision/recall 門檻、fixtures（C-003、C-005）。
- JSON schemas（spec/task/eval/manifest/change）。
- `profiles/`（9 種 AI 系統類型）、`references/`、`examples/`、`docs/`（M-002、M-003）。
- hash 式 adapter drift check 與 plugin packaging（C-004）。
- 來自 SOP 的 `workbench/source-analysis/` source-synthesis 產物（M-005）。

## Release 判定

沿用審查報告：以完整 Master Spec Definition of Done（sec. 25）衡量仍為 **未達 v1.0**。
本輪將專案由「核心草稿」提升為**具初步強制力的核心技能包（pack 0.1.0）**，並已誠實對外標示成熟度。
