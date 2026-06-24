
# CROSS-SKILL-WIRING.md - Legal, Compliance & Governance Cluster

## Purpose
This document defines how the `eia-report-automation` skill shares its sub-skills, schemas, and quality gates with sibling skills in the `legal-compliance` cluster.

## Shared Sub-Skills
The following sub-skills are designed to be reused by any cluster sibling that needs structured, evidence-linked compliance assessment:

- `skills/sub-requirements-gatherer.md` - intake validation and regime selection.
- `skills/sub-compliance-check.md` - regulatory completeness checklist and disclaimer enforcement.
- `skills/sub-improvement-roadmap.md` - prioritized action plan with mitigation hierarchy.

## Shared Schema
- `schema/shared-eia-schema.json` defines the canonical input and output shapes.
- Sibling skills should import/extend this schema rather than redefine fields.

## Shared Quality Gates
All cluster siblings are encouraged to implement these gates:

- **COMPLIANCE GATE** - mandatory professional-review disclaimer before regulated output.
- **EVIDENCE GATE** - every material claim cites a source.
- **FRAMEWORK GATE** - scores derive from named, citable frameworks.
- **CHALLENGE GATE** - devil's-advocate review of high-stakes claims.

## Reuse Patterns
1. **Copy-by-reference:** sibling skills invoke `sub-requirements-gatherer` and `sub-compliance-check` directly.
2. **Schema extension:** add domain-specific fields under `provided` but keep the top-level output shape.
3. **Knowledge base sharing:** keep `SECOND-KNOWLEDGE-BRAIN.md` and `tools/knowledge_updater.py` in a shared cluster folder for consistent standards updates.

## Anti-Patterns
- Do not duplicate the compliance disclaimer text; import it from `sub-compliance-check`.
- Do not invent ad-hoc scoring rubrics; ground every dimension in a named framework.
- Do not bypass the COMPLIANCE GATE for regulated advice.
