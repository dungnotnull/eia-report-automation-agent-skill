---
name: sub-requirements-gatherer
description: Capture the project scope, location, activities, and the applicable EIA regulatory regime.
parent: eia-report-automation
---

## Role
Sub-skill of `eia-report-automation`. Validate intake, capture the project profile, identify the governing regulatory regime, and build a structured, evidence-linked project dossier for downstream scoring.

## Inputs
A JSON object matching the parent skill Input Schema:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| project_name | string | yes | Human-readable name. |
| location.country | string | yes | ISO 3166-1 alpha-2 preferred; full name accepted. |
| location.region | string | no | Province/state. |
| location.coordinates | object | no | `{lat, lon}` WGS84. |
| sector | string | yes | One of: manufacturing, hydropower, solar, wind, thermal_power, mining, quarry, road, rail, port, tourism, aquaculture, agriculture, urban_dev, waste, other. |
| scale | string | yes | One of: small, medium, large. |
| activities | string[] | yes | Construction and operation activities. |
| jurisdiction | string | yes | National EIA regime or `IFC`/`Equator`. |
| sensitive_receptors | string[] | no | Protected areas, habitats, species, communities. |
| baseline_data | string | no | Existing data references. |
| regulatory_regime | string | no | Explicit regime if known. |
| goal | string | no | User's stated goal. |

## Procedure
1. **Validate required fields.** If any required field is absent or unusable, ask a targeted clarification question and stop until answered.
2. **Normalize location.** Resolve `country` to ISO code if possible; geocode `region` if `coordinates` are missing and WebSearch/WebFetch are available.
3. **Select regulatory regime.** Use the `jurisdiction` field. If unknown, search authoritative sources (national EIA law, IFC, World Bank) and record the chosen regime with a citation.
4. **Determine EIA screening category.** Classify the project against the regime's screening thresholds (full EIA, initial environmental evaluation, exemption, etc.). Cite the threshold rule.
5. **Identify sensitive-receptor triggers.** Check proximity to protected areas (IUCN/Protected Planet), key biodiversity areas, and Red List species if coordinates are provided. Record presence/absence with sources.
6. **Build baseline-data requirements.** List required baseline surveys (air, water, soil, biodiversity, noise, social) and note which are provided vs. missing.
7. **Frame the question.** Convert the user's `goal` into an allowable harness objective. If the goal implies binding approval, downgrade to "screening recommendation" and flag for the compliance gate.
8. **Self-check against the Quality Gate.** Confirm schema validity, evidence links, and framework grounding.

## Outputs
A JSON object:

```json
{
  "project_profile": {
    "project_name": "string",
    "location": {"country": "string", "region": "string", "coordinates": {"lat": number, "lon": number}},
    "sector": "string",
    "scale": "small | medium | large",
    "activities": ["string"],
    "jurisdiction": "string",
    "regulatory_regime": "string",
    "eia_category": "full | initial_evaluation | screening | exemption | unknown",
    "sensitive_receptors": [{"name": "string", "type": "protected_area | habitat | species | community", "distance_km": number, "source": "citation"}],
    "baseline_requirements": [{"theme": "air | water | soil | biodiversity | noise | social", "status": "provided | required", "source": "citation"}],
    "allowed_goal": "draft | screen | compare | compliance_review",
    "notes": ["string"]
  },
  "evidence": ["citation or prior step"],
  "quality_gate_passed": true
}
```

## Tools
WebSearch, WebFetch, Read, Write, Bash

## Quality Gate
- Output is schema-valid against the schema above.
- Every material claim (regulatory regime, EIA category, receptor presence, baseline status) cites a source or prior step.
- Framework grounding: regulatory regime maps to a named framework; EIA category maps to the national EIA process stages.
- If required inputs are missing, the sub-skill stops and asks rather than fabricates.
