# Handoff — 2026-08-19 overnight

Authority remains GitHub issues #1–#17. This is a snapshot, not architecture truth.

## Head

`3ca8095` on `main`. `pytest`: 129 passed, 1 xfailed (DNS rebinding until #4 resolver policy).

## Landed (fixture / fake only)

- #2 ports, import boundaries, walking skeleton
- #3 property catalog, Hypothesis fuzz, sealed holdout interface, Scheduler.tla, mutmut.toml
- #4 PolicyBroker network/capability/robots + WorkerEnvelope (no Podman/gVisor runtime yet)
- #5 CAS, Zstd, WARC prototype, S3-shaped memory object store
- #6 source registry + sitemap/feed parsers (candidates unauthorized)
- #7 DISCOVER/REFRESH, durable JSON scheduler, evidence-before-success, simulated 24-cycle soak, freshness windows
- #8 fake bakeoff harness + UnavailableEngine fail-closed placeholders
- #9 JSON + HTML JSON-LD + plaintext extractors
- #10 identity keys + change detection (embeddings ignored)
- #11 HistoryCatalog + SQLite catalog
- #12 four profiles: products, jobs, inference-providers, legal-documents
- #13 integrity inspect()
- #14 FossilStub + RebuildableGraph (cannot overwrite evidence)
- #15 BoundedGateway + MCP catalog + filter/sort
- #16 health probe + chaos restart + `ttc status`

Live crawlee/scrapy/search/firecrawl/browsertrix/playwright APIs fail closed. Tavily/Exa keys in desktop env are unused.

## Still blocked / open

- Real Podman/gVisor isolation and external egress (#4)
- Real Crawlee vs Scrapy bakeoff (#8) after #4
- Postgres + pgvector (#11/#10)
- Gravebuster 24/7 soak (#16/#17)
- Hidden holdout suite remains sealed/not configured
- No live autonomous crawl

## Next agent

Do not implement a custom crawler. Do not open live network. Prefer #4 isolation runtime or #8 adapter work behind UnavailableEngine until #4 passes.
