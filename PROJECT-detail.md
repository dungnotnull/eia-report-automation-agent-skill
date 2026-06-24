# PROJECT-detail.md — Environmental Impact Assessment (EIA) Report Automation

## Executive Summary
This skill is a full Claude harness that turns draft and score EIA reports for small/medium projects against regulatory and scientific standards. It operates research-first: every material judgment is grounded in a named, citable framework and, where possible, a freshly retrieved source. It produces a professional-grade deliverable: a multi-dimensional score against the chosen framework plus a prioritized, effort/impact-ranked improvement roadmap.

## Problem Statement
Small and medium projects need EIA reports but lack the expertise to identify significant impacts, structure the assessment, and meet regulatory technical standards, risking rejection. This skill structures an EIA from a project description, screens and scores impacts against assessment methodologies, checks regulatory compliance, and continuously updates technical standards and biodiversity data.

## Target Users & Use Cases
Primary users are practitioners and decision-makers in the **Legal, Compliance & Governance** domain. Trigger examples:
1. A small factory project needs an EIA; skill structures the report and screens significant impacts.
2. Project sits near a protected area; risk screener flags biodiversity significance and offset needs.
3. Wastewater discharge may exceed limits; skill applies the mitigation hierarchy and standards.
4. User asks the skill to 'approve' the project; compliance gate forces a licensed-expert-review disclaimer.
5. Regulation updates discharge limits; standards-updater revises the compliance section.
6. Skill outputs an impact-significance matrix plus a monitoring plan for the operations phase.

## Harness Architecture
```
/eia-report-automation (main.md harness)
  -> sub-requirements-gatherer              [intake / framing]
  -> sub-risk-screener              [framework selection / risk-scope screen]
  -> knowledge refresh   [SECOND-KNOWLEDGE-BRAIN via knowledge_updater.py]
  -> sub-compliance-check              [multi-dimensional scoring]
  -> COMPLIANCE/SAFETY GATE  [mandatory before output]
  -> improvement roadmap [prioritized, effort/impact]
  -> SYNTHESIZE          [final scored deliverable]
```

## Full Sub-Skill Catalog
### sub-requirements-gatherer
- **Purpose:** Capture the project scope, location, activities, and the applicable EIA regulatory regime.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-risk-screener
- **Purpose:** Screen and score environmental impacts (air, water, soil, biodiversity, social) for significance.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-compliance-check
- **Purpose:** Verify regulatory completeness and gate the report behind a 'requires licensed-expert review' disclaimer.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-standards-updater
- **Purpose:** Refresh national technical regulations, emission/discharge limits, and local biodiversity data.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-improvement-roadmap
- **Purpose:** Produce a mitigation and monitoring plan ordered by the mitigation hierarchy and impact significance.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.

## Skill File Format Specification
Every skill file uses YAML frontmatter (`name`, `description`) followed by the required sections: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates. The main harness invokes sub-skills via the Skill tool in the order shown above.

## E2E Execution Flow
1. Parse the user request; if inputs are insufficient, `sub-requirements-gatherer` asks targeted intake questions.
2. `sub-risk-screener` selects the governing framework(s) and screens scope/risk; branch to a refusal or disclaimer if out of scope.
3. Refresh knowledge if the brain is stale (>7 days) and WebSearch/WebFetch are available; otherwise degrade gracefully to internal knowledge with a stated limitation.
4. `sub-compliance-check` scores each dimension, citing evidence per claim.
5. Run the safety/compliance gate(s) and a devil's-advocate challenge pass.
6. Emit the scored report + roadmap in the Output Format below.

## SECOND-KNOWLEDGE-BRAIN Integration
- **Sources:** IFC Performance Standards & Equator Principles (ifc.org); IAIA (International Association for Impact Assessment) best practice; National EIA regulations and technical guidelines; IUCN Red List & protected-area databases (iucnredlist.org, protectedplanet.net); Google Scholar for environmental-impact research
- **Crawl config:** see `tools/knowledge_updater.py` (ArXiv categories physics.geo-ph, q-bio.PE; domain queries seeded from the idea).
- **Append format:** date-stamped entries with Title, Authors, Year, Venue, DOI/URL, key finding, relevance note; deduplicated by URL/DOI hash.

## Supporting Tools Spec — knowledge_updater.py
- **Inputs:** search queries + source list (in-file config), optional `--since` date.
- **Outputs:** appended entries in `SECOND-KNOWLEDGE-BRAIN.md` + a run log.
- **Schedule:** weekly cron (graceful no-op when offline).

## Quality Gates
- **Compliance gate (mandatory):** run `sub-compliance-check` before emitting the final deliverable; attach a jurisdiction/disclaimer notice and recommend a qualified professional.
- **Evidence gate:** every material claim is traceable to a cited source or a prior step; prefer the highest evidence tier available.
- **Framework gate:** all scoring is grounded in the named frameworks below — never ad-hoc criteria.
- **Challenge gate:** a devil's-advocate pass has stress-tested the recommendation before it is shown.

## Test Scenarios
See `tests/test-scenarios.md` (>=5 concrete scenarios with expected harness behavior).

## Key Design Decisions
1. Framework-grounded scoring only — no ad-hoc rubrics.
2. Research-first with graceful degradation when offline.
3. Composable sub-skills (>=3) so cluster siblings can reuse them.
4. Deliverable is an artifact (scored report + roadmap), not a chat reply.
5. Safety/compliance gate enforced before any sensitive/regulated output.
