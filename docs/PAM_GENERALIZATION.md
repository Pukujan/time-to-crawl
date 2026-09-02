# Frozen PAM v0.2 unseen-project generalization check

This branch applies the already-frozen Project Assurance Modules revision to `Pukujan/time-to-crawl` as an **unseen project compatibility/generalization check**. It does not modify PAM, add PAM as a runtime dependency, restart the Research Assurance retrospective, or run a model benchmark.

## Identities and independence boundary

Unseen project baseline:

- repository: `Pukujan/time-to-crawl`
- baseline branch: `main`
- exact baseline commit: `f8e7c39bed2b7a25263e6abe06017e8d035bcad0`
- baseline GitHub Actions run: `32228987637` (`ci`, successful)

Frozen methodology:

- repository: `Pukujan/project-assurance-modules`
- exact revision: `a10ad56b7088c1e101e80914a9e00357dbef9120`
- freeze ref: `freeze/v0.2-bounded-extractions`

Before selecting this target, repository search found no `time-to-crawl` reference in `project-assurance-modules`, `RA-plugin`, or `research-assurance`. The project was therefore not used to design the v0.2 extraction cluster.

This is generalization evidence about whether the frozen schemas/profiles/modules can describe a materially different project without bespoke methodology edits. It is **not** a causal A/B benchmark and must not be reported as one.

## Existing project authority remains authoritative

`time-to-crawl` already has its own strong assurance model:

- GitHub issues #1–#17 and `ARCHITECTURE.md` define architecture and execution gates;
- `AGENTS.md` says conversational memory is not authority and requires live GitHub reconciliation before mutation;
- `contracts/properties/ttc-properties-v1.json` binds semantic properties to owners, executable oracles, mutation scope, holdout flags, and formal references;
- `.github/workflows/ci.yml` runs the current deterministic repository lane;
- `docs/HANDOFF_CURRENT.md` is an existing human-readable snapshot, explicitly subordinate to live GitHub state.

PAM does not replace those artifacts. `HANDOFF_STATE.json` is only a generic machine-readable current-state companion. The pre-existing prose handoff and exact historical commits/issues remain project-native context.

## Declared facts and frozen routing

Observed project facts select all four frozen profiles:

- `projectization.software@0.1.0`
- `continuity.material-work@0.1.0`
- `benchmark.empirical-work@0.1.0`
- `provenance.material-decisions@0.1.0`

The resulting seven modules are all routed `required` from explicit facts, not manually promoted:

- `projectization.build-vs-reuse@0.1.0`
- `projectization.scope-boundary@0.1.0`
- `continuity.structured-handoff@0.1.0`
- `planning.foundation@0.1.0`
- `engineering.swe-ci-foundation@0.1.0`
- `benchmark.integrity@0.1.0`
- `provenance.decision-lineage@0.1.0`

`durable_provenance_and_decision_lineage` is deliberately declared `false`: the project has strong **data/evidence provenance**, but that is not automatically the same thing as a complete project-decision-lineage system. The provenance profile is selected because consequential architecture/security/engine decisions exist.

## Strong pre-existing matches

### Build vs reuse

Issues #1 and #8 already embody the reuse-before-build rule. The serious engine candidates are Crawlee and Scrapy. The project also records explicit narrower roles/dispositions for Nutch (defer unless large distributed batch is proven necessary), Browsertrix (optional high-fidelity archive adapter), Crawl4AI (optional isolated extraction adapter), and Firecrawl (optional provider/self-host adapter, not foundational).

The existing matched bakeoff design compares more than throughput: correctness, observability, recovery, security mediation, adapter simplicity, retries, robots behavior, resource use, dependency footprint/SBOM/license, browser integration, and isolation compatibility. The **actual matched Crawlee-vs-Scrapy bakeoff is still pending**, so empirical probe evidence and final engine disposition remain open rather than being inferred from planning prose.

### Scope and planning

The project already has unusually explicit scope gates: no unrestricted live crawling before issue #4 isolation; no custom crawler unless issue #8 documents a concrete gap; profiles cannot grant authority; and multiple optional mechanisms are explicitly deferred. Architecture ownership and dependency direction are frozen in `ARCHITECTURE.md` and agent rules.

The machine-readable property catalog is strong invariant evidence. However, PAM's `planning.foundation` asks for a consolidated failure register rather than failure knowledge scattered across security issues, properties, tests, and prose. No equivalent consolidated failure register was found at the frozen baseline, so `PLAN_FOUNDATION_004` remains pending.

### SWE/CI

The project documents a reproducible Python install/test path, has executable tests, and has a green CI run at the exact baseline revision. Its ordinary lane is fixture-only and does not depend on live Web crawling.

Ruff is configured in `pyproject.toml`, but the current CI workflow does not run Ruff (and no explicit rationale was found for omitting an ecosystem-appropriate static-quality check). `SWE_CI_002` therefore remains pending instead of treating test-only CI as complete static quality.

### Benchmark/holdout integrity

The project has a good public/private boundary: the property catalog flags holdout-sensitive properties, `src/ttc/assurance/holdout.py` exposes only a sealed/not-configured aggregate interface, and tests verify private cases are not exposed. Issues #3, #4, and #8 also define hidden/adversarial evaluation roles.

The real engine bakeoff and private holdout suite are not configured at the baseline. Exact first-campaign protocol/data identities, a deterministic hidden-package leakage scan/review receipt, and durable empirical result artifacts are therefore still pending under `BENCH_INT_002`, `BENCH_INT_004`, and `BENCH_INT_005`.

### Decision lineage

`AGENTS.md`, semantic property IDs, issue authority, and exact commits provide useful lineage primitives, while `ARCHITECTURE.md` correctly keeps live operational truth separate from optional FOSSIL learned knowledge.

What remains weaker is a portable record that binds consequential accepted decisions to exact supporting identities and makes proposed/accepted/superseded authority status explicit. `PROV_LINEAGE_002` and `PROV_LINEAGE_003` remain pending. No external FOSSIL ingest/promotion is claimed, so `PROV_LINEAGE_005` is explicitly N/A rather than fabricated from file existence.

## Generic handoff finding

The baseline already has `docs/HANDOFF_CURRENT.md`, but it is prose-only and records head `c9dd125` while the live baseline is `f8e7c39...`. This is not treated as a project error because the file explicitly says it is a snapshot and live GitHub remains authority. It is, however, a clean example of why PAM's generic machine-readable current packet and deterministic reconciliation rule are useful across projects.

On this branch:

- `HANDOFF_STATE.json` is replaceable current resumable state;
- `docs/HANDOFF_CURRENT.md` remains project-native historical/contextual state;
- exact commits/issues/CI runs are durable historical identities;
- live GitHub wins when any stored snapshot is stale.

## No-bespoke-edit rule

Any exact-PAM validation incompatibility discovered here must be classified as one of:

1. a generic PAM defect for a **future** methodology revision;
2. an explicit project/domain N/A allowed by the frozen module contract;
3. a genuine `time-to-crawl` pending/blocked requirement.

The frozen revision `a10ad56b7088c1e101e80914a9e00357dbef9120` must not be changed to make this unseen project pass.

## Next gate

Run the branch's exact-revision PAM workflow. It must detached-fetch and verify the frozen SHA, validate `PROJECT_ASSURANCE.json`, `HANDOFF_STATE.json`, and `PAM_BOOTSTRAP.json`, and verify that manifest dispositions equal the frozen router output for the declared facts.

A successful run establishes **schema/routing/contract portability to this unseen project**. It does not establish that every project requirement is complete and it does not authorize live crawling or a new model benchmark.
