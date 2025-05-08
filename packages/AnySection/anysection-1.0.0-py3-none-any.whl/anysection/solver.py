# anysection/solvers/section_solver.py

import numpy as np

class SectionSolver:
    """
    Class to perform section analysis to determine axial forces, moments,
    and moment-curvature relationships using iterative solvers.
    """

    def __init__(self, section):
        """
        Initialize the SectionSolver.

        Parameters:
            section (Section): The section object to analyze.
        """
        self.section = section

    def calculate_axial_force(self, neutral_axis, curvature):
        """
        Calculate the axial force in the section for a given neutral axis position and curvature.

        Parameters:
            neutral_axis (float): Position of the neutral axis.
            curvature (float): Curvature applied to the section.

        Returns:
            float: Total axial force.
        """
        total_force = 0.0

        # Iterate through fibers in the section
        for fiber in self.section.fibers:
            # Calculate strain in the fiber based on curvature and neutral axis
            strain = curvature * (fiber.y - neutral_axis)
            stress = fiber.material.stress(strain)
            force = stress * fiber.area
            total_force += force

        return total_force

    def calculate_moment_capacity(self, curvature):
        """
        Calculate the bending moment capacity of the section for a given curvature.

        Parameters:
            curvature (float): Curvature applied to the section.

        Returns:
            float: Total bending moment.
        """
        total_moment = 0.0
        neutral_axis = self.section.centroid()[1]  # Use section centroid as neutral axis

        # Iterate through fibers in the section
        for fiber in self.section.fibers:
            strain = curvature * (fiber.y - neutral_axis)
            stress = fiber.material.stress(strain)
            force = stress * fiber.area
            moment_arm = fiber.y - neutral_axis
            total_moment += force * moment_arm

        return total_moment

    def moment_curvature_analysis(self, curvature_range, axial_force=0.0):
        """
        Perform moment-curvature analysis for a specified axial force.

        Parameters:
            curvature_range (iterable): List or array of curvature values.
            axial_force (float): Applied axial force (positive = compression).

        Returns:
            list: List of (curvature, moment) tuples.
        """
        results = []

        for curvature in curvature_range:
            try:
                neutral_axis = self.find_neutral_axis(axial_force, curvature)
                moment = self.calculate_moment_capacity(curvature, neutral_axis)
                results.append((curvature, moment))
            except Exception as e:
                print(f"⚠️ Curvature {curvature:.5f} failed: {e}")
                results.append((curvature, None))

        return results

    def calculate_moment_capacity(self, curvature, neutral_axis):
        """
        Calculate bending moment for a given curvature and neutral axis.

        Parameters:
            curvature (float): Section curvature.
            neutral_axis (float): Position of the neutral axis.

        Returns:
            float: Resulting moment.
        """
        total_moment = 0.0

        for fiber in self.section.fibers:
            strain = curvature * (fiber.y - neutral_axis)
            stress = fiber.material.stress(strain)
            force = stress * fiber.area
            lever_arm = fiber.y - neutral_axis
            total_moment += force * lever_arm

        return total_moment

    def find_neutral_axis(self, target_axial_force, curvature, tolerance=1e-6, max_iter=100):
        """
        Find the neutral axis depth that satisfies the target axial force.

        Parameters:
            target_axial_force (float): Applied axial force.
            curvature (float): Section curvature.
            tolerance (float): Convergence tolerance.
            max_iter (int): Max iterations.

        Returns:
            float: Neutral axis position.
        """
        y_min = min(fiber.y for fiber in self.section.fibers)
        y_max = max(fiber.y for fiber in self.section.fibers)

        low = y_min
        high = y_max

        for _ in range(max_iter):
            mid = (low + high) / 2
            axial = self.calculate_axial_force(mid, curvature)

            if abs(axial - target_axial_force) < tolerance:
                return mid
            elif axial > target_axial_force:
                low = mid
            else:
                high = mid

        raise ValueError("Neutral axis not found (max iterations reached)")

    def interaction_curve(self, neutral_axis_range):
        """
        Generate the interaction curve (axial force vs. bending moment).

        Parameters:
            neutral_axis_range (tuple): (min, max) range for the neutral axis.

        Returns:
            list: List of (axial_force, bending_moment) tuples.
        """
        results = []
        min_na, max_na = neutral_axis_range
        steps = 50
        delta = (max_na - min_na) / steps

        for i in range(steps + 1):
            na_pos = min_na + i * delta
            axial_force = self.calculate_axial_force(na_pos, curvature=0.002)
            bending_moment = self.calculate_moment_capacity(curvature=0.002)
            results.append((axial_force, bending_moment))

        return results

    def __str__(self):
        return f"SectionSolver for {self.section.name}"


