# main.py
import ctypes, pathlib, sys, math
from ctypes import c_double, POINTER

SO = pathlib.Path(__file__).parent / "plp128.so"

# -------------------------------------------------
# 1. Try to load the fast C library
# -------------------------------------------------
try:
    lib = ctypes.CDLL(str(SO))
    lib.plp_cart2pol.argtypes = [c_double, c_double, POINTER(c_double * 2)]
    lib.plp_pol2cart.argtypes = [c_double, c_double, POINTER(c_double * 2)]
    lib.plp_cart2pol.restype = ctypes.c_int
    lib.plp_pol2cart.restype = ctypes.c_int
    _c_fast = True
except Exception as e:
    print("C lib not available → falling back to pure Python", file=sys.stderr)
    _c_fast = False

# -------------------------------------------------
# 2. Pure-Python implementations (identical API)
# -------------------------------------------------
def _py_cart2pol(x, y):
    r = math.hypot(x, y)
    theta = math.degrees(math.atan2(y, x))
    return r, theta

def _py_pol2cart(r, theta_deg):
    rad = math.radians(theta_deg)
    return r * math.cos(rad), r * math.sin(rad)

# -------------------------------------------------
# 3. Unified public API
# -------------------------------------------------
def cart2pol(x, y):
    if _c_fast:
        buf = (c_double * 2)()
        lib.plp_cart2pol(x, y, buf)
        return buf[0], buf[1]
    else:
        return _py_cart2pol(x, y)

def pol2cart(r, theta_deg):
    if _c_fast:
        buf = (c_double * 2)()
        lib.plp_pol2cart(r, theta_deg, buf)
        return buf[0], buf[1]
    else:
        return _py_pol2cart(r, theta_deg)

# -------------------------------------------------
# 4. CLI demo
# -------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python main.py cart x y   OR   python main.py pol r theta")
        sys.exit(1)

    mode = sys.argv[1].lower()
    a, b = float(sys.argv[2]), float(sys.argv[3])

    if mode == 'cart':
        r, theta = cart2pol(a, b)
        print(f"Polar → r = {r:.6f}  θ = {theta:.6f}°")
    elif mode == 'pol':
        x, y = pol2cart(a, b)
        print(f"Cartesian → x = {x:.6f}  y = {y:.6f}")
    else:
        print("Unknown mode")
