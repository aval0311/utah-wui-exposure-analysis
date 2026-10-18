# Predictor and label availability audit

## Audit conclusion

All 20 frozen predictors have been inventoried from the frozen specification. **None has complete historical as-issued provenance established by the inspected evidence.** Geometry is a fixed design choice; terrain is conditionally usable as a static proxy; climate is conditionally usable as a retrospective reconstruction. No observation values were read to make these classifications.

The accompanying CSV separates observed facts, assumptions and the evidence required for acceptance. A blank or unknown publication timestamp means unverified, not available. Existing file modification dates and present-day download dates are not substitutes for historical publication dates.

## Terrain and geometry

The thirteen terrain summaries derive from the retained aligned USGS 3DEP elevation raster, slope and aspect. Source paths and aggregation rules are in `wui_ml/terrain_policy.json`. Elevation and slope use area-weighted means, standard deviations and quantiles; aspect supplies northness and eastness; flat fraction uses slope below one degree. Exact polygon-pixel intersection uses the original county-clipped geometry, and source-group coverage below 95% yields missing values.

The policy explicitly accepts contemporary terrain as time-invariant. That is a plausible reconstruction convention but does not establish historical acquisition, historical terrain conditions or past publication. Slope and aspect inherit the DEM's provenance; their processing date cannot resolve the source's availability. Audit mosaic acquisition dates, source releases and processing lineage before any strict replay.

`study_area_km2` describes observation geometry. Keep the original support for comparability and do not apply a contemporary WUI or burnable-land mask. A fixed retrospective geometry can define the experiment, but the exact boundary/grid version still needs a pre-issue record for an operational replay claim. Primary county is proposed only for the county baseline; IDs remain join keys, not arbitrary numerical predictors.

## Antecedent climate

The frozen six features use precipitation, midpoint temperature derived from Tmin/Tmax, and vapor pressure deficit in two fixed windows. Daily precipitation is summed; temperature and VPD are averaged, then native climate-pixel overlaps are area weighted. Complete temporal support is required; missing support remains missing for training-only imputation. Existing temperature inversion checks must be retained without using later outcomes to repair values.

The existing climate report specifies source dates from October 1999 through September 2020 solely to construct target years 2001–2021. Those earlier measurement dates are already part of the reviewed reconstruction, not an extension of authorized target years. No new source retrieval is proposed here.

The provider defines the nominal day at 07:00 UTC and calls the last 60 days preliminary. It also dates the addition of VPD to January 2018. These facts support the timing cautions, not proof that today's historical values were accessible at earlier cutoffs. In particular, a December 2017 cutoff for a 2018 forecast precedes that documented VPD addition. Strict replay using these VPD fields is unsupported for forecast years through 2018; later vintages still need verification. [Official gridMET documentation](https://www.climatologylab.org/gridmet.html), accessed October 17, 2026.

Keep 60 days as an explicitly assumed reconstruction delay. Publication, product existence, revisions and source availability must each pass independently. A delayed measurement window cannot remove revision leakage.

## Additional candidates and exclusions

The proposed log-area feature is a deterministic transform of positive cell area and inherits geometry provenance. Historical pooled, recent, county and cell rates are fitted quantities, not static attributes: recompute them from eligible earlier labels within each fold. They inherit publication and review latency. Do not compute a full-period cell frequency and attach it to every historical year.

Target-year observed climate, target-year incident counts, target-year reporting/source assignments, contemporary WUI/fuel/vegetation/roads/population layers without historical versions, saved ML predictions and 2025 masks are excluded from version 1. Seasonal forecasts would require archived issue dates and vintage-matched hindcasts plus a separate design; they are not necessary for this first comparison.

## Label availability is also a gate

The target measures recorded discoveries. Discovery date is the event date, not the date a record or final zero became available. Missing incident records do not prove complete surveillance. Review approval timestamps, source snapshots, correction histories and coverage criteria are needed for training labels and exclusions, including zero-label maturation. Even an incident approval date alone cannot establish a complete cell-year zero.

The proposed T−2 label limit supplies time for reporting but does not certify completeness. The frozen unknown and flagged-zero masks may incorporate later review knowledge. Treat them as retrospective cohort definitions until historical availability is demonstrated. The 2020 source transition can change the observation process; it cannot safely become a target-year predictor inferred from the fires observed that year.

## Evidence register

Local paths are relative to the ML Phase notebooks working directory. Fingerprints are recorded in `planning_manifest.json`.

- `publication_releases/wui_ml_v1_1.0.0/data/frozen_specification.json`: exact 20-feature list, target, frozen recommendation and limitations.
- `ml_outputs/climate_features_ba80797440f5/feature_report.json`: windows, units, assumed lag, source-date support and unverified vintages.
- `wui_ml/climate_features.py`: cutoff arithmetic and feature-construction logic, inspected as text only.
- `wui_ml/terrain_policy.json` and `wui_ml/terrain_features.py`: source paths, aggregation, missingness and static-terrain assumption; inspected as metadata/code only.
- `historical_timeline_v1/tools/build_data.py`: reviewed target/cohort rules and scoped reader example; not executed.
- `wui_ml/reporting_coverage_audit.py`: reporting-transition limitations; not executed.

This audit establishes what can and cannot be inferred from the available metadata. It does not certify source vintages, evaluate features or authorize training.
