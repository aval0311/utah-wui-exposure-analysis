"""Portable wrapper; original statistical implementation is unchanged."""
from pathlib import Path
import argparse, importlib.util, sys, unittest
HERE=Path(__file__).resolve().parent
def load():
    spec=importlib.util.spec_from_file_location('forecast_experiment',HERE/'reference/experiment.py')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['test','prepare','train','evaluate','verify'])
    p.add_argument('--workspace',type=Path,help='Preserved workspace containing exact audited exports; required for real-data stages')
    p.add_argument('--run-name',default='local_reproduction')
    a=p.parse_args()
    if a.command!='test' and a.workspace is None: p.error('Real-data stages require an explicit --workspace; no automatic source discovery.')
    if not a.run_name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in a.run_name):p.error('Use a simple run name, without paths.')
    rs=importlib.util.spec_from_file_location('package_review',HERE/'review.py')
    reviewer=importlib.util.module_from_spec(rs);rs.loader.exec_module(reviewer)
    reviewer.verify()
    e=load()  # Initializes the original process-local Conda DLL paths before tests import NumPy.
    if a.command=='test':
        suite=unittest.TestSuite([unittest.TestLoader().discover(str(HERE/'reference'),pattern='test_contract.py'),unittest.TestLoader().discover(str(HERE/'tests'),pattern='test_*.py')])
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(0 if result.wasSuccessful() else 1)
    e.ROOT=a.workspace.resolve(); e.PLAN=HERE/'specification'; e.OUT=HERE/'runs'/a.run_name
    e.OUT.parent.mkdir(exist_ok=True)
    getattr(e,a.command)()
if __name__=='__main__':main()
