import math

class Axis:
    """
    Represents a coordinate axis defined by its name and orientation angle
    relative to the global x-axis (in degrees).
    """
    def __init__(self, name: str, angle_deg: float):
        self.name = name
        self.angle_rad = math.radians(angle_deg)

    @property
    def unit_vector(self):
        """Returns the unit vector of this axis in global coordinates."""
        return (math.cos(self.angle_rad), math.sin(self.angle_rad))

    def project(self, vector) -> float:
        """
        Projects the given Vector onto this axis and returns the scalar component.
        """
        ux, uy = self.unit_vector
        return vector.x * ux + vector.y * uy


class Vector:
    """
    Represents a vector by magnitude and direction angle relative to
    a reference axis (default: global x-axis).
    """
    def __init__(self, magnitude: float, angle_deg: float, reference: Axis = None):
        self.magnitude = magnitude
        # If a reference axis is provided, offset the angle
        base_angle = reference.angle_rad if reference else 0.0
        self.angle_rad = base_angle + math.radians(angle_deg)

    @property
    def x(self) -> float:
        """X-component in global coordinates."""
        return self.magnitude * math.cos(self.angle_rad)

    @property
    def y(self) -> float:
        """Y-component in global coordinates."""
        return self.magnitude * math.sin(self.angle_rad)

    def __add__(self, other: 'Vector') -> 'Vector':
        """
        Adds two vectors by summing their components and returns
        a new Vector in global coordinates.
        """
        x = self.x + other.x
        y = self.y + other.y
        mag = math.hypot(x, y)
        ang = math.degrees(math.atan2(y, x))
        return Vector(mag, ang)

    def magnitude_direction(self) -> tuple[float, float]:
        """
        Returns (magnitude, direction_degrees) relative to global x-axis.
        """
        mag = math.hypot(self.x, self.y)
        ang = math.degrees(math.atan2(self.y, self.x))
        return mag, ang


def read_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number, please try again.")


def main():
    print("=== Vector Resultant & Resolution Solver ===")
    # Define custom axes if needed
    axes = []
    add_axes = input("Define custom axes for projection? (y/n): ").strip().lower()
    if add_axes == 'y':
        n_axes = int(read_float("Number of axes: "))
        for i in range(n_axes):
            name = input(f"Name of axis {i+1}: ").strip()
            angle = read_float(f"Orientation of '{name}' relative to global x-axis (deg): ")
            axes.append(Axis(name, angle))

    # Read vectors
    vectors = []
    n = int(read_float("Number of vectors to sum: "))
    for i in range(n):
        mag = read_float(f"Magnitude of vector {i+1}: ")
        use_ref = 'n'
        ref_axis = None
        if axes:
            use_ref = input("Is this vector's angle relative to a custom axis? (y/n): ").strip().lower()
            if use_ref == 'y':
                for ax in axes:
                    print(f"- {ax.name}")
                choice = input("Choose axis name: ").strip()
                ref_axis = next((ax for ax in axes if ax.name == choice), None)
                if ref_axis is None:
                    print("Axis not found, defaulting to global x-axis.")
        angle = read_float(f"Angle of vector {i+1} relative to {'axis '+ref_axis.name if ref_axis else 'global x-axis'} (deg): ")
        vectors.append(Vector(mag, angle, reference=ref_axis))

    # Sum vectors
    resultant = Vector(0, 0)
    for v in vectors:
        resultant = resultant + v

    # Output global resultant
    R_mag, R_dir = resultant.magnitude_direction()
    print(f"\nResultant magnitude: {R_mag:.4f}")
    print(f"Resultant direction relative to global x-axis: {R_dir:.2f}°")

    # Project onto custom axes if defined
    if axes:
        print("\nProjections onto custom axes:")
        for ax in axes:
            comp = ax.project(resultant)
            print(f"Component along {ax.name}: {comp:.4f}")


if __name__ == '__main__':
    main()
