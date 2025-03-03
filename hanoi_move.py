import sys
import re
from pathlib import Path

class TowerOfHanoi:
    def __init__(self, n):
        # Initialize the pegs with disks (disks are represented by numbers: larger number = larger disk)
        self.n = n
        # Representing the pegs using a 2D array similar to your C code (with disks on peg 1)
        self.pegs = [[0, 0, 0] for _ in range(n)]  # Initialize with 0s (empty pegs)
        for i in range(n):
            self.pegs[i][0] = n - i  # Fill peg 1 with disks (largest disk at bottom)

    def print_state(self):
        """Print the current state of the Tower of Hanoi with proper alignment."""
        patterns = {
            0: "    |    ",  # Empty peg (no disk)
            1: "    *    ",  # Disk 1 (smallest)
            2: "   **    ",  # Disk 2
            3: "  ***    ",  # Disk 3
            4: "  *****  ",  # Disk 4
            5: " ******* ",  # Disk 5 (for up to 5 disks)
            6: "********* ",  # Disk 6 (for up to 6 disks)
        }

        # Print each level of the pegs
        for i in range(self.n):
            row = []
            for j in range(3):  # 3 pegs
                if self.pegs[i][j] != 0:
                    disk = self.pegs[i][j]
                    row.append(f"{patterns[disk]:^11}")  # Center the disk
                else:
                    row.append(f"{patterns[0]:^11}")  # Empty peg
            print("|".join(row))
        print("-----------------------------")
        print("\n")

    def move_disk(self, from_peg, to_peg):
        """Move a disk from one peg to another."""
        # Find the first non-zero (disk) on the source peg
        source_disk_index = next(i for i in range(self.n) if self.pegs[i][from_peg] != 0)
        dest_disk_index = next(i for i in range(self.n-1, -1, -1) if self.pegs[i][to_peg] == 0)

        # Move the disk
        disk = self.pegs[source_disk_index][from_peg]
        self.pegs[source_disk_index][from_peg] = 0
        self.pegs[dest_disk_index][to_peg] = disk

        # Print the updated state
        self.print_state()

    def get_legal_moves(self):
        """Return a list of all legal moves based on the current game state."""
        legal_moves = []
        for from_peg in range(3):  # Check each peg
            if any(self.pegs[i][from_peg] != 0 for i in range(self.n)):  # If there are disks on the peg
                for to_peg in range(3):
                    if from_peg != to_peg and (not any(self.pegs[i][to_peg] != 0 for i in range(self.n)) or
                                                self.pegs[self.n-1][from_peg] < self.pegs[self.n-1][to_peg]):
                        legal_moves.append((from_peg, to_peg))
        return legal_moves

    def solve_move(self, move):
        """Processes a move and updates the state."""
        match = re.match(r"Move disk (\d+) from peg (\d+) to peg (\d+)", move)
        if match:
            _, from_peg, to_peg = map(int, match.groups())
            self.move_disk(from_peg-1, to_peg-1)  # Subtract 1 for zero-indexing
            self.print_state()
        else:
            print("Invalid move format")


# Example of initializing the game and printing the state
def update_readme_with_move(move):
    # Number of disks (You can change this value)
    n = 4

    # Initialize the game
    hanoi = TowerOfHanoi(n)

    # Get the updated state after the move
    updated_state = hanoi.solve_move(move)

    # Get the legal moves for the current state
    legal_moves = hanoi.get_legal_moves()

    # Path to the README file
    readme_path = Path("README.md")

    # Read the current README content
    with open(readme_path, "r") as file:
        content = file.read()

    # Generate clickable move links in the README
    move_links = "\n".join([f"- [{move}](https://github.com/yourusername/yourrepository/issues/new?title={move.replace(' ', '%20')})" for move in legal_moves])

    # Replace the placeholder with the legal move links
    new_content = content.replace("<!-- LegalMoves -->", f"<!-- LegalMoves -->\n{move_links}\n")

    # Write the updated content back to README
    with open(readme_path, "w") as file:
        file.write(new_content)

    print("README updated successfully!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a move as an argument.")
    else:
        move = sys.argv[1]  # Get the move from the command-line argument
        update_readme_with_move(move)
