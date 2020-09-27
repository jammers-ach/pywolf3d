from math import pi
from math import sqrt

def format_number(n, accuracy=6):
    """Formats a number in a friendly manner (removes trailing zeros and unneccesary point."""
    fs = "%."+str(accuracy)+"f"
    str_n = fs%float(n)
    if '.' in str_n:
        str_n = str_n.rstrip('0').rstrip('.')
    if str_n == "-0":
        str_n = "0"
    return str_n

def lerp(a, b, i):
    """Linear enterpolate from a to b."""
    return a+(b-a)*i

def linear_distance(a,b):
    """Linear distance from a to b"""
    return sqrt( (b[0]-a[0])**2 + (b[1] - a[1])**2)
