#!/usr/bin/env python

import numpy
import pygame
import pygame.gfxdraw
import scipy.constants
import scipy.interpolate
import sys


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 500
HEIGHT = 500

SPAN = 10
MASS = 10 ** 11

pygame.display.init()

surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Objects

positions = []
velocities = []

for _ in range(10):
	positions.append(numpy.interp(numpy.random.random_sample(2), (0, 1), (-SPAN, SPAN)))
	velocities.append(numpy.zeros(2))

from_spacial = scipy.interpolate.interp1d((-SPAN, SPAN), (0, WIDTH))
to_spacial = scipy.interpolate.interp1d((0, WIDTH), (-SPAN, SPAN))

while True:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONUP:
			positions.append(to_spacial(pygame.mouse.get_pos()))
			velocities.append(numpy.zeros(2))
		elif event.type == pygame.QUIT:
			sys.exit()

	surface.fill(BLACK)

	dt = clock.tick() / 1000

	for i in range(len(positions)):
		acceleration = 0

		for j in range(len(positions)):
			if j != i:
				p_difference = positions[j] - positions[i]
				a_magnitude = scipy.constants.G * MASS / p_difference.dot(p_difference)

				acceleration += a_magnitude * p_difference / numpy.linalg.norm(p_difference)

		velocities[i] += acceleration * dt
		positions[i] += velocities[i] * dt

	for x, y in positions:
		try:
			x_i = int(from_spacial(x))
			y_i = int(from_spacial(y))
		except ValueError:
			pass
		else:
			pygame.gfxdraw.aacircle(surface, x_i, y_i, 1, WHITE)
			pygame.gfxdraw.filled_circle(surface, x_i, y_i, 1, WHITE)

	pygame.display.flip()
