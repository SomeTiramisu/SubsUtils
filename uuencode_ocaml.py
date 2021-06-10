import subprocess
import os.path as path

def uuencode(file):
    uuencode_exec, _ = path.split(path.realpath(__file__))
    proc = subprocess.run([uuencode_exec + '/uuencode3', file], capture_output=True)
    return proc.stdout.decode('ascii')
    