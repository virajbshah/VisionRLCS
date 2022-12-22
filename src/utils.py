from math import sin, cos
import numpy as np

class Color:
    RED     = (0xFF, 0x00, 0x00)
    GREEN   = (0x00, 0xFF, 0x00)
    BLUE    = (0x00, 0x00, 0xFF)
    CYAN    = (0x00, 0xFF, 0xFF)
    YELLOW  = (0xFF, 0x00, 0xFF)
    MAGENTA = (0xFF, 0xFF, 0x00)
    BLACK   = (0x00, 0x00, 0x00)
    GRAY    = (0x96, 0x96, 0x96)
    WHITE   = (0xFF, 0xFF, 0xFF)

def rotate(v, theta):
    s = sin(theta)
    c = cos(theta)

    m = np.array([
        [c, -s],
        [s,  c]    
    ], dtype=np.float64)

    return np.matmul(m, v)