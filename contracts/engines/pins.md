# Engine pins (not selected)

Issue #8 owns the Crawlee vs Scrapy bakeoff. These are **candidate pins**, not an architecture decision.

Do not install these into the default extra. Domain/application must not import them.

| Engine | Candidate pin | Role |
| --- | --- | --- |
| crawlee | `crawlee>=0.6,<1` | HTTP + Playwright composition candidate |
| scrapy | `scrapy>=2.12,<3` | mature baseline |
| warcio | `warcio>=1.7,<2` | optional WARC adapter |
| zstandard | `zstandard>=0.23,<1` | already in core for evidence codec |

Live adapters remain `UnavailableEngine` until #4 isolation passes.
