---
name: sub-compliance-check
description: Verify regulatory completeness and gate the report behind a 'requires licensed-expert review' disclaimer.
parent: eia-report-automation
---

## Role
Sub-skill of `eia-report-automation`. Verify that the draft EIA contains the regulatory elements required by the governing jurisdiction, enforce the mandatory professional-review disclaimer, and block binding approval language.

## Inputs
Outputs from `sub-requirements-gatherer` and `sub-risk-screener`:

| Field | Type | Notes |
|-------|------|-------|
| project_profile | object | Including `jurisdiction`, `eia_category`, `regulatory_regime`. |
| dimension_scores | object[] | Significant impact bands. |
| significant_impacts | object[] | A/B impacts. |

## Procedure
1. **Load jurisdictional checklist.** Retrieve the required EIA contents for the project's `regulatory_regime`. Use `SECOND-KNOWLEDGE-BRAIN.md` and WebSearch/WebFetch as sources.
2. **Check mandatory sections.** Typical required sections include:
   - project description and alternatives;
   - policy/legal/regulatory framework;
   - baseline description;
   - impact identification and significance (Leopold/RIAM);
   - mitigation and monitoring plan;
   - public consultation / stakeholder engagement;
   - cumulative impact assessment;
   - environmental management plan.
3. **Score completeness.** For each required section, mark `present`, `partial`, or `missing`. Compute `completeness_ratio = present / total`.
4. **Identify binding-approval triggers.** If the user's goal implies approval or "pass", set `approval_blocked = true` and force a screening-only verdict.
5. **Build the disclaimer.** The disclaimer must state:
   - the deliverable is not legally/officially binding;
   - a qualified, licensed professional must review and sign off;
   - jurisdiction-specific limits and any cross-border differences are flagged.
6. **Flag jurisdiction conflicts.** If multiple jurisdictions apply and they materially differ, note the conflict.
7. **Self-check against the Quality Gate.**

## Outputs
A JSON object:

```json
{
  "jurisdiction": "string",
  "regulatory_framework": "string",
  "required_sections": [
    {"section": "string", "status": "present | partial | missing", "evidence": ["citation"]}
  ],
  "completeness_ratio": "number 0.0-1.0",
  "approval_blocked": true,
  "disclaimer": "string — mandatory professional-review notice",
  "missing_elements": ["string"],
  "jurisdiction_conflicts": ["string"],
  "compliance_score": "pass | conditional | fail",
  "evidence": ["citation"],
  "quality_gate_passed": true
}
```

## Compliance Rules
- Do not present output as binding legal/official advice.
- Identify the governing jurisdiction(s) and flag where they materially differ.
- Attach a disclaimer recommending a qualified, licensed professional.
- Block the final deliverable if a mandatory compliance element is missing (`completeness_ratio < 0.6` or missing disclaimer).

## Tools
WebSearch, WebFetch, Read, Write, Bash

## Quality Gate
- Output is schema-valid.
- Every section status cites a source or prior step.
- `completeness_ratio` is computed from an explicit checklist.
- The disclaimer is present and non-empty.
- If `approval_blocked` is true, the verdict must be screening-only.
