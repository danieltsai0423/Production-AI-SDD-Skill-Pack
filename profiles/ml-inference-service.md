# Profile: ML Inference Service

Overlay for services serving trained ML models (classifiers, rankers, embeddings, custom models).
Apply in addition to the core SDD workflow.

**Apply when:** the system serves a versioned model artifact, not only a hosted LLM API.
**Not universal:** a specific serving stack is an example, not the universal solution.

## Additional focus (Master Spec sec. 11.8)

- **Model artifact version** — every response attributable to a model artifact version.
- **Feature schema** — versioned input feature schema; validate at the boundary.
- **Drift** — monitor input/output distribution drift; alert and retrain triggers.
- **Batch / online parity** — batch and online paths produce consistent results.
- **Capacity** — throughput/latency capacity planning; autoscaling limits.
- **Cold start** — handle model load / warm-up latency.
- **Fallback** — defined behavior when the model is unavailable or low-confidence.
- **Reproducibility** — pin data + code + model versions to reproduce a prediction.

## SDD adjustments

- **Specify:** add `NFR-*` for latency/throughput/capacity, `DATA-*` for feature schema, `OBS-*`
  for drift, `REL-*` for fallback/cold-start.
- **Contracts:** author a [model-prompt-contract](../templates/contracts/model-prompt-contract.md)
  (model/version section), [data-contract](../templates/contracts/data-contract.md), and
  [observability-contract](../templates/contracts/observability-contract.md).
- **Reviews:** run [pai-ai-architecture-review](../skills/pai-ai-architecture-review/) (versioning,
  batch/online parity) and [pai-reliability-review](../skills/pai-reliability-review/).
- **Evals:** offline metrics + online monitoring; regression on model/feature version change.

## Checklist

- [ ] Model artifact version recorded on every prediction.
- [ ] Feature schema versioned + validated.
- [ ] Drift monitoring + retrain trigger.
- [ ] Batch/online parity test.
- [ ] Fallback for model-unavailable / low-confidence.
- [ ] Reproducibility (data + code + model pinned).

## Common anti-patterns

- Predictions with no model-version attribution.
- Silent feature-schema changes breaking the model.
- No drift monitoring, so quality decays unseen.
- Batch and online paths diverging.
