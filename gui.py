# A pygame implementation of Conway's Game of Life, logic transferred from bitboard.py,
# the pygame stuff written by Copilot

# Pygame will need to be installed to run this code, install it by running `pip install pygame`

# Turn cells on and off by clicking on them, press space to start the simulation, press r to reset the board

import pygame
from pygame.locals import *
import sys

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

WIDTH, HEIGHT = 1000, 1000

GRID_SIZE = 20
ITERATIONS = 50


def get_neighbours(bitboard: int, i: int, j: int) -> list[int]:
    """Gets the neighbours of a cell in the grid"""
    neighbours = []

    for x in range(max(0, i - 1), min(GRID_SIZE, i + 2)):
        for y in range(max(0, j - 1), min(GRID_SIZE, j + 2)):
            if x != i or y != j:
                neighbours.append((bitboard >> x * GRID_SIZE + y) & 1)

    return neighbours


def get_live_indices(bitboard: int) -> list[tuple[int, int]]:
    """Gets the indices of all the live cells on the grid"""
    indices = []

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (bitboard >> i * GRID_SIZE + j) & 1:
                indices.append((i, j))

    return indices


def get_dead_indices(bitboard: int) -> list[tuple[int, int]]:
    """Gets the indices of all the dead cells on the grid"""
    indices = []

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (bitboard >> i * GRID_SIZE + j) & 1 == 0:
                indices.append((i, j))
    return indices


def rule_one_two_and_three(bitboard: int) -> list[tuple[int, int]]:
    """Carries out rules one, two and three"""
    live_indices = get_live_indices(bitboard)
    dead_indices = []

    for i, j in live_indices:
        live_neighbours = get_neighbours(bitboard, i, j).count(1)

        if live_neighbours > 3 or live_neighbours < 2:
            dead_indices.append((i, j))

    return dead_indices


def rule_four(bitboard: int) -> list[tuple[int, int]]:
    """Carries out rule four"""
    live_indices = get_live_indices(bitboard)
    indices = []

    for i, j in live_indices:
        dead_neighbours = []
        for x in range(max(0, i - 1), min(GRID_SIZE, i + 2)):
            for y in range(max(0, j - 1), min(GRID_SIZE, j + 2)):
                if x != i or y != j:
                    dead_neighbours.append((x, y))

        for neighbour in dead_neighbours:
            if get_neighbours(bitboard, neighbour[0], neighbour[1]).count(1) == 3:
                indices.append((neighbour[0], neighbour[1]))

    return indices


def apply_rules(bitboard: int, iterations: int) -> list[int]:
    """Applies all of the Game of Life rules"""
    steps = []
    counter = 0
    while counter < iterations + 1:
        dead_indices = rule_one_two_and_three(bitboard)
        live_indices = rule_four(bitboard)

        for i, j in dead_indices:
            bitboard &= ~(1 << i * GRID_SIZE + j)
        for i, j in live_indices:
            bitboard |= 1 << i * GRID_SIZE + j

        steps.append(bitboard)
        counter += 1

    return steps


def draw(screen, bitboard):
    screen.fill(BLACK)

    cell_size = WIDTH // GRID_SIZE

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, cell_rect)

            if (bitboard >> i * GRID_SIZE + j) & 1:
                pygame.draw.rect(screen, YELLOW, cell_rect)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, GRAY, cell_rect, 1)

    pygame.display.flip()


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game of Life")

    bitboard = 0

    initial_state = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    initial_state = bitboard
                    steps = apply_rules(bitboard, ITERATIONS)
                    while len(steps) > 1 and steps[-1] == steps[-2]:
                        steps.pop()
                    reset = False
                    for step in steps:
                        if reset:
                            break
                        draw(screen, step)
                        pygame.time.wait(250)

                        if pygame.event.peek(pygame.KEYDOWN):
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_r:
                                        bitboard = initial_state
                                        reset = True
                                        break

                        pygame.time.wait(500)
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i, j = y // (WIDTH // GRID_SIZE), x // (WIDTH // GRID_SIZE)
                bitboard ^= 1 << i * GRID_SIZE + j
                pygame.draw.rect(
                    screen,
                    YELLOW,
                    (
                        j * (WIDTH // GRID_SIZE),
                        i * (WIDTH // GRID_SIZE),
                        WIDTH // GRID_SIZE,
                        WIDTH // GRID_SIZE,
                    ),
                )
                pygame.display.flip()

        draw(screen, bitboard)

        pygame.time.Clock().tick(60.0)


if __name__ == "__main__":
    run()
