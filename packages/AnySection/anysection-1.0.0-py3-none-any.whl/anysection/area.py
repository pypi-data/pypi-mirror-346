from math import pi
from anysection.fiber import Fiber


class Area:
    """
    Base class representing a geometric area.
    """
    def __init__(self, name, centroid_x=0.0, centroid_y=0.0):
        self.name = name
        self.centroid_x = centroid_x
        self.centroid_y = centroid_y

    def area(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def centroid(self):
        return self.centroid_x, self.centroid_y

    def moment_of_inertia(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def __str__(self):
        return f"Area: {self.name}, Centroid: ({self.centroid_x}, {self.centroid_y})"


class Rectangle(Area):
    def __init__(self, width, height, centroid_x=0.0, centroid_y=0.0):
        super().__init__("Rectangle", centroid_x, centroid_y)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def moment_of_inertia(self):
        Ix = (self.width * self.height ** 3) / 12
        Iy = (self.height * self.width ** 3) / 12
        return Ix, Iy


class Circle(Area):
    def __init__(self, radius, centroid_x=0.0, centroid_y=0.0):
        super().__init__("Circle", centroid_x, centroid_y)
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2

    def moment_of_inertia(self):
        I = (pi * self.radius ** 4) / 4
        return I, I


class Triangle(Area):
    def __init__(self, base, height, centroid_x=0.0, centroid_y=0.0):
        super().__init__("Triangle", centroid_x, centroid_y)
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def moment_of_inertia(self):
        Ix = (self.base * self.height ** 3) / 36
        Iy = (self.height * self.base ** 3) / 36
        return Ix, Iy


class CompositeArea(Area):
    def __init__(self):
        super().__init__("Composite")
        self.components = []

    def add_area(self, area, dx=0, dy=0):
        self.components.append((area, dx, dy))

    def area(self):
        _sum = 0
        for component in self.components:
            if isinstance(component[0], Fiber):
                _sum += component[0].area
            else:
                _sum += component[0].area()
        return _sum

    def centroid(self):
        Ax_sum = 0
        Ay_sum = 0
        A_total = self.area()

        for comp, dx, dy in self.components:
            if isinstance(comp, Fiber):
                A = comp.area
            else:
                A = comp.area()
            cx, cy = comp.centroid()
            Ax_sum += A * (cx + dx)
            Ay_sum += A * (cy + dy)

        return Ax_sum / A_total, Ay_sum / A_total

    def moment_of_inertia(self):
        Ix_total = 0
        Iy_total = 0
        cx_total, cy_total = self.centroid()

        for comp, dx, dy in self.components:
            A = comp.area()
            cx, cy = comp.centroid()
            dx_total = cx + dx - cx_total
            dy_total = cy + dy - cy_total

            Ix, Iy = comp.moment_of_inertia()

            Ix_total += Ix + A * dy_total ** 2
            Iy_total += Iy + A * dx_total ** 2

        return Ix_total, Iy_total


class Tee(CompositeArea):
    """
    T-section composed of a flange and web.

    Parameters:
        bf: Flange width
        hf: Flange height
        bw: Web width
        hw: Web height
    """
    def __init__(self, bf, hf, bw, hw):
        super().__init__()
        self.bf = bf
        self.hf = hf
        self.bw = bw
        self.hw = hw

        # Flange at the top
        flange = Rectangle(width=bf, height=hf)
        flange_centroid_y = hf / 2 + hw  # from bottom
        self.add_area(flange, dx=0, dy=hw)

        # Web at the bottom
        web = Rectangle(width=bw, height=hw)
        web_centroid_x = (bf - bw) / 2  # center the web
        web_centroid_y = hw / 2
        self.add_area(web, dx=web_centroid_x, dy=0)
