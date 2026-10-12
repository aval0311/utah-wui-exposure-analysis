# Dashboard browser checks

**Passed for accepted run 20261012T180540Z_eb3fdcb7.**

The detailed interaction checks used the passed rebuild's dashboard candidate. The accepted
replay's HTML was then compared with that candidate: all content and implementation matched
after consistently renaming generated Folium identifiers and normalizing line endings.
The accepted dashboard was reloaded for the final smoke checks and screenshots.

- Desktop: 1440 × 900 and 1366 × 768.
- Mobile portrait: 390 × 844 and 360 × 640.
- Short landscape: 844 × 390.
- All eleven overlay controls toggled and restored; two basemaps switched.
- Hazard image opacity verified at 0% and 100%; contextual legend followed layer state.
- Facility and block-group popups stayed within the visible map and had no horizontal overflow.
- Long block-group content scrolled to its final row in the short viewport.
- Fresh mobile view opened with the drawer closed; opening, closing, and Escape worked.
- Reset restored the three-county view.
- Both popup types stayed visible through native Fullscreen API entry and exit.
  Entry was confirmed by the active :fullscreen element, wui-app, and exit by its absence.
- No browser console warnings or errors were recorded during these checks.

This was a local HTTP test in the Codex in-app Chromium browser using responsive viewports.
It does not claim physical-device testing, coverage of every browser engine, or a completed
public GitHub Pages deployment. Recheck the deployed URL as described in RELEASE_HANDOFF.md.

Measurements, screenshots, candidate/accepted HTML hashes, and normalization details are
retained beside this report.
