def print_hanoi(state):
    """Print the state of the towers."""
    pattern = ['    |    ', '    *    ', '   ***   ', '  *****  ', ' ******* ', '*********']
    for i in range(4):  # Assuming 4 disks
        for j in range(3):
            print(pattern[state[i][j]], end=" ")
        print()
    print("-----------------------------\n")

def move(state, source, dest):
    """Move a disk from the source tower to the destination tower."""
    temp = 0
    riga_source = 0
    riga_dest = 3

    while state[riga_source][source] == 0:
        riga_source += 1
    while state[riga_dest][dest] != 0:
        riga_dest -= 1
    temp = state[riga_source][source]
    state[riga_source][source] = state[riga_dest][dest]
    state[riga_dest][dest] = temp
    print_hanoi(state)
    return state

# Example state initialization (4 disks, on tower 0)
hanoi_state = [[1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 0]]
print_hanoi(hanoi_state)
move(hanoi_state, 0, 2)  # Move from tower 0 to tower 2
