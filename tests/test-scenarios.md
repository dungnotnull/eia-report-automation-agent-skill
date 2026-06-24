
# tests/test-scenarios.md - Environmental Impact Assessment (EIA) Report Automation

Scenario-based tests for the `eia-report-automation` harness. Each scenario asserts the harness flow,
framework-grounded scoring, gate enforcement, and deliverable shape.

## Scenario 1: Small factory EIA
- **Given:** A small garment factory (300 employees, light manufacturing) in Vietnam, district industrial zone, no protected area nearby.
- **Inputs:** `{"project_name": "ABC Garment Factory", "location": {"country": "VN", "region": "Binh Duong"}, "sector": "manufacturing", "scale": "small", "activities": ["cutting", "sewing", "washing", "boiler operation"], "jurisdiction": "Vietnam", "sensitive_receptors": [], "goal": "draft EIA"}`
- **Expected harness behavior:** intake validates -> framework selected (Vietnam EIA + IFC PS) -> Leopold/RIAM scores air/water/noise/social -> compliance gate attaches disclaimer -> roadmap ranks effluent treatment and worker safety first.
- **Pass criteria:** all quality gates pass; every score cites a framework; `disclaimer` is non-empty; roadmap items are effort/impact-ranked; `completeness_ratio >= 0.6`.

## Scenario 2: Project near protected area
- **Given:** A 5 MW solar farm proposed 500 m from a Ramsar wetland in the Philippines.
- **Inputs:** `{"project_name": "Laguna Solar Farm", "location": {"country": "PH", "coordinates": {"lat": 14.3, "lon": 121.0}}, "sector": "solar", "scale": "medium", "activities": ["panel installation", "cable trenching", "access roads"], "jurisdiction": "Philippines", "sensitive_receptors": ["Ramsar wetland"], "goal": "screen impacts"}`
- **Expected harness behavior:** biodiversity dimension scores A/B; offset need flagged; protected-area trigger cited from Protected Planet/IUCN; compliance gate enforced.
- **Pass criteria:** biodiversity is among the highest bands; offset need is documented; all citations present.

## Scenario 3: Wastewater discharge exceedance
- **Given:** A medium food-processing plant discharging high-BOD effluent near a river in Thailand.
- **Inputs:** `{"project_name": "Thai Food Processing", "location": {"country": "TH"}, "sector": "manufacturing", "scale": "medium", "activities": ["washing", "blanching", "effluent discharge"], "jurisdiction": "Thailand", "sensitive_receptors": ["river"], "goal": "check compliance"}`
- **Expected harness behavior:** water dimension scores B/C; mitigation hierarchy suggests minimize (effluent treatment) before discharge; standards-updater cites national discharge limits; exceedance risk flagged.
- **Pass criteria:** roadmap actions ordered avoid > minimize > restore > offset; standards snapshot includes water parameter limit.


## Scenario 4: User asks to approve
- **Given:** Same as Scenario 1, but user goal is `approve the project`.
- **Inputs:** goal = `approve`.
- **Expected harness behavior:** harness downgrades goal to `screen`; `approval_blocked` = true; final verdict is screening recommendation only; disclaimer is enforced.
- **Pass criteria:** no binding approval language; `compliance_score` is `conditional` or `fail` unless all sections present; disclaimer is mandatory.

## Scenario 5: Regulation update changes discharge limit
- **Given:** Scenario 3 project, but the national standard has been tightened since the last brain update.
- **Inputs:** same as Scenario 3, with `baseline_data` referencing an older permit.
- **Expected harness behavior:** `sub-standards-updater` flags `refresh_needed`; compares project load to new limit; `regulatory_changes` contains the update; compliance section is revised.
- **Pass criteria:** `refresh_needed` = true if brain age > 7 days or data gap exists; exceedance risk is re-evaluated.

## Scenario 6: Impact-significance matrix + operations monitoring plan
- **Given:** A quarry expansion in Indonesia with air, noise, and biodiversity impacts.
- **Inputs:** `{"project_name": "Java Quarry Expansion", "location": {"country": "ID"}, "sector": "quarry", "scale": "large", "activities": ["blasting", "crushing", "hauling", "rehabilitation"], "jurisdiction": "Indonesia", "sensitive_receptors": ["forest edge community"], "goal": "operations monitoring plan"}`
- **Expected harness behavior:** harness emits a full Leopold matrix; multi-dimensional score includes air, water, soil, biodiversity, social, cumulative; monitoring plan covers all A/B impacts with indicators and thresholds.
- **Pass criteria:** output contains `leopold_matrix`; monitoring plan length >= number of A/B impacts; all seven Output Format sections present.

## Cross-cutting checks
- **Graceful degradation:** with WebSearch/WebFetch disabled, the harness still produces a deliverable and explicitly states the knowledge-currency limitation.
- **Refusal/scope:** out-of-scope or unsafe requests are refused or redirected with the mandatory professional-consultation disclaimer.
- **Determinism of structure:** every run yields the seven Output-Format sections.
