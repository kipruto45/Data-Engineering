import os
import subprocess

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SCRIPTS = os.path.join(BASE, 'scripts')


def test_generate_small():
    # generate small dataset to keep test fast
    cmd = ['python', os.path.join(SCRIPTS, 'generate_sample_data.py'), '--size', '100']
    subprocess.check_call(cmd)
    # assert files exist
    raw = os.path.join(BASE, 'data', 'raw')
    assert os.path.exists(os.path.join(raw, 'taxpayers_raw.csv'))


def test_run_pipeline():
    cmd = ['python', os.path.join(BASE, 'run_pipeline.py')]
    subprocess.check_call(cmd)
    # check db
    db = os.path.join(BASE, 'kra_tax.db')
    assert os.path.exists(db)
