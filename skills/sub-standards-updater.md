---
name: sub-standards-updater
description: Refresh national technical regulations, emission/discharge limits, and local biodiversity data.
parent: eia-report-automation
---

## Role
Sub-skill of `eia-report-automation`. Refresh the technical standards that apply to the project: emission and discharge limits, protected-area and biodiversity designations, and any recent regulatory changes.

## Inputs
Outputs from prior stages, especially `project_profile.jurisdiction`, `project_profile.location`, and `dimension_scores`.

## Procedure
1. **Check brain freshness.** Read `SECOND-KNOWLEDGE-BRAIN.md` and note the most recent update date.
2. **Determine relevant standards.** Based on jurisdiction and scored dimensions, identify applicable standards:
   - air emissions (e.g., national ambient air quality standards);
   - wastewater/effluent discharge limits;
   - noise limits;
   - soil contamination thresholds;
   - protected-area and species lists (IUCN Red List, Protected Planet).
3. **Search authoritative sources.** Use WebSearch/WebFetch for the latest official regulation, IFC standards, IUCN lists, and protected-area databases. Prefer primary sources.
4. **Extract and normalize.** Record the standard name, parameter, limit value, unit, effective date, source URL, and applicability to the project.
5. **Compare to project emissions/loads.** If project-specific discharge/emission estimates are available, compare to limits and flag exceedances.
6. **Record limitations.** If a source cannot be reached, note the limitation and use the most recent cached value from the brain.
7. **Self-check against the Quality Gate.**

## Outputs
A JSON object:

```json
{
  "brain_last_updated": "YYYY-MM-DD",
  "standards_snapshot": [
    {"theme": "air | water | soil | noise | biodiversity", "parameter": "string",
     "limit_value": "string", "unit": "string", "effective_date": "YYYY-MM-DD",
     "source": "citation", "applicable": true, "exceedance_risk": "yes | no | unknown"}
  ],
  "protected_area_triggers": [
    {"name": "string", "designation": "string", "distance_km": number, "source": "citation"}
  ],
  "species_triggers": [
    {"scientific_name": "string", "common_name": "string", "iucn_status": "string", "source": "citation"}
  ],
  "regulatory_changes": [
    {"date": "YYYY-MM-DD", "description": "string", "source": "citation"}
  ],
  "refresh_needed": true,
  "limitations": ["string"],
  "evidence": ["citation"],
  "quality_gate_passed": true
}
```

## Tools
WebSearch, WebFetch, Read, Write, Bash

## Quality Gate
- Every limit or designation cites an authoritative source.
- If a source is unreachable, the limitation is explicit and a cached value is used.
- `refresh_needed` is set based on brain age and data gaps.
- No invented numeric limits; if unknown, mark `exceedance_risk` as `unknown`.
