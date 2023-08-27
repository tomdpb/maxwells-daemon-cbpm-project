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
        self._speed: float = np.hypot(velocity[0], velocity[1])
        self.isHot: bool = True if self._speed >= SPEED_THRESHHOLD else False

    def __repr__(self):
        return f"Particle({self.position}, {self.velocity}, {self._speed}, {self.isHot}, {self.radius})"

    def _bounce(self, position, boundary, coordinate):
        if position <= self.radius:
            position = 2 * (self.radius) - position
            self.velocity[coordinate] *= -1
        elif position >= boundary - self.radius:
            position = 2 * (boundary - self.radius) - position
            self.velocity[coordinate] *= -1

        return position

    def _isAtGate(self, upper_boundary, gate_size, point) -> bool:
        if (
            0.5 * (upper_boundary - gate_size)
            < point
            < upper_boundary - 0.5 * (upper_boundary + gate_size) + gate_size
        ):
            return True
        else:
            return False

    def _isOnLeft(self, container, point) -> bool:
        if 0 <= point[X] <= container[X] / 2:
            return True
        else:
            return False

    def _hasBreachedBoundary(self, container, point) -> bool:
        if point + self.radius >= container:
            # breach on right side
            return True
        elif point - self.radius <= 0:
            # breach on left side
            return True
        else:
            # no breach
            return False

    def update(self):
        new_position = self.position + self.velocity

        if self._hasBreachedBoundary(CONTAINER_COORDINATES[X], new_position[X]):
            new_position[X] = self._bounce(new_position[X], CONTAINER_COORDINATES[X], X)
        if self._hasBreachedBoundary(CONTAINER_COORDINATES[Y], new_position[Y]):
            new_position[Y] = self._bounce(new_position[Y], CONTAINER_COORDINATES[Y], Y)

        if self.isHot:
            # particle is on right side, wants to go left
            if (
                CONTAINER_COORDINATES[X] / 2
                <= new_position[X] + self.radius
                < CONTAINER_COORDINATES[X]
            ):
                if (
                    0
                    <= new_position[Y]  # + self.radius
                    < CONTAINER_COORDINATES[Y] / 2 - GATE_SIZE / 2  # under gate
                    and self.velocity[X] < 0  # heading right
                    and new_position[X] + self.radius
                    <= CONTAINER_COORDINATES[X] / 2  # in middle X
                ):
                    # bounce might need fixing
                    # print("under")
                    self._bounce(new_position[X], CONTAINER_COORDINATES[X] / 2, X)
                elif (
                    CONTAINER_COORDINATES[Y] / 2 + GATE_SIZE / 2  # above gate
                    < new_position[Y]  # + self.radius
                    <= CONTAINER_COORDINATES[Y]
                    and self.velocity[X] < 0  # heading right
                    and new_position[X] + self.radius <= CONTAINER_COORDINATES[X] / 2
                ):
                    # bounce might need fixing
                    # print("above")
                    self._bounce(new_position[X], CONTAINER_COORDINATES[X] / 2, X)
            # TODO check if it's actually hitting above and below

            # TODO find out what the hell this is doing
            # if self.velocity[X] < 0 and new_position[X] > CONTAINER_COORDINATES[X] / 2:
            #     if new_position[X] < CONTAINER_COORDINATES[X] / 2 + self.radius:
            #         self._bounce(new_position[X], CONTAINER_COORDINATES[X] / 2, X)

        self.position = new_position
