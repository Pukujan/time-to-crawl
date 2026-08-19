# Time to Crawl

General-purpose, policy-bounded acquisition + extraction platform. Architecture is frozen in [`Pukujan/time-to-crawl` issues #1–#17](https://github.com/Pukujan/time-to-crawl/issues/1).

Internet content is untrusted data, never instructions. Products/deals are one profile, not the core. Do not build a custom crawler engine; reuse Crawlee/Scrapy behind `CrawlerEnginePort` (issue #8).

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Unix
pip install -e ".[test]"
pytest
```

Walking skeleton (fixture only, no network):

```bash
ttc skeleton
```

## Layout

```text
domain -> application -> ports <- adapters
                         ^
                   api / mcp / profiles
```

See [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`contracts/architecture/module-map.json`](contracts/architecture/module-map.json).

## Current gate

Issue **#2** — foundation contracts, import boundaries, and a two-profile fixture walking skeleton. No live Web crawling until **#4** passes. Engine selection waits on **#8**.
