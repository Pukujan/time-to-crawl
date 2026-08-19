# Changelog

Unreleased work is on `main`. Architecture authority remains issues #1–#17.

## 0.1.0-fixture

- Walking skeleton for four profiles
- PolicyBroker, CAS/WARC, scheduler TLA+, fake bakeoff
- Live crawlee/scrapy/search/firecrawl/browsertrix fail closed until #4
- Source Registry can gate PolicyBroker
- Redirect loops, hop budgets, and five-hop cap fail closed
- MIME/body match, 403/404, empty-body, and secret-header redaction fail closed
- Lease TTL fencing in Python and TLA+
- Provenance records robots_compliant; status reports robots on / anti_block off
- Skeleton mints RunReceipt; CLI prints receipt_id
- ClockPort/FrozenClock; fixture-only `ttc soak`
