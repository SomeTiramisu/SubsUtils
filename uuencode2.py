from pathlib import Path
import numpy as np

def encode3(a):
    x = (a [0]<<16)+(a[1]<<8)+a[2]
    f = lambda s: ((x>>s)&63)+33
    return f(np.array([18, 12, 6, 0]))
    
def encode(a):
    a3 = a.reshape((-1, 3))
    tmp = np.apply_along_axis(encode3, 1, a3)
    return tmp.reshape(-1)

def resize3(a):
    n = a.size
    if n%3:
        tmp = np.zeros(n+3-n%3, dtype=a.dtype)
        np.copyto(tmp[:n], a)
        return tmp
    return a

def to_string(a):
    s = ''
    c = 1
    for x in a:
        s += chr(x)
        if not c % 80: s+= '\n'
        c+=1
    return s

def uuencode(src):
    b = np.frombuffer(src.read_bytes(), dtype=np.ubyte)
    b = resize3(b)
    eb = encode(b)
    return to_string(eb)
    