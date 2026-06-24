---
name: sub-risk-screener
description: Screen and score environmental impacts (air, water, soil, biodiversity, social) for significance.
parent: eia-report-automation
---

## Role
Sub-skill of `eia-report-automation`. Screen the project for significant environmental and social impacts and score each impact dimension using the Leopold matrix and the Rapid Impact Assessment Matrix (RIAM).

## Inputs
Output object from `sub-requirements-gatherer`:

| Field | Type | Notes |
|-------|------|-------|
| project_profile | object | Normalized project dossier. |
| project_profile.activities | string[] | Construction/operation activities. |
| project_profile.sensitive_receptors | object[] | Receptors with type and distance. |
| project_profile.baseline_requirements | object[] | Required vs. provided surveys. |

## Procedure
1. **Build the Leopold interaction matrix.** For each activity (row) and environmental/social receptor (column), identify whether an interaction exists and whether it is adverse, beneficial, or neutral.
2. **Score each interaction with RIAM.** For each `(activity, receptor)` pair, assign:
   - **A** = magnitude of change (1 = no/negligible, 2 = low, 3 = medium, 4 = high)
   - **B** = importance/condition of receptor (1 = low, 2 = moderate, 3 = high, 4 = critical)
   - **C** = duration of impact (1 = short, 2 = medium, 3 = long, 4 = irreversible)
   - **D** = scale/extent (1 = site-only, 2 = local, 3 = regional, 4 = national/global)
   - **RIAM score** = `(A + B) * (C + D)`.
3. **Convert to significance band.**
   - >= 48: A (very significant / critical)
   - 36-47: B (significant)
   - 24-35: C (moderate)
   - 12-23: D (low)
   - < 12: E (negligible)
4. **Aggregate by dimension.** Group interactions into `air`, `water`, `soil`, `biodiversity`, `social`, `cumulative`. The dimension score is the highest band among its interactions.
5. **Flag significant impacts and offset needs.** Any dimension scored A/B triggers the mitigation hierarchy and, where residual impact remains, an offset need.
6. **Validate data sufficiency.** If baseline data is missing for a scored dimension, lower the confidence and flag the gap.
7. **Self-check against the Quality Gate.**

## Outputs
A JSON object:

```json
{
  "leopold_matrix": [
    {"activity": "string", "receptor": "string", "dimension": "air | water | soil | biodiversity | social",
     "nature": "adverse | beneficial | neutral", "riam": {"A": 1-4, "B": 1-4, "C": 1-4, "D": 1-4, "score": number},
     "band": "A | B | C | D | E", "confidence": "high | medium | low", "evidence": ["citation"]}
  ],
  "dimension_scores": [
    {"dimension": "air | water | soil | biodiversity | social | cumulative",
     "band": "A-E", "riam_score": number, "framework": "Leopold matrix / RIAM", "evidence": ["citation"],
     "confidence": "high | medium | low"}
  ],
  "significant_impacts": [
    {"dimension": "string", "activity": "string", "receptor": "string", "band": "A | B",
     "mitigation_trigger": "avoid | minimize | restore | offset", "evidence": ["citation"]}
  ],
  "offset_needs": [{"dimension": "string", "justification": "string", "evidence": ["citation"]}],
  "confidence_notes": ["string"],
  "quality_gate_passed": true
}
```

## Tools
WebSearch, WebFetch, Read, Write, Bash

## Quality Gate
- Every `(A, B, C, D)` assignment is justified by a citation or prior step.
- No ad-hoc rubrics: all scoring derives from Leopold matrix and RIAM.
- Dimension scores reflect the worst interaction in that dimension.
- Significant impacts (A/B) trigger a mitigation tier.
