.PHONY: help install install-hooks validate evals gate hooks-test sync dist clean

help:
	@echo "Targets:"
	@echo "  install        Install skills into Codex + Claude adapter paths (repo scope)"
	@echo "  install-hooks  Install git pre-commit + Claude settings hooks"
	@echo "  validate       Run schema/skill/spec/reference validators"
	@echo "  evals          Run trigger/workflow/output/safety eval suites (static)"
	@echo "  hooks-test     Run the hook tests"
	@echo "  gate           Run the full quality gate (standard mode)"
	@echo "  sync           Re-sync adapter copies from canonical skills/"
	@echo "  dist           Build the distribution archive"
	@echo "  clean          Remove build/adapter/generated artifacts"

install:
	python scripts/install.py --targets codex claude --scope repo

install-hooks:
	python scripts/install_hooks.py

validate:
	python scripts/_minijsonschema.py
	python scripts/validate_skills.py
	python scripts/validate_specs.py
	python scripts/validate_references.py

evals:
	python scripts/run_trigger_evals.py
	python scripts/run_workflow_evals.py
	python scripts/run_output_evals.py
	python scripts/run_safety_evals.py

hooks-test:
	python scripts/test_hooks.py

gate:
	python scripts/run_quality_gate.py --mode standard

sync:
	python scripts/sync_skills.py --check

dist:
	python scripts/build_distribution.py

clean:
	rm -rf dist .agents/skills .claude/skills .pai-sdd-install-manifest.json
