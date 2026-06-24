# CLAUDE.md - Environmental Impact Assessment (EIA) Report Automation

**Skill slug:** `eia-report-automation`
**Source idea:** #183 (Vietnamese backlog `ideas.md`)
**Cluster:** legal-compliance - Legal, Compliance & Governance
**Tagline:** Draft and score EIA reports for small/medium projects against regulatory and scientific standards.
**Current phase:** Phase 5 complete - all phases 100% done, production-ready.

## Problem This Skill Solves
Small and medium projects need EIA reports but lack the expertise to identify significant impacts, structure the assessment, and meet regulatory technical standards, risking rejection. This skill structures an EIA from a project description, screens and scores impacts against assessment methodologies, checks regulatory compliance, and continuously updates technical standards and biodiversity data.

## Harness Flow (Summary)
1. **Intake** -> `sub-requirements-gatherer` gathers inputs and frames the problem.
2. **Screen / select** -> `sub-risk-screener` selects the governing framework and screens risk/scope.
3. **Score / analyze** -> `sub-compliance-check` produces a multi-dimensional score against named frameworks.
4. **Knowledge refresh** -> optional `tools/knowledge_updater.py` run keeps SECOND-KNOWLEDGE-BRAIN.md current.
5. **Gate** -> quality / safety/compliance gates must pass.
6. **Synthesize** -> main harness emits the scored deliverable + prioritized improvement roadmap.

## Sub-skills
- `skills/sub-requirements-gatherer.md` - Capture the project scope, location, activities, and the applicable EIA regulatory regime.
- `skills/sub-risk-screener.md` - Screen and score environmental impacts (air, water, soil, biodiversity, social) for significance.
- `skills/sub-compliance-check.md` - Verify regulatory completeness and gate the report behind a 'requires licensed-expert review' disclaimer.
- `skills/sub-standards-updater.md` - Refresh national technical regulations, emission/discharge limits, and local biodiversity data.
- `skills/sub-improvement-roadmap.md` - Produce a mitigation and monitoring plan ordered by the mitigation hierarchy and impact significance.

## Tools Required
WebSearch, WebFetch, Read, Write, Bash

## Knowledge Sources (for crawl + reasoning)
- IFC Performance Standards & Equator Principles (ifc.org)
- IAIA (International Association for Impact Assessment) best practice
- National EIA regulations and technical guidelines
- IUCN Red List & protected-area databases (iucnredlist.org, protectedplanet.net)
- Google Scholar for environmental-impact research

## Supporting Python Tools
- `tools/knowledge_updater.py` - crawl4ai + WebSearch pipeline that fetches latest papers/reports from the domain sources above, scores by recency + relevance + source tier, deduplicates by URL/DOI hash, and appends to `SECOND-KNOWLEDGE-BRAIN.md`. Recommended schedule: weekly cron.

## Active Development Tasks
- [x] Scaffold all required deliverables
- [x] Define >=3 sub-skills with quality gates
- [x] Ground scoring in named world-renowned frameworks
- [x] Wire knowledge_updater crawl sources
- [x] Expand SECOND-KNOWLEDGE-BRAIN with seed references
- [x] Add regression fixtures from the test scenarios
- [x] Cross-skill wiring and shared schema
- [x] Mark all phases 100% done

## Reference Docs (this folder)
- `PROJECT-detail.md` - full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` - phase roadmap (all phases complete)
- `SECOND-KNOWLEDGE-BRAIN.md` - self-improving knowledge base
- `skills/main.md` - harness entry point
- `schema/shared-eia-schema.json` - canonical input/output schema
- `CROSS-SKILL-WIRING.md` - cluster reuse guide