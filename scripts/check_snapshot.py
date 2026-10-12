"""Verify the release snapshot before starting Jupyter."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from wui.runtime import recipe_hash, sha256, require_source_inventory

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("workspace", type=Path)
args = parser.parse_args()
root = args.workspace.resolve()
manifest = json.loads((root / "snapshot_manifest.json").read_text(encoding="utf-8"))
repository = Path(__file__).resolve().parents[1]
if manifest["recipe_sha256"] != recipe_hash(repository):
    raise SystemExit("The snapshot recipe does not match this notebook version.")
records = manifest["cache_inputs"]
if not records:
    raise SystemExit("Snapshot inventory is empty.")
require_source_inventory(records)
for record in records:
    path = (root / record["path"]).resolve()
    if not path.is_relative_to(root):
        raise SystemExit("Invalid path in snapshot inventory.")
    if not path.is_file() or sha256(path) != record["sha256"]:
        raise SystemExit("Missing or changed snapshot input: " + record["path"])
print(f"PASS: {len(records)} input files and the analytical recipe match the snapshot.")

