import numpy as np


CONTAINER_COORDINATES = np.array([800, 600])  # x, y
# the daemon will open the gate for a particle when it reaches this speed
SPEED_THRESHHOLD: float = 10.0
GATE_SIZE: int = 100
X, Y = 0, 1  # this is just for ease of reading
PARTICLE_RADIUS: int = 5


class Particle:
    def __init__(self, position: np.ndarray, velocity: np.ndarray):
        self.position: np.ndarray = position
        self.velocity: np.ndarray = velocity
        self._speed: float = np.hypot(velocity[0], velocity[1])
        self.isHot: bool = True if self._speed >= SPEED_THRESHHOLD else False

    def __repr__(self):
        return (
            f"Particle({self.position}, {self.velocity}, {self._speed}, {self.isHot})"
        )

    def _bounce(self, position, boundary, coordinate):
        if position <= PARTICLE_RADIUS:
            position = 2 * (PARTICLE_RADIUS) - position
            self.velocity[coordinate] *= -1
        elif position >= boundary - PARTICLE_RADIUS:
            position = 2 * (boundary - PARTICLE_RADIUS) - position
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
        if point + PARTICLE_RADIUS >= container:
            # breach on right side
            return True
        elif point - PARTICLE_RADIUS <= 0:
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

        # TODO REMOVE NOT
        if not self.isHot:
            # heading right to left
            if self.velocity[X] < 0 and not self._isOnLeft(
                CONTAINER_COORDINATES, new_position
            ):
                if self._isAtGate(CONTAINER_COORDINATES[Y], GATE_SIZE, new_position[Y]):
                    # we can pass through!
                    pass
            elif self.velocity[X] < 0 and self._hasBreachedBoundary(
                CONTAINER_COORDINATES[X] / 2, new_position[X]
            ):
                # we're not at the gate. Behave as if hitting a wall
                new_position[X] = self._bounce(
                    new_position[X], CONTAINER_COORDINATES[X] / 2, X
                )
                # print("We've hit the middle")
            # heading left to right
            elif self.velocity[X] >= 0 and not self._isOnLeft(
                CONTAINER_COORDINATES, new_position
            ):
                # will hit the rightmost wall
                if self._hasBreachedBoundary(CONTAINER_COORDINATES[X], new_position[X]):
                    new_position[X] = self._bounce(
                        new_position[X], CONTAINER_COORDINATES[X], X
                    )
            elif self.velocity[X] >= 0 and self._isOnLeft(
                CONTAINER_COORDINATES, new_position
            ):
                # will hit middle
                new_position[X] = self._bounce(
                    new_position[X], CONTAINER_COORDINATES[X] / 2, X
                )

        # this was copied
        # if self.isHot:
        #    if 0 <= new_position[X] < CONTAINER_COORDINATES[X]/2 + PARTICLE_RADIUS:
        #       if self.velocity[X] > 0 and 0 < new_position[Y] < CONTAINER_COORDINATES[Y] - GATE_SIZE/2 and new_position[X] >= CONTAINER_COORDINATES[X] - PARTICLE_RADIUS:
        #           self._bounce(new_position[X], CONTAINER_COORDINATES[X]/2, X)
        #       elif self.velocity[X] > 0 and CONTAINER_COORDINATES[Y]/2 + GATE_SIZE/2 < new_position[Y] < CONTAINER_COORDINATES[Y] and new_position[X] >= CONTAINER_COORDINATES[X]/2 - PARTICLE_RADIUS:
        #           self._bounce(new_position[X], CONTAINER_COORDINATES[X]/2, X)
        #
        #   if self.velocity[X] < 0 and new_position[X] > CONTAINER_COORDINATES[X]/2:
        #       if new_position[X] < CONTAINER_COORDINATES[X]/2 + PARTICLE_RADIUS:
        #           self._bounce(new_position[X], CONTAINER_COORDINATES[X]/2, X)

        # ew_position[X] = self._bounce(new_position[X], CONTAINER_COORDINATES[X], X)
        # ew_position[Y] = self._bounce(new_position[Y], CONTAINER_COORDINATES[Y], Y)
        self.position = new_position
