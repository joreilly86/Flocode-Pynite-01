# Units used for the model in this example are meters and kilonewtons

# Import `FEModel3D` from `PyNite`
from PyNite import FEModel3D
from matplotlib import pyplot as plt
import numpy as np

# Import 'Visualization' for rendering the model
from PyNite import Visualization

# Create a new finite element model
simple_beam = FEModel3D()

# Add nodes (6 meters apart)
simple_beam.add_node('N1', 0, 0, 0)
simple_beam.add_node('N2', 6, 0, 0)  # 6 meters

# Define a material
E = 210000  # Modulus of elasticity (MPa)
G = 81000   # Shear modulus of elasticity (MPa)
nu = 0.3    # Poisson's ratio
rho = 7.85  # Density (kg/m^3)
simple_beam.add_material('Steel', E, G, nu, rho)

# Add a beam with the following properties:
# Iy = 1.2e-4 m^4, Iz = 1.6e-4 m^4, J = 2.7e-4 m^4, A = 0.025 m^2
simple_beam.add_member('M1', 'N1', 'N2', 'Steel', 1.2e-4, 1.6e-4, 2.7e-4, 0.025)

# Provide simple supports
# simple_beam.def_support(node_id, u1, u2, u3, r1, r2, r3)
# where u1, u2, u3 are the restraints in the x, y, and z directions, respectively, 
# and r1, r2, r3 are the rotations about the x, y, and z axes, respectively.
simple_beam.def_support('N1', True, True, True, False, False, False)
simple_beam.def_support('N2', True, True, True, True, False, False)

# Add a uniformly distributed load (UDL) of 20 kN/m to the beam
# simple_beam.add_member_dist_load(member_id, direction, w1, w2, x1, x2, case)
simple_beam.add_member_dist_load('M1', 'Fy', -20, -20, 0, 6, 'D')

# Add a snow load of 10 kN/m to the beam
simple_beam.add_member_dist_load('M1', 'Fy', -5, -5, 0, 6, 'S')

# Add point loads at different positions
# simple_beam.add_member_pt_load(member_id, direction, P, x, case)
simple_beam.add_member_pt_load('M1', 'Fy', -10, 3, 'D')  # 50 kN Dead load at midspan (3 meters)
simple_beam.add_member_pt_load('M1', 'Fy', 10, 1.5, 'L')  # 50 kN Live load at quarter span (1.5 meters)
simple_beam.add_member_pt_load('M1', 'Fy', -2.5, 4.5, 'L')  # -2.5 kN Live load at three-quarter span (4.5 meters)

# Add load combinations
# simple_beam.add_load_combo(name, factors)
simple_beam.add_load_combo('1.4D', {'D': 1.4})
simple_beam.add_load_combo('1.2D+1.6L', {'D': 1.2, 'L': 1.6})
simple_beam.add_load_combo('1.2D+1.6L+0.5S', {'D': 0.5, 'L': 1.6, 'S': 0.5})

# Analyze the beam and perform a statics check
simple_beam.analyze(check_statics=True)

Visualization.render_model(simple_beam, annotation_size=0.1, deformed_shape=True, deformed_scale=10, render_loads=True, combo_name='1.2D+1.6L')

# Plot the moment diagram with all load cases and max/min envelope
x, M1 = simple_beam.Members['M1'].moment_array("Mz", n_points=400, combo_name='1.4D')
_, M2 = simple_beam.Members['M1'].moment_array("Mz", n_points=400, combo_name='1.2D+1.6L')
_, M3 = simple_beam.Members['M1'].moment_array("Mz", n_points=400, combo_name='1.2D+1.6L+0.5S')

max_envelope = np.maximum(np.maximum(M1, M2), M3)
min_envelope = np.minimum(np.minimum(M1, M2), M3)

plt.plot(x, np.zeros(len(x)), c="black", lw=3)
plt.plot(x, M1, label='1.4D')
plt.plot(x, M2, label='1.2D+1.6L')
plt.plot(x, M3, label='1.2D+1.6L+0.5S')
plt.plot(x, max_envelope, alpha=0.3, c="green", lw=5, label='Max Envelope')
plt.plot(x, min_envelope, alpha=0.3, c="red", lw=5, label='Min Envelope')
plt.legend()
plt.xlabel('Position along the beam (meters)')
plt.ylabel('Moment (kN-m)')
plt.title('Moment Diagram')
plt.show()