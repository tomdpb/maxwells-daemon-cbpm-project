"""

DARIO FUMAROLA - PHYS265 FINAL PROJECT
SIMULATION OF THE MAXWELL'S DEMON
File: redParticle.py

"""


import math
import pygame

(w, h) = (1000, 600)
screen = pygame.display.set_mode((w, h + 200))


class redPar:
    def __init__(self, x, y, size, mass=1):
        """Declares intrinsic characteristics of particle."""
        self.x = x
        self.y = y
        self.size = size
        self.colour = (255, 0, 0)
        self.thickness = 100
        self.speed = 80
        self.angle = 0
        self.mass = mass
        self.temp = 40

    def display(self):
        """Takes characteristics of the particle, and places it on the screen."""
        pygame.draw.circle(
            screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness
        )

    def move(self):
        """Adjusts coordinates of particles according to current speed and angles of movement."""
        self.x += 5 * math.sin(self.angle) * self.speed
        self.y -= 5 * math.cos(self.angle) * self.speed
        self.vel_y = self.speed * math.cos(self.angle)
        self.vel_x = self.speed * math.sin(self.angle)

    def rebound(self):
        """Adjust speed and angle of particles that are about to rebound against walls or other particles.
        Coordinates conditions allow red particles to pass through the door from the first chamber to the second."""
        if self.x > w - self.size - 10:
            self.x = 2 * (w - self.size - 10) - self.x
            self.angle = -self.angle

        elif self.x < self.size + 10:
            self.x = 2 * (self.size + 10) - self.x
            self.angle = -self.angle

        if self.y > h - self.size - 10:
            self.y = 2 * (h - self.size - 10) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.size + 10:
            self.y = 2 * (self.size + 10) - self.y
            self.angle = math.pi - self.angle

        if 0 <= self.x < 510:
            if 0 < self.y < 225 and self.vel_x > 0 and self.x >= 500 - self.size:
                self.x = 2 * (self.size + self.x - self.size) - self.x
                self.angle = -self.angle
            elif 405 < self.y < 600 and self.vel_x > 0 and self.x >= 500 - self.size:
                self.x = 2 * (self.size + self.x - self.size) - self.x
                self.angle = -self.angle

        if self.vel_x < 0 and self.x > w / 2:
            if self.x < w / 2 + self.size:
                self.x = 2 * (self.size + w / 2) - self.x
                self.angle = -self.angle
