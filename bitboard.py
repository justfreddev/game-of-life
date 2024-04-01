# This version of code was made to see how much more efficient I could make it, compared to the
# previous one.
# This code is 35.43% quicker than the other version, with the other one running in 1.75ms, and
# this program running in 1.13ms.

# The increase in speed is completely unnecessary due to its already quick runtime, however it was
# fun to optimise it to see how fast I could make it.

# This program uses bitboards to represent the grid of cells, for an increased speed performance
# and merges rules together to reduce unnecessary processing.


# Rules:
# 1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbors lives on to the next generation.
# 3. Any live cell with more than three live neighbors dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.


# I strongly dislike global variables however I don't feel like passing around a single constant
# as a parameter to every single function
global GRID_SIZE


def print_bitboard(bitboard: int) -> None:
    """Prints out the bitboard in a readable way"""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            print((bitboard >> i * GRID_SIZE + j) & 1, end=" ")
        print()
    print("\n")


def get_neighbours(bitboard: int, i: int, j: int) -> list[int]:
    """Gets the neighbours of a cell in the grid"""
    neighbours = []

    # Uses max and min functions to prevent unwanted indexes
    for x in range(max(0, i - 1), min(GRID_SIZE, i + 2)):
        for y in range(max(0, j - 1), min(GRID_SIZE, j + 2)):
            # Makes sure that the given cell is not included in the outputted list
            if x != i or y != j:
                # Appends the value of the surrounding cell to the list
                # (bitboard >> x * N + y) gets the bit index from the x, and y values of the 2D list
                # The & is a bitwise AND operator and hence compares the value at the bit index to 1,
                # Meaning that if the value at the bit index is 1, it will 1, otherwise it will be 0
                neighbours.append((bitboard >> x * GRID_SIZE + y) & 1)

    return neighbours


def get_live_indices(bitboard: int) -> list[tuple[int, int]]:
    """Gets the indices of all the live cells on the grid"""
    indices = []

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Checks if the value at the bit index is equal to 1
            if (bitboard >> i * GRID_SIZE + j) & 1:
                indices.append((i, j))

    return indices


def get_dead_indices(bitboard: int) -> list[tuple[int, int]]:
    """Gets the indices of all the dead cells on the grid"""
    indices = []

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Checks if the value at the bit index is equal to 0
            # Because if the value at (bitboard >> i * N + j) is equal to 0, then 0 & 1 == 0
            if (bitboard >> i * GRID_SIZE + j) & 1 == 0:
                indices.append((i, j))
    return indices


def rule_one_two_and_three(bitboard: int) -> list[tuple[int, int]]:
    """Carries out rules one, two and three"""
    live_indices = get_live_indices(bitboard)
    dead_indices = []

    for i, j in live_indices:
        # The number of live neighbours the current live cell has
        live_neighbours = get_neighbours(bitboard, i, j).count(1)

        # Because rules 1, 2 and 3 work with the number of live neighbours, and do not interfere with
        # each other, they are all able to be carried out at the same time.
        # Where n is the number of live neighbours:
        # Rule 1: n < 2 dies
        # Rule 2: 1 < n < 4 lives, aka 1 > n > 4 dies
        # Rule 3: n > 4 dies
        # This means that have the following inequalities for cells that die:
        # 2 > n ────┐
        # 1 > n ────┴──> Simplifies to 2 > n
        # 4 > n ────┐
        # 3 > n ────┴──> Simplifies to n > 3
        # Hence why there need to be more than 3 and less then 2 live neighbours to become dead in the
        # next generation.
        if live_neighbours > 3 or live_neighbours < 2:
            dead_indices.append((i, j))

    return dead_indices


def rule_four(bitboard: int) -> list[tuple[int, int]]:
    """Carries out rule four"""
    live_indices = get_live_indices(bitboard)
    indices = []

    for i, j in live_indices:
        # I initially carried out this rule by looking at every single dead cell on the board, and checking
        # if it had three live neighbours, however I realised that it was checking unnecessarily many cells,
        # So I made it only check dead cells that had at least 1 live neighbour.
        dead_neighbours = []
        for x in range(max(0, i - 1), min(GRID_SIZE, i + 2)):
            for y in range(max(0, j - 1), min(GRID_SIZE, j + 2)):
                if x != i or y != j:
                    dead_neighbours.append((x, y))

        # Checks if the the dead cell has exactly three live neighbours, if so, it appends it to the indices list
        for neighbour in dead_neighbours:
            if get_neighbours(bitboard, neighbour[0], neighbour[1]).count(1) == 3:
                indices.append((neighbour[0], neighbour[1]))

    return indices


def apply_rules(bitboard: int, iterations: int) -> None:
    """Applies all of the Game of Life rules"""
    counter = 0  # A counter to limit the number of iterations
    while counter < iterations + 1:
        dead_indices = rule_one_two_and_three(
            bitboard
        )  # Gets the indices of the cells that will die
        live_indices = rule_four(
            bitboard
        )  # Gets the indices of the cells that will live

        for i, j in dead_indices:
            # Sets all the cells in dead_indices to dead
            # The ~(1 << i * N + j) is a number where the only turned off bit is the one at the (i, j) position.
            # This acts as a mask and means that for the currently dead cells: 0 & 1 =0 =, for the currently
            # alive cells, 1 & 1 == 1, leaving the unaffected ones still alive, and for the current (i, j) index,
            # because it has been reversed, the calculation will be (0 | 1) & 0 = 0, setting the cell to be dead.
            bitboard &= ~(1 << i * GRID_SIZE + j)
        for i, j in live_indices:
            # Similarly to the statement in the for loop above, the `1 << i * N + j` creates a mask that is just
            # a singular 'on' bit at the (i, j) position. Using the bitwise OR assignment operator, every other cell
            # remains untouched, and the cell at (i, j) becomes live because (1 | 0) | 1 == 1
            bitboard |= 1 << i * GRID_SIZE + j

        print_bitboard(bitboard)
        counter += 1


if __name__ == "__main__":
    # Sets the initial conditions for the simulation
    bitboard = 0

    GRID_SIZE = 10 # The length of the grid 

    bitboard |= 1 << 0 * GRID_SIZE + 1 # ┐
    bitboard |= 1 << 1 * GRID_SIZE + 2 # │
    bitboard |= 1 << 2 * GRID_SIZE + 0 # ├──> Sets the initial state of the board. This one creates a cool glider
    bitboard |= 1 << 2 * GRID_SIZE + 1 # │
    bitboard |= 1 << 2 * GRID_SIZE + 2 # ┘

    iterations = 20

    apply_rules(bitboard, iterations)
