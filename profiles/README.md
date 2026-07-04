# Project Profiles

Profiles are **incremental overlays** for specific AI project types (Master Spec sec. 11). They are
*not* always-loaded skills. Apply a profile on top of the core SDD workflow when your system matches
its "Apply when" clause. Stack- and vendor-specific details live in profiles and `examples/`, never
in canonical skills.

| Profile | Apply when |
|---|---|
| [conversational-ai](conversational-ai.md) | Multi-turn chat, messaging channels, outbound messages |
| [rag-knowledge-system](rag-knowledge-system.md) | Retrieval-grounded answers, ingestion, citations |
| [agent-tool-use](agent-tool-use.md) | LLM calls tools with real side effects |
| [workflow-automation](workflow-automation.md) | Logic in n8n / low-code exported workflows |
| [generative-content](generative-content.md) | Publishable content generation |
| [realtime-voice](realtime-voice.md) | Streaming audio / spoken conversation |
| [document-intelligence](document-intelligence.md) | Document extraction / understanding |
| [ml-inference-service](ml-inference-service.md) | Serving versioned trained models |
| [multi-tenant-ai-saas](multi-tenant-ai-saas.md) | Multiple isolated tenants on shared infra |

Each profile lists additional risk/requirement focus, SDD adjustments (which requirement kinds,
contracts, and reviews to add), a checklist, and common anti-patterns.
