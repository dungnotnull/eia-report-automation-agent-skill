# EIA Report Automation Agent Skill

<p align="center">
  <img src="https://img.shields.io/badge/cluster-legal--compliance-blue" alt="Cluster">
  <img src="https://img.shields.io/badge/status-production--ready-success" alt="Status">
  <img src="https://img.shields.io/badge/open--source-ready-brightgreen" alt="Open Source">
  <img src="https://img.shields.io/badge/phase-5%2F5%20complete-success" alt="Phase">
</p>

<p align="center"><b>Draft, score, and improve Environmental Impact Assessment (EIA) reports for small/medium projects using named, citable frameworks.</b></p>

---

## What is this?

This repository contains a complete **Claude agent skill** for automating the first pass of an EIA report. It is designed for practitioners in the **Legal, Compliance & Governance** domain who need a structured, transparent, and reproducible way to:

- Screen projects for environmental and social significance.
- Score impacts using internationally recognized frameworks.
- Check regulatory completeness against jurisdictional requirements.
- Build a prioritized mitigation and monitoring roadmap.
- Continuously refresh technical standards and biodiversity data.

Every output is **framework-grounded**, **evidence-linked**, and carries a **mandatory licensed-professional disclaimer**. It never pretends to be binding regulatory approval.

---

## Problem it Solves

Small and medium projects often need an EIA but lack the budget or in-house expertise to structure the assessment, identify significant impacts, and meet technical regulatory standards. Manual drafting is slow, inconsistent, and prone to missing critical receptors or compliance gaps. This skill automates the heavy lifting while leaving final authority to qualified human professionals.

---

## Core Design Principles

1. **Framework-grounded scoring**  every dimension is scored against a named, citable framework; no ad-hoc rubrics.
2. **Evidence-first**  every material claim cites a source or prior step; prefer the highest evidence tier available.
3. **Research-first**  use live search, WebFetch, and a self-updating knowledge brain before falling back to internal knowledge.
4. **Safety/compliance gate**  no binding approval; a mandatory disclaimer is attached to every deliverable.
5. **Graceful degradation**  works offline with cached knowledge, clearly stating limitations.
6. **Composable sub-skills**  each stage is a reusable skill that sibling `legal-compliance` skills can invoke.

---

## Governing Frameworks

| # | Framework | Role in this skill |
|---|-----------|--------------------|
| 1 | **Leopold matrix** | Identify and rank action-environment interactions. |
| 2 | **Rapid Impact Assessment Matrix (RIAM)** | Compute impact significance as `(A+B) * (C+D)` with A-E bands. |
| 3 | **IFC Performance Standards** | Environmental and social risk screening and mitigation expectations. |
| 4 | **Equator Principles** | Baseline for large/international financed projects. |
| 5 | **EIA process stages** | Ensure screening, scoping, and impact-significance stages are followed. |
| 6 | **Mitigation hierarchy** | Order actions as avoid ? minimize ? restore ? offset. |
| 7 | **Baseline/cumulative-impact methodology** | Evaluate additive and cumulative effects. |
| 8 | **National EIA regulations + IUCN/WDPA** | Jurisdiction-specific thresholds and protected-area triggers. |

---

## Repository Structure

```
eia-report-automation/
 CLAUDE.md                              # Agent skill entry card
 PROJECT-detail.md                      # Full technical specification
 PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Phase roadmap (all phases 100% done)
 SECOND-KNOWLEDGE-BRAIN.md              # Self-improving knowledge base
 CROSS-SKILL-WIRING.md                  # Reuse guide for sibling skills
 README.md                              # This file
 skills/
    main.md                            # Harness entry point
    sub-requirements-gatherer.md       # Intake & project profile
    sub-risk-screener.md               # Leopold/RIAM impact scoring
    sub-compliance-check.md            # Regulatory checklist & disclaimer
    sub-standards-updater.md           # Standards & biodiversity refresh
    sub-improvement-roadmap.md         # Mitigation & monitoring plan
 schema/
    shared-eia-schema.json             # Canonical input/output JSON schema
 tests/
    test-scenarios.md                  # 6 scenario descriptions
    test_runner.py                     # Regression test runner
    fixtures/
      scenario_1.json                # Small factory EIA
      scenario_2.json                # Project near protected area
      scenario_3.json                # Wastewater discharge
      scenario_4.json                # User asks to approve
      scenario_5.json                # Regulation update
      scenario_6.json                # Quarry + monitoring plan
  tools/
  knowledge_updater.py               # Self-updating knowledge pipeline
```

---

## Harness Flow

```
User Request
    |
    v
[sub-requirements-gatherer]  Validate intake, build project profile
    |
    v
[sub-risk-screener]          Leopold matrix + RIAM scoring
    |
    v
[knowledge_updater.py]         Optional brain refresh if >7 days stale
    |
    v
[sub-compliance-check]       Regulatory checklist, disclaimer, approval block
    |
    v
[sub-standards-updater]      Refresh standards, protected areas, species
    |
    v
[sub-improvement-roadmap]    Prioritized mitigation + monitoring plan
    |
    v
Quality Gates (COMPLIANCE / EVIDENCE / FRAMEWORK / CHALLENGE / OUTPUT)
    |
    v
Final Scored Report + Roadmap (JSON-serializable artifact)
```

---

## Input Schema

```json
{
  "project_name": "ABC Garment Factory",
  "location": {
    "country": "VN",
    "region": "Binh Duong",
    "coordinates": {"lat": 10.9, "lon": 106.7}
  },
  "sector": "manufacturing",
  "scale": "small",
  "activities": ["cutting", "sewing", "washing", "boiler operation"],
  "jurisdiction": "Vietnam",
  "sensitive_receptors": [],
  "baseline_data": "",
  "goal": "draft EIA"
}
```

Supported scales: `small`, `medium`, `large`.
Supported sectors: manufacturing, hydropower, solar, wind, thermal_power, mining, quarry, road, rail, port, tourism, aquaculture, agriculture, urban_dev, waste, other.

---

## Output Schema

```json
{
  "executive_summary": {"verdict": "...", "headline_score": "..."},
  "inputs_and_assumptions": {"provided": {}, "assumed": [], "missing": []},
  "multi_dimensional_score": [
    {"dimension": "water", "score": "C", "framework": "RIAM", "evidence": [...], "confidence": "medium"}
  ],
  "findings": {"strengths": [], "risks": [], "gaps": []},
  "improvement_roadmap": [
    {"action": "...", "tier": "minimize", "effort": "medium", "impact": "high", "priority_rank": 1, "timeline": "...", "evidence": [...]}
  ],
  "sources_and_limitations": {"sources": [], "limitations": []},
  "disclaimer": "This deliverable is for screening and planning purposes only..."
}
```

---

## Quality Gates

The harness will block or downgrade the final output if any mandatory gate is not satisfied:

- **COMPLIANCE GATE**  disclaimer + licensed-professional recommendation required; blocks binding approval language.
- **EVIDENCE GATE**  every score, limit, or receptor claim must cite a source or prior step.
- **FRAMEWORK GATE**  every dimension must be scored against a named framework.
- **CHALLENGE GATE**  a devil's-advocate pass documents weakest evidence, most generous assumption, and largest residual risk.
- **OUTPUT GATE**  final artifact must contain all seven required sections with non-empty critical fields.

---

## Knowledge Updater

`tools/knowledge_updater.py` is a production-grade pipeline that:

- Fetches recent ArXiv papers (`physics.geo-ph`, `q-bio.PE`).
- Optionally calls a WebSearch endpoint or crawl4ai on authoritative domains (`iaia.org`, `ifc.org`, `iucnredlist.org`, `protectedplanet.net`).
- Scores entries by **recency  relevance  source tier**.
- Deduplicates by URL/DOI hash.
- Appends date-stamped rows to `SECOND-KNOWLEDGE-BRAIN.md`.
- Supports `--dry-run`, `--since YYYY-MM-DD`, `--max-results`, and structured JSONL logging.

### Example usage

```bash
# Validate the pipeline without modifying the brain
python tools/knowledge_updater.py --dry-run --since 2025-01-01

# Live update (requires network and optional WEB_SEARCH_ENDPOINT)
python tools/knowledge_updater.py --max-results 20
```

### Cron recommendation

```cron
0 2 * * 0 cd /path/to/repo && python tools/knowledge_updater.py --max-results 15
```

---

## Running Tests

```bash
python tests/test_runner.py
```

The runner validates:
- All required skill files exist and have Inputs, Outputs, and Quality Gate sections.
- `SECOND-KNOWLEDGE-BRAIN.md` is seeded with core frameworks and update log.
- `tools/knowledge_updater.py` is syntactically importable.
- `schema/shared-eia-schema.json` is valid JSON.
- All 6 scenario fixtures conform to the schema.

---

## Test Scenarios Covered

1. **Small factory EIA**  garment factory in Vietnam.
2. **Project near protected area**  solar farm near a Ramsar wetland.
3. **Wastewater discharge exceedance**  food-processing plant in Thailand.
4. **User asks to approve**  compliance gate blocks binding approval.
5. **Regulation update**  standards updater flags stale permits.
6. **Impact matrix + monitoring plan**  quarry expansion in Indonesia.

---

## Cross-Skill Reuse

This skill contributes reusable components to the `legal-compliance` cluster:

- Reusable sub-skills: `sub-requirements-gatherer`, `sub-compliance-check`, `sub-improvement-roadmap`.
- Shared schema: `schema/shared-eia-schema.json`.
- Shared patterns: evidence gate, framework gate, compliance gate, challenge gate.

See `CROSS-SKILL-WIRING.md` for integration patterns and anti-patterns.

---

## Safety & Ethics

- This tool **does not** grant project approval.
- Every deliverable carries a mandatory disclaimer recommending review by a qualified, licensed environmental professional.
- It is designed to augment human expertise, not replace it.
- All scoring is transparent and auditable against named frameworks.

---

## Roadmap to Open Source

All development phases are 100% complete:

- [x] Phase 0  Research & Skill Architecture
- [x] Phase 1  Core Sub-Skills
- [x] Phase 2  Main Harness + Quality Gates
- [x] Phase 3  SECOND-KNOWLEDGE-BRAIN Pipeline
- [x] Phase 4  Testing & Validation
- [x] Phase 5  Integration & Cross-Skill Wiring

The repository is production-ready and open-source-ready.

---

## License

MIT License: see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Frameworks and data sources referenced in this skill:
- Leopold matrix (Leopold et al., 1971)
- Rapid Impact Assessment Matrix (Pastakia, 1998)
- IFC Performance Standards (International Finance Corporation)
- Equator Principles (Equator Principles Association)
- IAIA Best Practice Principles
- IUCN Red List of Threatened Species
- World Database on Protected Areas (UNEP-WCMC & IUCN)

---

<p align="center"><i>Built for transparency, rigor, and responsible environmental decision-making.</i></p>
