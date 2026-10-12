# Publication audit revisions

The release preserves the complete ETL workflow while making its analytical scope and evidence
easier to review.

| Priority | Finding | Revision |
|---|---|---|
| High | Historical occurrence processing mixed incident categories and did not clearly state its domain | Select WF records within an explicit UTC interval; report rectangle and actual county counts; reconcile every excluded record |
| High | Two central analytical inputs were outside the required source checksum inventory | Require and verify the ACS numerical CSV and occurrence GeoJSON, including when rebuilding derivatives |
| High | Cached observation-support counters could report values that had not been calculated | Calculate support and mutually exclusive NDVI/NDMI availability from the retained rasters on either execution path |
| High | Phase order and headings interrupted the ETL narrative | Present overview and assumptions before configuration; place dashboard assembly after analytical findings; correct phase and facility headings |
| Medium | Facility flags and popup context suggested stronger conclusions than the calculation supports | Name the one-mile proximity rule explicitly; identify demographics as block-group values |
| Medium | Overview map used a large combined extent with sparse detail | Show separate polygon-masked county panels and study-wide class areas; identify differing map scales |
| Medium | Opening claims and evidence could become stale after a new run | Export notebook and README summaries from the accepted run; move previous release reports into historical evidence |
| Medium | Historical HPC benchmark could be mistaken for a whole-pipeline or current-input result | State benchmark workload, timing boundaries, and memory tradeoff; provide a separate current serial/Dask comparison |
| Medium | Next-step modeling objective needed precise scope | Document a planned model of new recorded wildfire ignition probability for a defined unit and future period; no predictive model is claimed here |

## Deliberately retained analytical limitations

Area-weighted exposure assumes uniform demographic density within block groups.
The weighted hazard index is not calibrated against observed future outcomes.
Source vintages differ; MTBS absence leaves the history term capped at 0.60 under the
retained weighting formulation. The canonical county footprint has a disclosed 208-cell
difference from independent reconstruction. Coverage exclusions remain separate from modeled
hazard values. Future ML development requires a time-aligned, independently validated dataset.

Stable internal filenames and component identifiers can retain the legacy
historical_fire_likelihood key for compatibility. Reader-facing descriptions identify it
as an occurrence indicator and do not interpret it as a probability.
