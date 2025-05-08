from math import sqrt, pow
from enum import Enum
from dataclasses import dataclass
import numpy as np

class ModelType(Enum):
    """
    Enumeration of available material model types for concrete, steel, and FRP.
    """
    CONCRETE_PARABOLIC_LINEAR_EC2 = "Concrete_ParabolicLinearEC2"
    CONCRETE_Nonlinear_EC2 = "Concrete_NonlinearEC2"
    CONCRETE_POPOVICS = "Concrete_Popovics"
    CONCRETE_PARABOLIC_LINEAR_GENERAL = "Concrete_ParabolicLinearGeneral"
    CONCRETE_PARABOLIC_LINEAR_FRC = "Concrete_ParabolicLinearFRC"
    CONCRETE_MC90_GENERAL = "Concrete_MC90General"
    CONCRETE_CONFINED_KAPPOS = "Concrete_ConfinedKappos"
    CONCRETE_CONFINED_SPOELSTRA = "Concrete_ConfinedSpoelstra"
    STEEL_BILINEAR = "Steel_Bilinear"
    STEEL_PARK_SAMPSON = "Steel_ParkSampson"
    FRP_LINEAR = "FRP_Linear"


class Material:
    """
    Abstract base class for all material models.
    """

    def __init__(self, name):
        """
        Initialize a material with a given name.

        Args:
            name (str): The name of the material model.
        """
        self.name = name

    def stress(self, strain):
        """
        Calculate stress based on strain.

        Args:
            strain (float): Input strain.

        Returns:
            float: Computed stress.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def is_failure(self, strain):
        """
        Determine if the material has failed at the given strain.

        Args:
            strain (float): Input strain.

        Returns:
            bool: True if failed, False otherwise.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def __str__(self):
        return f"Material: {self.name}"


# ----------------- CONCRETE MATERIALS ----------------- #

class Concrete_NonlinearEC2(Material):
    """
    EC2 nonlinear concrete model (parabolic up to ec1, then constant).

    Args:
        fcm (float): Mean compressive strength [Pa].
        ec1 (float): Strain at peak stress.
        ecu1 (float): Ultimate strain.
    """
    def __init__(self, fcm, ec1, ecu1):
        super().__init__("Concrete_NonlinearEC2")
        self.fcm = fcm
        self.ec1 = ec1
        self.ecu1 = ecu1
        self.Ec = 22000 * pow(fcm / 10, 0.3)

    def stress(self, strain):
        if strain >= 0:
            return 0
        elif abs(strain) <= self.ec1:
            return self.fcm * (2 * (abs(strain) / self.ec1) - pow(abs(strain) / self.ec1, 2))
        elif abs(strain) <= self.ecu1:
            return self.fcm
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.ecu1


class Concrete_ParabolicLinearEC2(Material):
    def __init__(self, fck, acc, gc, ec2, ecu2, n):
        super().__init__("Concrete_ParabolicLinearEC2")
        self.fck = fck
        self.acc = acc
        self.gc = gc
        self.ec2 = ec2
        self.ecu2 = ecu2
        self.n = n

    def stress(self, strain):
        if strain >= 0:
            return 0
        elif abs(strain) <= self.ec2:
            return self.acc * self.fck / self.gc * (1 - pow((1 - abs(strain) / self.ec2), self.n))
        elif abs(strain) <= self.ecu2:
            return self.acc * self.fck / self.gc
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.ecu2


class Concrete_Popovics(Material):
    def __init__(self, Eco, fc, ec, ecu):
        super().__init__("Concrete_Popovics")
        self.Eco = Eco
        self.fc = fc
        self.ec = ec
        self.ecu = ecu

    def stress(self, strain):
        if strain >= 0:
            return 0
        abs_strain = abs(strain)
        r = self.Eco / (self.Eco - self.fc / self.ec)
        if abs_strain <= self.ec:
            return self.fc * (r * abs_strain / self.ec) / (r - 1 + pow(abs_strain / self.ec, r))
        elif abs_strain <= self.ecu:
            return self.fc * (1 - ((abs_strain - self.ec) / (self.ecu - self.ec)))
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.ecu


class Concrete_ParabolicLinearGeneral(Material):
    def __init__(self, Ec, fc, eco, ecu, slope, ft, etu):
        super().__init__("Concrete_ParabolicLinearGeneral")
        self.Ec = Ec
        self.fc = fc
        self.eco = eco
        self.ecu = ecu
        self.slope = slope
        self.ft = ft
        self.etu = etu

    def stress(self, strain):
        if strain >= 0:
            return min(self.Ec * strain, self.ft) if strain <= self.etu else 0
        elif abs(strain) <= self.eco:
            return self.fc * (2 * (abs(strain) / self.eco) - pow(abs(strain) / self.eco, 2))
        elif abs(strain) <= self.ecu:
            return self.fc * (1 - ((abs(strain) - self.eco) / (self.ecu - self.eco)))
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.ecu


class Concrete_ParabolicLinearFRC(Material):
    def __init__(self, Ec, fc, eco, ecu, ft, s2, e2, s3, e3):
        super().__init__("Concrete_ParabolicLinearFRC")
        self.Ec = Ec
        self.fc = fc
        self.eco = eco
        self.ecu = ecu
        self.ft = ft
        self.s2 = s2
        self.e2 = e2
        self.s3 = s3
        self.e3 = e3

    def stress(self, strain):
        if strain >= 0:
            if strain <= self.e2:
                return self.ft + (self.s2 - self.ft) * (strain / self.e2)
            elif strain <= self.e3:
                return self.s2 + (self.s3 - self.s2) * ((strain - self.e2) / (self.e3 - self.e2))
            else:
                return 0
        elif abs(strain) <= self.eco:
            return self.fc * (2 * (abs(strain) / self.eco) - pow(abs(strain) / self.eco, 2))
        elif abs(strain) <= self.ecu:
            return self.fc * (1 - ((abs(strain) - self.eco) / (self.ecu - self.eco)))
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.ecu


class Concrete_MC90General(Material):
    def __init__(self, fcm, ecu, ft, etu):
        super().__init__("Concrete_MC90General")
        self.fcm = fcm
        self.ecu = ecu
        self.ft = ft
        self.etu = etu

    def stress(self, strain):
        if strain >= 0:
            return min(self.ft * (1 - (strain / self.etu)), self.ft) if strain <= self.etu else 0
        elif abs(strain) <= self.ecu:
            return self.fcm * (1 - (abs(strain) / self.ecu))
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.ecu


class Concrete_ConfinedKappos(Material):
    def __init__(self, fc, eco, rw, bc, s, fyw, HoopType):
        super().__init__("Concrete_ConfinedKappos")
        self.fc = fc
        self.eco = eco
        self.rw = rw
        self.bc = bc
        self.s = s
        self.fyw = fyw
        self.HoopType = HoopType

    def stress(self, strain):
        k = 1 + 0.5 * self.rw * (self.fyw / self.fc)
        if strain <= self.eco:
            return self.fc * k * (strain / self.eco)
        elif strain <= self.eco * 1.5:
            return self.fc * k
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.eco * 2


class Concrete_ConfinedSpoelstra(Material):
    def __init__(self, D, tj, fco, fju, Ej, eco):
        super().__init__("Concrete_ConfinedSpoelstra")
        self.D = D
        self.tj = tj
        self.fco = fco
        self.fju = fju
        self.Ej = Ej
        self.eco = eco

    def stress(self, strain):
        flu = 2 * self.tj * self.fju / (self.D + 2 * self.tj)
        fcc = self.fco * (2.254 * sqrt(1 + 7.94 * flu / self.fco) - 2 * flu / self.fco - 1.254)
        if strain <= self.eco:
            return fcc * (strain / self.eco)
        elif strain <= self.eco * 1.5:
            return fcc
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.eco * 2



# ----------------- STEEL MATERIALS ----------------- #

class Steel_Bilinear(Material):
    def __init__(self, Es, fy, euk):
        super().__init__("Steel_Bilinear")
        self.Es = Es
        self.fy = fy
        self.euk = euk
        self.ey = fy / Es

    def stress(self, strain):
        abs_strain = abs(strain)
        if abs_strain <= self.ey:
            return self.Es * strain
        elif abs_strain <= self.euk:
            return self.fy * (1 if strain > 0 else -1)
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.euk


class Steel_ParkSampson(Material):
    def __init__(self, Es, fy, fu, esh, esu):
        super().__init__("Steel_ParkSampson")
        self.Es = Es
        self.fy = fy
        self.fu = fu
        self.esh = esh
        self.esu = esu
        self.ey = fy / Es

    def stress(self, strain):
        abs_strain = abs(strain)
        if abs_strain <= self.ey:
            return self.Es * strain
        elif abs_strain <= self.esh:
            return self.fy * (1 if strain > 0 else -1)
        elif abs_strain <= self.esu:
            r = self.esu - self.esh
            rr = abs_strain - self.esh
            m = ((self.fu / self.fy) * pow(30 * r + 1, 2) - 60 * r - 1) / (15 * r * r)
            return self.fy * ((m * rr + 2) / (60 * rr + 2) + (rr * (60 - m)) / (2 * pow(30 * r + 1, 2)))
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.esu


# ----------------- FRP MATERIALS ----------------- #

class FRP_Linear(Material):
    def __init__(self, Es, euk, gs):
        super().__init__("FRP_Linear")
        self.Es = Es
        self.euk = euk
        self.gs = gs

    def stress(self, strain):
        if abs(strain) <= self.euk / self.gs:
            return self.Es / self.gs * strain
        else:
            return 0

    def is_failure(self, strain):
        return abs(strain) > self.euk / self.gs


# ----------------- MATERIAL FACTORY ----------------- #

class MaterialFactory:
    @staticmethod
    def create_material(material_type, *args):
        material_classes = {
            "Concrete_NonlinearEC2": Concrete_NonlinearEC2,
            "Concrete_ParabolicLinearEC2": Concrete_ParabolicLinearEC2,
            "Concrete_Popovics": Concrete_Popovics,
            "Steel_Bilinear": Steel_Bilinear,
            "Steel_ParkSampson": Steel_ParkSampson,
            "FRP_Linear": FRP_Linear
        }

        if material_type not in material_classes:
            raise ValueError(f"Material type '{material_type}' not recognized.")

        return material_classes[material_type](*args)


# ----------------- EXAMPLE USAGE ----------------- #

if __name__ == "__main__":
    # Example for Concrete_NonlinearEC2
    concrete = Concrete_NonlinearEC2(fcm=30e6, ec1=0.002, ecu1=0.0035)
    strain = -0.0035
    print(concrete)
    print(f"Stress at strain {strain}: {concrete.stress(strain)}")
    print(f"Failure: {'Yes' if concrete.is_failure(strain) else 'No'}")

    # Example for Steel_Bilinear
    steel = Steel_Bilinear(Es=200e9, fy=250e6, euk=0.02)
    strain = 0.001
    print(steel)
    print(f"Stress at strain {strain}: {steel.stress(strain)}")
    print(f"Failure: {'Yes' if steel.is_failure(strain) else 'No'}")

    # Example using MaterialFactory
    frp = MaterialFactory.create_material("FRP_Linear", 230e9, 0.015, 1.0)
    strain = 0.012
    print(frp)
    print(f"Stress at strain {strain}: {frp.stress(strain)}")
    print(f"Failure: {'Yes' if frp.is_failure(strain) else 'No'}")
