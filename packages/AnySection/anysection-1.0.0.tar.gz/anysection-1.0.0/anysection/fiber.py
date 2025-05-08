class Fiber:
    """
    Represents a fiber in a section, with area and material properties.
    """

    def __init__(self, area, x, y, material):
        self.area = area  # Area of the fiber
        self.x = x        # X-coordinate of the fiber centroid
        self.y = y        # Y-coordinate of the fiber centroid
        self.material = material  # Associated material object

    def stress(self, strain):
        """
        Calculate stress based on the material's stress-strain relationship.
        """
        return self.material.stress(strain)

    def force(self, strain):
        """
        Calculate force in the fiber as stress * area.
        """
        return self.stress(strain) * self.area

    def centroid(self):
        """
        Return the centroid of the fiber.
        """
        return self.x, self.y

    def __str__(self):
        return f"Fiber at ({self.x}, {self.y}) with area {self.area} and material {self.material.name}"
