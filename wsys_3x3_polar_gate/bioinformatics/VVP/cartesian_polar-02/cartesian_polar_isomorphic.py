# cartesian_polar_isomorphic.py
import math
import struct
from typing import Tuple, Callable

class PLPFunctor:
    """Python isomorphic layer for Cartesian-Polar functor mapping"""
    
    def __init__(self):
        self.cartesian_to_polar = self._cartesian_to_polar
        self.polar_to_cartesian = self._polar_to_cartesian
        
    def encode_cartesian_binary(self, x: float, y: float) -> int:
        """Encode Cartesian coordinates to 8-bit binary"""
        x_encoded = int(((x + 10.0) / 20.0) * 15)
        y_encoded = int(((y + 10.0) / 20.0) * 15)
        return (x_encoded << 4) | y_encoded
    
    def encode_polar_binary(self, r: float, theta: float) -> int:
        """Encode Polar coordinates to 8-bit binary"""
        r_encoded = int((r / 10.0) * 15)
        theta_encoded = int((theta / 360.0) * 15)
        return (r_encoded << 4) | theta_encoded
    
    def decode_cartesian_binary(self, bits: int) -> Tuple[float, float]:
        """Decode binary back to Cartesian coordinates"""
        x_encoded = (bits >> 4) & 0x0F
        y_encoded = bits & 0x0F
        
        x = (x_encoded / 15.0) * 20.0 - 10.0
        y = (y_encoded / 15.0) * 20.0 - 10.0
        return x, y
    
    def decode_polar_binary(self, bits: int) -> Tuple[float, float]:
        """Decode binary back to Polar coordinates"""
        r_encoded = (bits >> 4) & 0x0F
        theta_encoded = bits & 0x0F
        
        r = (r_encoded / 15.0) * 10.0
        theta = (theta_encoded / 15.0) * 360.0
        return r, theta
    
    def _cartesian_to_polar(self, cart_bits: int) -> int:
        """Heterogeneous functor: Cartesian to Polar"""
        x, y = self.decode_cartesian_binary(cart_bits)
        
        r = math.sqrt(x*x + y*y)
        theta = math.degrees(math.atan2(y, x))
        if theta < 0:
            theta += 360.0
            
        return self.encode_polar_binary(r, theta)
    
    def _polar_to_cartesian(self, polar_bits: int) -> int:
        """Heterogeneous functor: Polar to Cartesian"""
        r, theta = self.decode_polar_binary(polar_bits)
        
        rad = math.radians(theta)
        x = r * math.cos(rad)
        y = r * math.sin(rad)
        
        return self.encode_cartesian_binary(x, y)
    
    def is_sparse_mapping_valid(self, cart_bits: int, polar_bits: int) -> bool:
        """Validate sparse mapping between coordinate systems"""
        converted_cart = self._polar_to_cartesian(polar_bits)
        x1, y1 = self.decode_cartesian_binary(cart_bits)
        x2, y2 = self.decode_cartesian_binary(converted_cart)
        
        distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return distance < 1.0

# Real-time conversion system using PLP framework
class RealTimeCoordinateSystem:
    def __init__(self):
        self.functor = PLPFunctor()
        self.current_system = 'cartesian'  # or 'polar'
        
    def convert_point(self, point_bits: int, target_system: str) -> int:
        """Real-time conversion between coordinate systems"""
        if self.current_system == target_system:
            return point_bits
            
        if self.current_system == 'cartesian' and target_system == 'polar':
            return self.functor.cartesian_to_polar(point_bits)
        else:
            return self.functor.polar_to_cartesian(point_bits)
    
    def set_coordinate_system(self, system: str):
        """Switch between Cartesian and Polar systems"""
        self.current_system = system

# Example usage
if __name__ == "__main__":
    # Create the functor system
    rt_system = RealTimeCoordinateSystem()
    
    # Example: Convert Cartesian point (3, 4) to Polar
    cart_bits = rt_system.functor.encode_cartesian_binary(3.0, 4.0)
    polar_bits = rt_system.convert_point(cart_bits, 'polar')
    
    r, theta = rt_system.functor.decode_polar_binary(polar_bits)
    print(f"Cartesian (3,4) -> Polar: r={r:.2f}, θ={theta:.2f}°")
    
    # Convert back to verify isomorphism
    converted_back = rt_system.convert_point(polar_bits, 'cartesian')
    x, y = rt_system.functor.decode_cartesian_binary(converted_back)
    print(f"Polar -> Cartesian: ({x:.2f}, {y:.2f})")
    
    # Validate sparse mapping
    is_valid = rt_system.functor.is_sparse_mapping_valid(cart_bits, polar_bits)
    print(f"Sparse mapping valid: {is_valid}")
