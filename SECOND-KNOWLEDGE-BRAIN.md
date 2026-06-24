
# SECOND-KNOWLEDGE-BRAIN.md - Environmental Impact Assessment (EIA) Report Automation

> Self-improving domain knowledge base for the `eia-report-automation` skill. Grown continuously by `tools/knowledge_updater.py`.

## Core Concepts & Frameworks
- **Leopold matrix & Rapid Impact Assessment Matrix (RIAM) for impact significance**
- **IFC Performance Standards & Equator Principles environmental screening**
- **Screening / scoping / impact-significance EIA process stages**
- **Mitigation hierarchy (avoid, minimize, restore, offset)**
- **Baseline-data and cumulative-impact assessment methodology**
- **National EIA technical regulations and biodiversity/protected-area checks**

## Key Research Papers
| Title | Authors | Year | Venue | DOI/Link | Relevance |
|-------|---------|------|-------|----------|-----------|
| Environmental Impact Statement (EIS) and the Leopold matrix | Leopold, L.B. et al. | 1971 | U.S. Geological Survey | https://www.usgs.gov/ | Foundational action-environment impact ranking matrix. |
| The Rapid Impact Assessment Matrix (RIAM) | Pastakia, C.M.R. | 1998 | Impact Assessment and Project Appraisal | https://www.iaia.org/ | EIA scoping/significance scoring method: (A+B)*(C+D). |
| IFC Performance Standards on Environmental and Social Sustainability | International Finance Corporation | 2012 | IFC | https://www.ifc.org/ | Risk screening, stakeholder engagement, mitigation hierarchy. |
| Equator Principles III | Equator Principles Association | 2013 | Equator Principles | https://equator-principles.com/ | Financial-sector EIA baseline for large/international projects. |

| IUCN Red List of Threatened Species | IUCN | ongoing | IUCN Red List | https://www.iucnredlist.org/ | Authoritative species-status and extinction-risk data. |
| World Database on Protected Areas | UNEP-WCMC & IUCN | ongoing | Protected Planet | https://www.protectedplanet.net/ | Authoritative protected-area boundaries and designations. |
| IAIA Best Practice Principles | International Association for Impact Assessment | ongoing | IAIA | https://www.iaia.org/ | EIA process stages and quality-control guidance. |
| _seed_ | - | - | - | - | Foundational references for Legal, Compliance & Governance. |

## State-of-the-Art Methods & Tools
- Apply the frameworks above as the scoring backbone.
- Prefer the highest available evidence tier (Systematic Review > Meta-Analysis > RCT/benchmark > Cohort/field study > Expert opinion > Blog).
- Triangulate multiple sources before asserting a numeric score.

## Authoritative Data Sources
- IFC Performance Standards & Equator Principles (ifc.org)
- IAIA (International Association for Impact Assessment) best practice
- National EIA regulations and technical guidelines
- IUCN Red List & protected-area databases (iucnredlist.org, protectedplanet.net)
- Google Scholar for environmental-impact research

## Analytical Frameworks (Scoring Backbone)
The skill scores every deliverable against the named frameworks above; each scoring dimension cites the framework it derives from.

## Self-Update Protocol
- **Tool:** `tools/knowledge_updater.py`
- **ArXiv categories:** physics.geo-ph, q-bio.PE
- **Search queries:**
  - `environmental impact assessment methodology RIAM`
  - `cumulative impact assessment`
  - `mitigation hierarchy biodiversity offset`
  - `EIA regulatory standards update`
- **Domains:** iaia.org, ifc.org, iucnredlist.org, protectedplanet.net
- **Frequency:** weekly cron.
- **Append format:** date-stamped row in *Key Research Papers* + a *Knowledge Update Log* line; deduplicate by URL/DOI hash.

## Knowledge Update Log
- 2026-06-18 - Brain initialized with core frameworks and seed sources for `eia-report-automation`.
- 2026-06-24 - Seeded with real foundational references (Leopold matrix, RIAM, IFC PS, Equator Principles, IUCN, WDPA, IAIA).
