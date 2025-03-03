import sys
import re
from pathlib import Path

# Define patterns for disks (larger the disk, the more stars)
patterns = [
    "    |    ",  # Empty peg (no disk)
    "    *    ",  # Disk 1 (smallest)
    "   **    ",  # Disk 2
    "  ***    ",  # Disk 3 (largest)
]

class TowerOfHanoi:
    def __init__(self, n):
        # Initialize the pegs with disks (disks are represented by their index number: larger index = larger disk)
        self.n = n
        # Peg 1 has all disks: 3 (largest), 2, 1 (smallest)
        self.pegs = {1: [1, 2, 3], 2: [], 3: []}  # Peg 1: [1, 2, 3] -> Disk 1 is the smallest, disk 3 is the largest

    def print_state(self):
        """Returns the current state of the Tower of Hanoi as a string."""
        # Initialize an empty table for the game state
        table = []
        
        # We go through each level of the tower from bottom to top
        for level in range(self.n, 0, -1):
            row = []
            for peg in range(1, 4):
                if len(self.pegs[peg]) >= level:
                    disk_size = self.pegs[peg][-level]  # Disk size is the value of the disk (1 to 3)
                    row.append(f"{patterns[disk_size]:^11}")  # Center the pattern in the column
                else:
                    row.append(f"{patterns[0]:^11}")  # No disk, just the empty peg
            table.append(row)
        
        # Add Peg Labels at the bottom
        table.append(['Peg 1'.center(11), 'Peg 2'.center(11), 'Peg 3'.center(11)])
        
        # Convert table into a Markdown-compatible string
        markdown_table = ""
        for row in table:
            markdown_table += "|".join(row) + "\n"
        markdown_table = markdown_table.replace("\n", "\n|---|---|---|\n", 1)  # Add separator row after header
        return markdown_table.strip()

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
            return self.print_state()
        else:
            return "Invalid move format"


# Main logic to update README with new state
def update_readme_with_move(move):
    # Number of disks (3 disks)
    n = 3

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
    move_links = "\n".join([f"- [**{move}**](https://github.com/leonardoLavagna/leonardoLavagna/issues/new?title={move.replace(' ', '%20')})" for move in legal_moves])

    # Replace the placeholders with the updated game state and legal moves
    new_content = content.replace("<!-- GameState -->", f"<!-- GameState -->\n{updated_state}\n")
    new_content = new_content.replace("<!-- LegalMoves -->", f"<!-- LegalMoves -->\n{move_links}\n")

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
