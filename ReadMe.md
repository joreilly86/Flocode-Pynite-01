# Flocode Newsletter #033

## PyNite Simple Beam Analysis

Welcome to this tutorial on using PyNite for simple beam analysis. In this guide, we'll walk through creating and analyzing a basic beam model. This tutorial is brought to you by [flocode](https://flocode.substack.com/), where we explore coding techniques for engineering applications.

### Objective

This tutorial will guide you through the process of creating a simple beam model, applying loads, performing analysis, and extracting results using the PyNite library.

### Prerequisites

- Python installed on your system.
- Poetry for dependency management.
- Basic understanding of structural analysis and finite element methods.

### Setting Up the Environment

First, ensure you have the required Python packages installed. We will use Poetry for managing dependencies.

1. **Install Poetry**:
   Follow the instructions on the [Poetry website](https://python-poetry.org/docs/#installation) to install Poetry.

2. **Initialize a New Poetry Project**:
   Open a terminal and run:

   ```sh
   poetry init
   ```

   Follow the prompts to configure your project.

3. **Add Dependencies**:
   Add the required packages using Poetry:

   ```sh
   poetry add PyNiteFEA pyvista[all,trame] ipywidgets trame_jupyter_extension
   ```

### Creating the Beam Model

In this section, we will set up the basic structure of the beam model.

#### 1. Importing Libraries and Creating the Model

```python
# Import PyNite correctly
from PyNite import FEModel3D

# Create a new finite element model
model = FEModel3D()
```

- **Import PyNite**: We import the `FEModel3D` class from the PyNite library, which provides the necessary functionality for creating and analyzing finite element models.
- **Create the Model**: An instance of `FEModel3D` is created and named `model`.

#### 2. Defining Beam Properties

```python
# Define the length of the beam
L = 20 * 12  # in (20 feet converted to inches)

# Define the material properties (Steel)
E = 29000   # ksi
G = 11200   # ksi
model.add_material('Steel', E, G, 0.3, 490 / 1000 / 12**3)

# Define the section properties (example values for a W8x35 section)
A = 10.3    # in^2
Iz = 127    # in^4 (strong axis)
Iy = 42.6   # in^4 (weak axis)
J = 0.769   # in^4
```

- **Length of the Beam**: The length of the beam is defined as 20 feet, converted to inches.
- **Material Properties**: Steel properties are defined with Young's modulus \( E \) and shear modulus \( G \). The material is added to the model.
- **Section Properties**: Cross-sectional properties for a W8x35 beam section are defined, including area \( A \), moments of inertia \( I_y \) and \( I_z \), and torsional constant \( J \).

#### 3. Adding Nodes

```python
# Add nodes at the ends of the beam
model.add_node('N1', 0, 0, 0)
model.add_node('N2', L, 0, 0)
```

- **Nodes**: Nodes are added at the ends of the beam, labeled `N1` and `N2`, with their coordinates specified.

#### 4. Defining Supports

```python
# Define fixed supports at both ends
model.def_support('N1', True, True, True, True, True, True)
model.def_support('N2', True, True, True, True, True, True)
```

- **Supports**: Fixed supports are defined at both ends of the beam. The `True` values indicate that the node is restrained in all six degrees of freedom (translations and rotations).

#### 5. Adding Members

```python
# Add a member between the two nodes
model.add_member('M1', 'N1', 'N2', 'Steel', Iy, Iz, J, A)
```

- **Member**: A member is added between nodes `N1` and `N2`. The member is assigned the previously defined material and section properties.

### Applying Loads

Next, we will apply loads to the beam model.

```python
# Add a point load at the midpoint of the beam
model.add_member_pt_load('M1', 'Fy', -50, L / 2)  # 50 kips downward at midspan
```

- **Point Load**: A point load of 50 kips is applied downward at the midpoint of the beam. The load is specified in the global Y direction (`Fy`).

### Performing Analysis

Now, we will analyze the beam model.

```python
# Analyze the model
model.analyze(log=True, check_statics=True)
```

- **Analyze the Model**: The `analyze` method is called to perform the analysis. The `log` parameter enables logging, and `check_statics` checks the static equilibrium of the model.

### Extracting and Printing Results

Finally, we will extract and print the reaction forces, maximum deflection, and moments.

```python
# Extract and print the reaction forces at the supports
print('Reaction Forces at Node N1:')
print('RxnFX:', model.Nodes['N1'].RxnFX)
print('RxnFY:', model.Nodes['N1'].RxnFY)
print('RxnFZ:', model.Nodes['N1'].RxnFZ)

print('Reaction Forces at Node N2:')
print('RxnFX:', model.Nodes['N2'].RxnFX)
print('RxnFY:', model.Nodes['N2'].RxnFY)
print('RxnFZ:', model.Nodes['N2'].RxnFZ)

# Extract and print the maximum deflection and moments in the member
d_max = model.Members['M1'].max_deflection('dy')
M_max = model.Members['M1'].max_moment('Mz')

print('Maximum deflection:', round(d_max, 4), 'in')
print('Maximum moment:', round(M_max), 'k-in')
```

- **Reaction Forces**: Reaction forces at nodes `N1` and `N2` are extracted and printed.
- **Maximum Deflection**: The maximum deflection in the Y direction (`dy`) is extracted and printed.
- **Maximum Moment**: The maximum moment about the Z axis (`Mz`) is extracted and printed.

### Running the Script

To run the script, ensure you are in the correct directory and execute the following command:

```sh
poetry run python example.py
```

This will execute the script and display the results in the terminal.

### Summary

In this tutorial, you learned how to:

- Set up a finite element model using PyNite.
- Define material and section properties.
- Add nodes and members to the model.
- Apply loads and define supports.
- Perform analysis and extract results.

This basic example serves as a foundation for more complex analyses and demonstrates the core functionality of the PyNite library.

### Socials

For more tutorials and updates, follow flocode on:

- [**Newsletter**](https://flocode.substack.com/)
- [**YouTube**](https://www.youtube.com/channel/UC51qm0xOHhJRImfKNwfH_Qw)
- [**LinkedIn**](https://www.linkedin.com/in/james-o-reilly-engineering/)
- [**Twitter**](http://x.com/flocode_dev)