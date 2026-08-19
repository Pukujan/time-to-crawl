# Time to Crawl — agent contract

Parent tracker: GitHub issue #1. This file is the in-repo definition of done for coding agents.

## Authority

- Architecture lives in issues #1–#17, `ARCHITECTURE.md`, and `contracts/`.
- Conversational memory is not authority. Re-read live GitHub + this file before mutating.
- No live autonomous Web crawling until issue #4 (Policy Broker + isolation) passes.
- Fixture/fake work is allowed now.
- Do not implement a custom generic crawler/queue/browser pool. Issue #8 owns the engine bakeoff.

## Dependency direction

```text
domain -> application -> ports <- adapters
                         ^
                   api / mcp / profiles
```

- `ttc.domain` imports only the stdlib and itself.
- `ttc.ports` import only stdlib + `ttc.domain`.
- `ttc.application` imports stdlib + `ttc.domain` + `ttc.ports`.
- `ttc.adapters` implement ports; they do not import other adapters' internals.
- Domain/application must not import Crawlee, Scrapy, Playwright, Browsertrix, Crawl4AI, Firecrawl, SearXNG, Tika, psycopg, pgvector, FOSSIL internals, Graphiti, Neo4j, or a harness SDK.

`pytest tests/test_import_boundaries.py` is the mechanical check.

## Product model is a profile

Core records are generic: `Profile`, `Evidence`, `TypedRecord`. `products-and-offers` is one profile. Jobs, legal documents, and custom schemas must use the same acquisition path.

Profiles are validated data. They cannot grant capabilities or ship executable code.

## Walking skeleton

Prove this thin path before expanding engines/providers:

```text
authorized seed
 -> PolicyDecisionPort
 -> CrawlerEnginePort (fake)
 -> immutable evidence
 -> profile-driven typed records
 -> resolve identity
 -> persist catalog
 -> query API
```

Then a second profile with a different schema **without changing crawler-engine/domain code**.

## Assurance

Issue #3 owns the property catalog at `contracts/properties/ttc-properties-v1.json`. Semantic PRs must name affected IDs:

- `TTC-NET-001` / `TTC-NET-002`
- `TTC-AUTH-001` / `TTC-AUTH-002`
- `TTC-PROV-001` / `TTC-PROV-002`
- `TTC-ENGINE-001`
- `TTC-SCHED-001` / `TTC-SCHED-002`
- `TTC-PROFILE-001` / `TTC-PROFILE-002`
- `TTC-ID-001`
- `TTC-KNOW-001`
- `TTC-EVID-001`
- `TTC-DEAL-001`

Do not skip or weaken tests to obtain green. Model prose is not completion authority.
