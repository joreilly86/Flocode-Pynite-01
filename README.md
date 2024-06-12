# Flocode #034 - Pynite 01: Introduction to Finite Element Models in Python

This repository contains a simple example of using the PyNite library to perform finite element analysis (FEA) on a beam with both point and distributed loads. The example demonstrates how to set up the model, apply loads, perform the analysis, and visualize the results.

## Prerequisites

- Python ^3.11
- Poetry for dependency management, my preferred choice
- I also added a `requirements.txt` file for the pip users

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/joreilly86/Flocode-034-Pynite-01.git
   cd Flocode-034-Pynite-01
   ```

2. **Install dependencies using Poetry**:
   ```sh
   poetry install
   ```

3. **Activate the Poetry environment**:
   ```sh
   poetry shell
   ```

Certainly! Here's the revised section:

## Running the Example

I like to use Jupyter Notebooks, but you can choose to use a script or a notebook, whichever you prefer.

### Running as a Script

To run the example script, execute the following command:
```sh
poetry run python example.py
```

### Running in a Jupyter Notebook

1. **Ensure you have Jupyter installed**:
   ```sh
   poetry add notebook
   ```

2. **Start Jupyter Notebook**:
   ```sh
   poetry run jupyter notebook
   ```

3. **Create a new notebook and copy the example code into a cell**:
   - Open the newly created notebook in your browser.
   - Copy the example code into a cell.
   - Run the cell to execute the code.

This way, you can run the example either as a standalone script or interactively in a Jupyter notebook, based on your preference.

## Code Explanation

### Importing Libraries

```python
from PyNite import FEModel3D
from matplotlib import pyplot as plt
import numpy as np
from PyNite import Visualization
import pyvista as pv
```

### Creating the Finite Element Model

```python
simple_beam = FEModel3D()
```
Creates a new finite element model object.

### Adding Nodes

```python
simple_beam.add_node('N1', 0, 0, 0)
simple_beam.add_node('N2', 6, 0, 0)  # 6 meters
```
- `add_node(name, x, y, z)`: Adds a node to the model.
  - `name` (str): The node identifier.
  - `x` (float): The x-coordinate of the node.
  - `y` (float): The y-coordinate of the node.
  - `z` (float): The z-coordinate of the node.

### Defining a Material

```python
E = 210000  # Modulus of elasticity (MPa)
G = 81000   # Shear modulus of elasticity (MPa)
nu = 0.3    # Poisson's ratio
rho = 7.85  # Density (kg/m^3)
simple_beam.add_material('Steel', E, G, nu, rho)
```
- `add_material(name, E, G, nu, rho)`: Defines a material and adds it to the model.
  - `name` (str): The material name.
  - `E` (float): Modulus of elasticity in MPa.
  - `G` (float): Shear modulus in MPa.
  - `nu` (float): Poisson's ratio.
  - `rho` (float): Density in kg/m³.

### Adding a Beam

```python
simple_beam.add_member('M1', 'N1', 'N2', 'Steel', 1.2e-4, 1.6e-4, 2.7e-4, 0.025)
```
- `add_member(name, i_node, j_node, material, Iy, Iz, J, A)`: Adds a beam member to the model.
  - `name` (str): The member identifier.
  - `i_node` (str): The start node identifier.
  - `j_node` (str): The end node identifier.
  - `material` (str): The material name.
  - `Iy` (float): Moment of inertia about the y-axis in m⁴.
  - `Iz` (float): Moment of inertia about the z-axis in m⁴.
  - `J` (float): Torsional constant in m⁴.
  - `A` (float): Cross-sectional area in m².

### Defining Supports

```python
simple_beam.def_support('N1', True, True, True, False, False, False)
simple_beam.def_support('N2', True, True, True, True, False, False)
```
- `def_support(node_id, u1, u2, u3, r1, r2, r3)`: Defines support conditions at a node.
  - `node_id` (str): The node identifier.
  - `u1` (bool): Restraint in the x direction.
  - `u2` (bool): Restraint in the y direction.
  - `u3` (bool): Restraint in the z direction.
  - `r1` (bool): Restraint about the x-axis rotation.
  - `r2` (bool): Restraint about the y-axis rotation.
  - `r3` (bool): Restraint about the z-axis rotation.

### Adding Loads

#### Distributed Load

```python
simple_beam.add_member_dist_load('M1', 'Fy', -30, -30, 0, 6, 'D')
```
- `add_member_dist_load(member, direction, w1, w2, x1, x2, case)`: Adds a distributed load to a member.
  - `member` (str): The member identifier.
  - `direction` (str): The direction of the load ('Fx', 'Fy', 'Fz').
  - `w1` (float): The load intensity at the start of the load in kN/m.
  - `w2` (float): The load intensity at the end of the load in kN/m.
  - `x1` (float): The start position of the load along the member length in meters.
  - `x2` (float): The end position of the load along the member length in meters.
  - `case` (str): Load case identifier.

#### Point Loads

```python
simple_beam.add_member_pt_load('M1', 'Fy', -10, 3, 'D')
simple_beam.add_member_pt_load('M1', 'Fy', 45, 1.5, 'L')
simple_beam.add_member_pt_load('M1', 'Fy', -20, 4.5, 'L')
```
- `add_member_pt_load(member, direction, P, x, case)`: Adds a point load to a member.
  - `member` (str): The member identifier.
  - `direction` (str): The direction of the load ('Fx', 'Fy', 'Fz').
  - `P` (float): The load magnitude in kN.
  - `x` (float): The position of the load along the member length in meters.
  - `case` (str): Load case identifier.

### Adding Load Combinations

```python
simple_beam.add_load_combo('1.4D', {'D': 1.4})
simple_beam.add_load_combo('1.2D+1.6L', {'D': 1.2, 'L': 1.6})
simple_beam.add_load_combo('1.2D+1.6L+0.5S', {'D': 0.5, 'L': 1.6, 'S': 0.5})
```
- `add_load_combo(name, factors)`: Adds a load combination.
  - `name` (str): The load combination name.
  - `factors` (dict): A dictionary of load cases and their factors.

### Analyzing the Model

```python
simple_beam.analyze(check_statics=True)
```
- `analyze(check_statics)`: Analyzes the model.
  - `check_statics` (bool): If `True`, performs a statics check.

### Visualization

#### Set PyVista Jupyter Backend

```python
pv.set_jupyter_backend('static')  # Use 'static' backend for simplicity
```
Sets the PyVista backend for rendering in Jupyter notebooks.

#### Render Model

```python
Visualization.render_model(simple_beam, annotation_size=0.1, deformed_shape=True, deformed_scale=0.1, render_loads=True, combo_name='1.2D+1.6L')
```
- `render_model(model, annotation_size, deformed_shape, deformed_scale, render_loads, combo_name)`: Renders the finite element model.
  - `model` (FEModel3D): The finite element model to render.
  - `annotation_size` (float): Size of the annotations.
  - `deformed_shape` (bool): Whether to render the deformed shape.
  - `deformed_scale` (float): Scale factor for the deformed shape.
  - `render_loads` (bool): Whether to render the loads.
  - `combo_name` (str): Load combination to use for rendering.

### Plotting Moment Diagram

```python
x, M1 = simple_beam.Members['M1'].moment_array("Mz", n_points=400, combo_name='1.4D')
_, M2 = simple_beam.Members['M1'].moment_array("Mz", n_points=400, combo_name='1.2D+1.6L')
_, M3 = simple_beam.Members['M1'].moment_array("Mz", n_points=400, combo_name='1.2D+1.6L+0.5S')

max_envelope = np.maximum(np.maximum(M1, M2), M3)
min_envelope = np.minimum(np.minimum(M1, M2), M3)

plt.plot(x, np.zeros(len(x)), c="black", lw=

3)
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
```
- `moment_array(direction, n_points, combo_name)`: Returns the moment array for a member.
  - `direction` (str): The direction of the moment ('Mx', 'My', 'Mz').
  - `n_points` (int): Number of points along the member length to calculate the moment.
  - `combo_name` (str): Load combination name.

## Follow flocode

For more tutorials and updates, follow flocode on:

- [**Newsletter**](https://flocode.substack.com/)
- [**YouTube**](https://www.youtube.com/channel/UC51qm0xOHhJRImfKNwfH_Qw)
- [**LinkedIn**](https://www.linkedin.com/in/james-o-reilly-engineering/)
- [**Twitter**](http://x.com/flocode_dev)

See you in the next one.

James 🌊
