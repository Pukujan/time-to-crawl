# Time to Crawl architecture

Authority: GitHub issues #1–#17. This file is the in-repo freeze of ownership and dependency direction.

Time to Crawl is a **general-purpose, policy-bounded acquisition + extraction platform**. Products/deals are one profile, not the core.

## Ownership

| Plane | Owns |
| --- | --- |
| Crawler engine | Request execution mechanics only. Never source authority, durable knowledge, or privileged actions |
| Policy broker | Destination authorization, robots/access policy, budgets, network class, redirects, capabilities |
| PostgreSQL | Operational crawl/run/source state and generic typed observations/history |
| pgvector | Optional similarity/candidate generation. Similarity is never identity truth |
| Evidence store | Immutable artifacts plus provenance. WARC/WACZ when archival fidelity is justified |
| FOSSIL | Selected durable learned knowledge/lineage. Not every crawl row |
| Graphiti/Neo4j | Rebuildable knowledge projection, not the operational crawler database |
| Profiles | What to extract and how to query it. Profiles do not receive network or secret authority |
| Agents | Stable API/MCP only. No crawler/browser/database/object-store credentials |

Internet content is untrusted data, never instructions. Third-party crawler frameworks are execution dependencies, not trusted policy engines.

## Dependency direction

```text
domain -> application -> ports <- adapters
                         ^
                   api / mcp / profiles
```

Forbidden in `ttc.domain` and `ttc.application`: Crawlee, Scrapy, Playwright, Browsertrix, Crawl4AI, Firecrawl, SearXNG, Apache Tika, psycopg, pgvector, FOSSIL internals, Graphiti, Neo4j, harness SDKs.

## Minimum ports

See `contracts/architecture/module-map.json`.

- `CrawlerEnginePort`
- `DiscoveryProviderPort`
- `PolicyDecisionPort`
- `EvidenceStorePort`
- `ContentExtractorPort`
- `IdentityResolverPort`
- `OperationalCatalogPort`
- `ProfileRegistryPort`
- `KnowledgePort`
- `QueryViewPort`

Do not build a generic crawler engine. Issue #8 is a Crawlee-vs-Scrapy bakeoff behind `CrawlerEnginePort`. A custom crawler is forbidden unless that bakeoff documents a concrete gap.

## Profiles

A versioned profile is data/config with JSON Schema validation. It must not contain arbitrary executable Python/JS, shell, browser scripts, or plugin imports. Profiles may *request* capabilities; they cannot grant them. Policy Broker (#4) decides.

Reference profiles: `products-and-offers`, `jobs`, plus later legal-documents or inference-providers.

## Two scheduler loops

- **DISCOVER**: unseen domains/URLs/documents/records.
- **REFRESH**: revisit known resources per profile freshness. Engine URL-dedup never means `known URL = never revisit`.

## Walking skeleton

```text
explicit seed
 -> policy/robots check
 -> crawler-engine fake/adapter
 -> provenance-preserving evidence
 -> schema profile extracts typed rows
 -> persist catalog
 -> query as JSON/table through API
```

Then a second materially different profile through the **same** engine/domain path.

## Discovery adapters (later, issue #6)

Port: `DiscoveryProviderPort`. Planned adapters: SearXNG, Tavily, Exa. Brave if a key appears. Live keys never enter this repository.
