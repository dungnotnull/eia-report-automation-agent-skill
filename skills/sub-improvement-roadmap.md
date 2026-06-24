---
name: sub-improvement-roadmap
description: Produce a mitigation and monitoring plan ordered by the mitigation hierarchy and impact significance.
parent: eia-report-automation
---

## Role
Sub-skill of `eia-report-automation`. Convert the scored impacts into a prioritized mitigation and monitoring roadmap ordered by the mitigation hierarchy and ranked by effort * impact.

## Inputs
Outputs from `sub-risk-screener`, `sub-compliance-check`, and `sub-standards-updater`:

| Field | Type | Notes |
|-------|------|-------|
| significant_impacts | object[] | A/B impacts with dimension and receptor. |
| dimension_scores | object[] | All dimension bands. |
| standards_snapshot | object[] | Applicable limits. |
| missing_elements | string[] | Compliance gaps. |

## Procedure
1. **Map each significant impact to the mitigation hierarchy.**
   - **Avoid** — redesign, relocate, or cancel the activity if impacts are critical and irreversible.
   - **Minimize** — engineering controls, scheduling, emission controls, effluent treatment.
   - **Restore** — rehabilitation, re-vegetation, soil remediation.
   - **Offset** — biodiversity offsets, compensation, restoration elsewhere; only after other tiers are exhausted.
2. **Assign effort and impact.** For each action, assign:
   - `effort` (low/medium/high) based on capital/operational cost and time.
   - `impact` (low/medium/high) based on the RIAM band and receptor sensitivity.
3. **Compute priority.** `priority_score = impact_weight * effort_inverse` where impact_weight = {A:4, B:3, C:2, D:1, E:0.5} and effort_inverse = {low:3, medium:2, high:1}. Rank descending; ties broken by mitigation tier (avoid > minimize > restore > offset).
4. **Build monitoring plan.** For each significant A/B impact, define indicator, frequency, method, responsible party, and threshold.
5. **Address compliance gaps.** Add actions that close `missing_elements` from `sub-compliance-check`.
6. **Self-check against the Quality Gate.**

## Outputs
A JSON object:

```json
{
  "prioritized_actions": [
    {"rank": 1, "action": "string", "dimension": "air | water | soil | biodiversity | social | cumulative",
     "tier": "avoid | minimize | restore | offset", "effort": "low | medium | high",
     "impact": "low | medium | high", "priority_score": number,
     "rationale": "string", "evidence": ["citation"]}
  ],
  "monitoring_plan": [
    {"dimension": "string", "indicator": "string", "frequency": "string",
     "method": "string", "responsible_party": "string", "threshold": "string",
     "evidence": ["citation"]}
  ],
  "residual_risks": [
    {"dimension": "string", "risk": "string", "management": "string"}
  ],
  "compliance_closure_actions": ["string"],
  "evidence": ["citation"],
  "quality_gate_passed": true
}
```

## Tools
WebSearch, WebFetch, Read, Write, Bash

## Quality Gate
- Every action maps to a mitigation tier in the hierarchy.
- Priority ranking uses the defined formula; no arbitrary ordering.
- The monitoring plan covers every A/B impact.
- Residual risks are acknowledged.
