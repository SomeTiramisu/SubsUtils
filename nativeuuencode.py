import subprocess
from pathlib import Path

def _uuencode(src, bin_name):
    bin_path = Path(__file__).parent.joinpath("uuencode", bin_name)
    proc = subprocess.run([bin_path, src], capture_output=True)
    return proc.stdout.decode('ascii')
    
def cuuencode(src):
    return _uuencode(src, "cuuencode")

def ouuencode(src):
    return _uuencode(src, "ouuencode")

def ruuencode(src):
    return _uuencode(src, "ruuencode")
