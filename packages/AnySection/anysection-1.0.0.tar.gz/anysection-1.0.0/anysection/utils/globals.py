class Globals:
    """
    This class contains global constants used throughout the AnySection library.
    """

    # Precision tolerances
    ZERO = 1e-6               # General zero tolerance
    E_TOL = 1e-5              # Tolerance for strain calculations
    N_TOL = 1e-5              # Tolerance for axial force calculations
    D_TOL = 1e-5              # Tolerance for displacement or distance calculations
    TOL_MP = 1e-3             # Tolerance for moment calculations

    # Brent Solver settings
    MAX_EVALS = 1000          # Maximum evaluations for Brent solver
    EXP_START_NA = 5          # Starting exponent for neutral axis search
    EXP_START_NE = 5          # Starting exponent for eccentricity search
    EXP_START_NU = 5          # Starting exponent for angle search

    # Integration constants
    PI = 3.141592653589793    # Pi constant
    DEG_TO_RAD = PI / 180.0   # Degrees to radians conversion
    RAD_TO_DEG = 180.0 / PI   # Radians to degrees conversion

    # Other constants
    INF = float('inf')        # Representation of infinity
    NEG_INF = float('-inf')   # Representation of negative infinity

    @staticmethod
    def is_close(a, b, tol=ZERO):
        """
        Check if two values are approximately equal within a specified tolerance.

        Parameters:
            a (float): First value.
            b (float): Second value.
            tol (float): Tolerance.

        Returns:
            bool: True if values are close, False otherwise.
        """
        return abs(a - b) <= tol

    @staticmethod
    def clamp(value, min_value, max_value):
        """
        Clamp a value between a minimum and maximum.

        Parameters:
            value (float): The value to clamp.
            min_value (float): Minimum allowed value.
            max_value (float): Maximum allowed value.

        Returns:
            float: Clamped value.
        """
        return max(min(value, max_value), min_value)
