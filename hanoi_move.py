class TowerOfHanoi:
    def __init__(self, n):
        # Initialize the pegs with disks (disks are represented by their size: 3, 2, 1)
        self.n = n
        # Peg 1 starts with all disks, Peg 2 and Peg 3 are empty
        self.pegs = {1: [3, 2, 1], 2: [], 3: []}  # Peg 1: [3, 2, 1]

    def print_state(self):
        """Print the current state of the Tower of Hanoi."""
        patterns = {
            0: "    |    ",  # Empty peg (no disk)
            1: "    *    ",  # Disk 1 (smallest)
            2: "   **    ",  # Disk 2
            3: "  ***    ",  # Disk 3 (largest)
        }

        # Loop through each row of the tower (from largest disk to smallest)
        for level in range(self.n, 0, -1):
            row = []
            for peg in range(1, 4):
                if len(self.pegs[peg]) >= level:
                    disk = self.pegs[peg][-level]
                    row.append(f"{patterns[disk]:^11}")  # Center the disk pattern
                else:
                    row.append(f"{patterns[0]:^11}")  # Empty peg
            print("|".join(row))
        
        # Print the labels for the pegs
        print(f"{'Peg 1':^11}|{'Peg 2':^11}|{'Peg 3':^11}")

    def move_disk(self, from_peg, to_peg):
        """Move a disk from one peg to another."""
        if not self.pegs[from_peg]:
            print(f"Error: No disks on Peg {from_peg}")
            return False
        disk = self.pegs[from_peg].pop()
        self.pegs[to_peg].append(disk)
        return True

    def get_legal_moves(self):
        """Return a list of all legal moves based on the current game state."""
        legal_moves = []
        for from_peg in range(1, 4):
            if self.pegs[from_peg]:  # If there are disks on this peg
                for to_peg in range(1, 4):
                    if from_peg != to_peg and (not self.pegs[to_peg] or self.pegs[from_peg][-1] < self.pegs[to_peg][-1]):
                        # Move from from_peg to to_peg is legal
                        disk = self.pegs[from_peg][-1]
                        move_str = f"Move disk {disk} from peg {from_peg} to peg {to_peg}"
                        legal_moves.append(move_str)
        return legal_moves

    def solve_move(self, move):
        """Processes a move and updates the state."""
        # Parsing the move like "Move disk 1 from peg 1 to peg 2"
        match = re.match(r"Move disk (\d+) from peg (\d+) to peg (\d+)", move)
        if match:
            disk_num, from_peg, to_peg = map(int, match.groups())
            self.move_disk(from_peg, to_peg)
            self.print_state()
        else:
            print("Invalid move format")


# Example of initializing the game and printing the state
if __name__ == "__main__":
    # Number of disks (3 disks)
    n = 3
    game = TowerOfHanoi(n)

    # Print initial game state
    game.print_state()

    # Example: Make a move and print updated state
    move = "Move disk 1 from peg 1 to peg 2"
    print(f"\nMaking move: {move}")
    game.solve_move(move)

    # Print updated state
    game.print_state()
