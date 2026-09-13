"""Rebuild from the reviewed, version-controlled factual tables (no scraping)."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
for script in ['source_catalog.py','build_dataset.py','render_maps.py','validate.py']:
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)
