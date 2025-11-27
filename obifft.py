"""
OBIFFT.PY - Obinexus Fast Fourier Transform Model
Author: Nnamdi Michael Okpala
License: MIT
Repository: https://github.com/obinexus
This model implements a triangular matrix-based transformation pipeline.
Includes:
- Homogeneous input enforcement
- Buffer size gating
- Matrix construction (triangular and square)
- 2D convolution (signal-style)
- Linear solving (AX = C)
- Parity elimination logic for dual-buffer edge-case resolution
"""

import numpy as np
from scipy.signal import convolve2d

class InputDataError(Exception):
    pass

class MatrixModel:
    def __init__(self, min_input_bytes=32768):
        self.min_input_bytes = min_input_bytes
        self.input_buffer = []

    def validate_input(self, data_chunk):
        if not all(isinstance(x, (int, float)) for x in data_chunk):
            raise InputDataError("Only numeric, homogeneous data allowed.")

    def feed_data(self, data_chunk):
        self.validate_input(data_chunk)
        self.input_buffer.extend(data_chunk)
        buffer_size = len(self.input_buffer) * 8
        return buffer_size >= self.min_input_bytes

    def build_triangle_matrix(self):
        n = int((2 * len(self.input_buffer))**0.5)
        triangle_size = n * (n + 1) // 2
        if triangle_size == 0:
            raise InputDataError("Not enough data to build matrix.")
        triangular_data = self.input_buffer[:triangle_size]
        self.input_buffer = self.input_buffer[triangle_size:]
        matrix = np.zeros((n, n))
        index = 0
        for i in range(n):
            for j in range(i + 1):
                matrix[i][j] = triangular_data[index]
                index += 1
        return matrix

    def build_square_matrix(self):
        n = int(len(self.input_buffer)**0.5)
        square_size = n * n
        if square_size == 0:
            raise InputDataError("Not enough data to build square matrix.")
        square_data = self.input_buffer[:square_size]
        self.input_buffer = self.input_buffer[square_size:]
        return np.array(square_data).reshape(n, n)

    def convolve_matrix(self, matrix, kernel):
        return convolve2d(matrix, kernel, mode='same')

    def solve_ax_equals_c(self, A, C):
        try:
            A_inv = np.linalg.inv(A)
            return np.dot(A_inv, C)
        except np.linalg.LinAlgError:
            raise InputDataError("Matrix A is singular and cannot be inverted.")

    def parity_eliminate_dual(self, A1, A2):
        return (A1 + A2) / 2  # simple average fusion for dual-buffer case

if __name__ == '__main__':
    model = MatrixModel(min_input_bytes=0)
    example_data = list(range(1, 37))
    model.feed_data(example_data)
    Ma1 = model.build_triangle_matrix()
    model.feed_data(example_data)
    Mb1 = model.build_triangle_matrix()

    kernel = np.array([[1, 0, -1],
                       [1, 0, -1],
                       [1, 0, -1]])

    conv_Ma1 = model.convolve_matrix(Ma1, kernel)
    conv_Mb1 = model.convolve_matrix(Mb1, kernel)

    print("Triangular Matrix A (Ma1):\n", Ma1)
    print("Convolved Ma1:\n", conv_Ma1)
    print("Triangular Matrix B (Mb1):\n", Mb1)
    print("Convolved Mb1:\n", conv_Mb1)

    try:
        if Ma1.shape != conv_Mb1.shape:
            raise InputDataError("Shapes of A and C do not match for solving AX = C.")
        X = model.solve_ax_equals_c(Ma1, conv_Mb1)
        print("Solved X from AX = C:\n", X)
    except InputDataError as e:
        print("Error:", str(e))
 to join this conversation 
