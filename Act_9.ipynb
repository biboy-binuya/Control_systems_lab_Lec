import sympy as sp
from control import tf, step_response, poles, zeros, pzmap
import matplotlib.pyplot as plt
import numpy as np

# 1. Define Symbols
s = sp.symbols('s')
X = sp.symbols('X')
Y = sp.symbols('Y')

# 2. Represent the Equation: 2*s^2*Y + s*Y = s*X + X
# replace 'D' with 's' as per Laplace transform rules
A = 2*s**2 * Y + s * Y
B = s * X + X

# 3. Solve for Y/X (Transfer Function)
# Mathematically: Y(2s^2 + s) = X(s + 1) -> Y/X = (s + 1) / (2s^2 + s)
tf_expr = sp.solve(sp.Eq(A, B), Y)[0] / X
tf_simplified = sp.simplify(tf_expr)

print(f"Calculated Transfer Function G(s): {tf_simplified}")

# 4. Converted to Control Library Format
num_coeffs = [float(c) for c in sp.Poly(sp.numer(tf_simplified), s).all_coeffs()]
den_coeffs = [float(c) for c in sp.Poly(sp.denom(tf_simplified), s).all_coeffs()]

sys = tf(num_coeffs, den_coeffs)
print(sys)

# 5. Poles and zeros output value
print(f"Poles: {poles(sys)}")
print(f"Zeros: {zeros(sys)}")

# 6. Plot Step Response
t, y = step_response(sys)
plt.plot(t, y)
plt.title('Step Response')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

# 7. Poles and Zeros
pzmap(sys, grid=True)
plt.show()
