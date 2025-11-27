# sparse_coord.py
import ctypes, math, os, pathlib
from ctypes import c_double, c_int, Structure

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libsparse_coord.so')))

class Cart(Structure): _fields_ = [('x', c_double), ('y', c_double)]
class Pol(Structure):  _fields_ = [('r', c_double), ('theta', c_double)]

lib.sparse_coord_functor.argtypes = [ctypes.POINTER(Cart), ctypes.POINTER(Pol), c_int, c_int]
lib.sparse_coord_functor.restype  = None

def functor(c=None, p=None):
    """Sparse functor – give one side, get the other."""
    have_c = c is not None
    have_p = p is not None
    if not (have_c or have_p):
        raise ValueError("At least one side must be provided")
    _c = Cart(c.x, c.y) if have_c else Cart(0,0)
    _p = Pol(p.r, p.theta) if have_p else Pol(0,0)
    lib.sparse_coord_functor(ctypes.byref(_c), ctypes.byref(_p), int(have_c), int(have_p))
    return (None if not have_c else Cart(_c.x, _c.y),
            None if not have_p else Pol(_p.r, _p.theta))

# ----------  Demo  ----------
if __name__ == '__main__':
    cart, polar = functor(c=type('C',(object,),{'x':12.0,'y':5.0})())
    print(f"Polar → r={polar.r:.3f}  θ={math.degrees(polar.theta):.1f}°")

    cart, polar = functor(p=type('P',(object,),{'r':13.0,'theta':math.radians(22.6)})())
    print(f"Cartesian → x={cart.x:.3f}  y={cart.y:.3f}")
