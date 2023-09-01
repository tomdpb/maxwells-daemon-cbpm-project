import numpy as np


CONTAINER_COORDINATES = np.array([800, 600])  # x, y
# the daemon will open the gate for a particle when it reaches this speed
SPEED_THRESHHOLD: float = 10.0
GATE_SIZE: int = 100
X, Y = 0, 1  # this is just for ease of reading
PARTICLE_RADIUS: int = 5


class Particle:
    def __init__(self, position: np.ndarray, velocity: np.ndarray, radius: int):
        self.position: np.ndarray = position
        self.velocity: np.ndarray = velocity
        self.radius: int = radius
        self._speed: float = np.linalg.norm(velocity)  # pyright: ignore
        self.isHot: bool = True if abs(self._speed) >= SPEED_THRESHHOLD else False

    def __repr__(self):
        return f"Particle({self.position}, {self.velocity}, {self.radius}, {self._speed}, {self.isHot})"

    def _calculateIsHot(self):
        """Checks and adjusts if the particle is considered hot or not depending on its speed compared to the threshhold."""
        self._speed = np.linalg.norm(self.velocity)  # pyright: ignore
        self.isHot: bool = True if abs(self._speed) >= SPEED_THRESHHOLD else False

    def _bounce(self, coordinate):
        """Inverts the particles velocity at a cartesian coordinate and recalculates the particle's angle."""
        self.velocity[coordinate] *= -1
        self._calculateIsHot()

    def _isAtGateY(self, position):
        """Determines whether a particle is at the gate where it can cross to the other container."""
        # below gate
        if (
            0.5 * (CONTAINER_COORDINATES[Y] + GATE_SIZE)
            <= position + self.radius
            <= CONTAINER_COORDINATES[Y]
        ):
            return False
        # above gate
        elif (
            0 <= position + self.radius <= 0.5 * (CONTAINER_COORDINATES[Y] - GATE_SIZE)
        ):
            return False
        else:
            return True

    def _isAtMiddleX(self, position):
        """Determines whether the particle is close to or at the centre of the container based on its position and velocity."""
        middle = CONTAINER_COORDINATES[X] / 2
        if abs(position - middle) <= self.radius:
            return True
        else:
            return False

    def _isOnCorrectSide(self):
        """Determines whether a particle is on the correct side of the container based on isHot boolean."""
        # hot should be left
        # cold sohuld be right
        middle = CONTAINER_COORDINATES[X] / 2
        if self.position[X] > middle and self.isHot:
            return False
        elif self.position[X] < middle and self.isHot:
            return True
        elif self.position[X] > middle and not self.isHot:
            return True
        elif self.position[X] < middle and not self.isHot:
            return False
        else:
            raise RuntimeError("Where are we supposed to be?")

    def _hasBreachedBoundary(self, container, point) -> bool:
        """Determines whether the particle has breached a specific boundary."""
        if point + self.radius >= container:
            # breach on right side
            return True
        elif point - self.radius <= 0:
            # breach on left side
            return True
        else:
            # no breach
            return False

    def collide(self, other):
        distance = np.linalg.norm(self.position - other.position)
        if distance <= self.radius + other.radius:
            self.velocity, other.velocity = other.velocity, self.velocity
            self._calculateIsHot()
            other._calculateIsHot()

    def update(self):
        """Updates the particle's new position based on its previous position and its velocity."""
        new_position = self.position + self.velocity
        self.position += self.velocity

        if self._hasBreachedBoundary(CONTAINER_COORDINATES[X], new_position[X]):
            self._bounce(X)

        if self._hasBreachedBoundary(CONTAINER_COORDINATES[Y], new_position[Y]):
            self._bounce(Y)

        if self._isAtMiddleX(new_position[X]):
            if self._isAtGateY(new_position[Y]):
                # check to see if we should pass through
                if self.isHot and self.velocity[X] > 0:
                    # hot is correct side
                    self._bounce(X)
                elif not self.isHot and self.velocity[X] < 0:
                    # cold is on correct side
                    self._bounce(X)
                else:
                    pass
            else:
                self._bounce(X)
