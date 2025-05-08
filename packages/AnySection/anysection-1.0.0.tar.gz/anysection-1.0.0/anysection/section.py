from anysection.area import CompositeArea
from anysection.fiber import Fiber
class Section:
    """
    Class representing a structural section composed of fibers.
    """

    def __init__(self, name):
        self.name = name
        self.fibers = []  # List to store fiber objects
        self.composite_area = CompositeArea()

    def add_fiber(self, area, x, y, material):
        """
        Add a fiber to the section.

        Parameters:
            area (float): Area of the fiber.
            x (float): X-coordinate of the fiber centroid.
            y (float): Y-coordinate of the fiber centroid.
            material (Material): Material object (Concrete, Steel, etc.)
        """
        fiber = Fiber(area, x, y, material)
        self.fibers.append(fiber)
        self.composite_area.add_area(fiber, dx=0, dy=0)

    def add_area(self, area_obj, dx=0, dy=0):
        """
        Add an area object (CompositeArea, Rectangle, Circle, etc.) to the section.

        Parameters:
            area_obj (Area): An area object that has an `area()` and `centroid()` method.
            dx (float): Shift in x-direction.
            dy (float): Shift in y-direction.
        """
        self.composite_area.add_area(area_obj, dx=dx, dy=dy)

    def total_area(self):
        """
        Calculate the total area of the section.
        """
        return self.composite_area.area()

    def centroid(self):
        """
        Calculate the centroid of the section.
        """
        return self.composite_area.centroid()

    def moment_of_inertia(self):
        """
        Calculate the moment of inertia of the section.
        """
        return self.composite_area.moment_of_inertia()

    def __str__(self):
        return f"Section: {self.name}, Total Area: {self.total_area()}"
