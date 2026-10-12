# Publish release v3

The code ZIP contains the executed notebook, supporting modules, documentation, accepted-run
tables and figures, and docs/index.html. The separate v3 snapshot ZIP contains analytical
inputs and matching derivatives. Neither package changes an existing repository or workspace.

## Review

1. Extract the code release into a review folder and open docs/index.html in a browser.
2. Review the notebook's opening results, methods, limitations, and future-work section.
3. Consult evidence/release_validation.json and the browser report for the checks actually completed.
4. Keep the matching v3 source archive if you want to rerun the notebook. A fresh run is not
   required merely to publish the already validated saved outputs.

## Replace repository content

Use a new Git branch and preserve existing history. Copy the contents of this code package
into the repository root, including src/, scripts/, environment.yml, data documentation,
notebooks/, images/, outputs/, docs/, and evidence/. Review the resulting diff.
The replacement_manifest.json lists obsolete images for manual removal after checking
that current documents no longer reference them. No cleanup is performed automatically.

Do not copy the large analytical data workspace into Git. Leave the retained working
workspace unchanged; use the separate matching snapshot whenever testing a new execution.

## Publish the dashboard

Configure GitHub Pages to deploy the repository's main branch /docs folder (or retain a
compatible existing Pages workflow), then commit and push the reviewed release. Verify
the completed Pages deployment at the repository's published URL. The expected project
URL is https://aval0311.github.io/utah-wui-exposure-analysis/; confirm it in repository settings.

Check county boundary toggles, all layer groups, opacity, facility/block-group popups, reset,
mobile drawer behavior, and native fullscreen on the public deployment. Local browser
validation does not establish that GitHub Pages deployment has completed.

After verifying v3 at that URL, change the README's deployment-target wording to a direct
live-dashboard link. If desired, set PUBLIC_DASHBOARD_URL in the notebook for later
executions. Publish the snapshot to a data host and update the data guide and download
record with its verified public link. Data hosting and GitHub deployment remain maintainer steps.

## New accepted executions

Use the complete package and matching snapshot with the tested kernel. Restart and run all
cells in snapshot mode. Use scripts/export_publication.py with the accepted run directory
to synchronize presentation assets and opening summaries. Then regenerate current equivalence,
browser evidence, and release checksums. Keep retained historical benchmark records labeled
as historical; they are not replaced by an ordinary notebook execution.
