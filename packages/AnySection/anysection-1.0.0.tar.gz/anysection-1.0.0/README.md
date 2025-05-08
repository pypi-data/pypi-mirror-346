# 📐 **AnySection** – Reinforced Concrete Section Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()

---

## 📊 **Overview**

**AnySection** is a Python library for reinforced concrete section analysis. It provides tools for modeling, analyzing, and visualizing the structural behavior of reinforced concrete sections using material nonlinearities and fiber-based analysis methods.

Key features include:

- ✅ Support for **Concrete_NonlinearEC2** and **Steel_Bilinear** material models.
- ✅ Fiber-based **moment-curvature** analysis.
- ✅ Calculation of **axial forces**, **bending moments**, and **neutral axis** positions.
- ✅ Generate **moment-curvature diagrams** and plot **section views**.
- ✅ Extensible architecture for adding custom materials and solvers.

---

## 📁 **Project Structure**
```
AnySection/
│
├── anysection/              # Main package
│   ├── __init__.py
│   ├── geometry/            # Geometrical objects (Area, Fiber, Points)
│   │   └── area.py
│   │
│   ├── materials/           # Material models
│   │   └── material.py
│   │
│   ├── sections/            # Section definitions and properties
│   │   └── section.py
│   │
│   ├── solvers/             # Section analysis solvers
│   │   └── section_solver.py
│   │
│   └── utils/               # Utility classes (constants, helpers)
│       └── globals.py
│
├── examples/                # Example usage
│   └── example1.py
│
├── setup.py                 # Build configuration
├── requirements.txt         # Dependencies
├── README.md                 # 📖 You are here
└── LICENSE                   # MIT License
```

---

## ⚙️ **Installation**

### 🔹 **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/anysection.git
cd anysection
```

### 🔹 **2. Install Dependencies**

```bash
pip install -r requirements.txt
```
### 🔹 3. Install the Library Locally
```bash
pip install -e .
```
This installs the package in editable mode for local development.

🧮 Quick Start Example
```python

import matplotlib.pyplot as plt
import numpy as np
from anysection.materials import Concrete_NonlinearEC2, Steel_Bilinear
from anysection.sections import Section
from anysection.solvers import SectionSolver

# Define Materials
concrete = Concrete_NonlinearEC2(fcm=20e6, ec1=0.002, ecu1=0.0035)  # C20/25 Concrete
steel = Steel_Bilinear(Es=200e9, fy=500e6)  # Reinforcement Steel

# Create a Section
section = Section("Rectangular Beam")
section.add_fiber(area=0.01, x=0.0, y=0.0, material=concrete)
section.add_fiber(area=0.01, x=0.1, y=0.0, material=concrete)
section.add_fiber(area=0.01, x=0.0, y=0.1, material=concrete)
section.add_fiber(area=0.01, x=0.1, y=0.1, material=concrete)

# Initialize Solver
solver = SectionSolver(section)

# Analyze Moment-Curvature
curvatures = np.linspace(0, 0.02, 100)
moments = [solver.calculate_moment_capacity(c) for c in curvatures]

# Plot Moment-Curvature Diagram
plt.plot(curvatures, moments)
plt.xlabel('Curvature (1/m)')
plt.ylabel('Moment (Nm)')
plt.title('Moment-Curvature Diagram')
plt.grid(True)
plt.show()
```

## 📐 Features
🏗️ **Section Modeling:** Fiber-based section modeling for reinforced concrete.

📊 **Moment-Curvature Analysis:** Plot moment-curvature behavior for reinforced sections.


**📏 Material Models:**
- Concrete_NonlinearEC2 (Nonlinear EC2 behavior for concrete)

- Steel_Bilinear (Bilinear elastic-plastic model for reinforcement)


📈 **Customizable Solvers:** Easily extend the library with new solvers and materials.


## 🛠️ Contributing
Contributions are welcome! 🚀 Feel free to fork the repository, submit issues, and create pull requests.

📢 To contribute:
```bash
Fork the repository.
Create a new branch: git checkout -b feature/my-feature
Commit your changes: git commit -m 'Add new feature'
Push to the branch: git push origin feature/my-feature
Open a Pull Request ✅
```

## 📄 **License**

This project is licensed under the MIT License.

## 🌐 **Links**
📚 **Documentation:** *Coming Soon*

🐛 **Issue Tracker:** *GitHub Issues*

🏗️ **PyPI**: *Coming Soon*

**Citation**:
If you use AnySection in your research, please cite the following paper:

```bibtex
Papanikolaou, Vassilis. (2019). AnySection : Software for the analysis of arbitrary composite sections in biaxial bending and axial load. 
```