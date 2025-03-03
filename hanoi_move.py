import sys
import re
from pathlib import Path

class TowerOfHanoi:
    def __init__(self, n):
        self.n = n
        # Create a board: a list of n rows and 3 columns.
        # Each cell holds a disk number (0 means empty).
        # We fill peg1 (column 0) with disks so that row 0 is the top (smallest disk)
        # and row n-1 is the bottom (largest disk)
        self.board = [[0, 0, 0] for _ in range(n)]
        for i in range(n):
            self.board[i][0] = i + 1  # row 0 gets disk 1, row 1 gets disk 2, etc.

    def print_state(self):
        """Return a string showing the board state with the desired patterns."""
        # Define patterns: index 0 = empty, 1 = smallest, etc.
        patterns = {
            0: "    |    ",
            1: "    *    ",
            2: "   **    ",
            3: "  ***    ",
            4: "  *****  ",
            5: " ******* ",
            6: "*********"
        }
        output = ""
        # Print rows in order (top row first)
        for row in range(self.n):
            line = []
            for peg in range(3):
                disk = self.board[row][peg]
                line.append(patterns[disk])
            output += " ".join(line) + "\n"
        return output.strip()

    def move_disk(self, source, dest):
        """Move the top disk from peg (source) to peg (dest).
           Peg numbers are zero-indexed.
        """
        # Find the top disk on the source peg (first nonzero in column 'source')
        src_index = None
        for i in range(self.n):
            if self.board[i][source] != 0:
                src_index = i
                break
        if src_index is None:
            print(f"Error: Peg {source+1} is empty")
            return False

        # Find where to place the disk on the destination peg:
        # Look from the bottom upward for the first empty cell in column 'dest'
        dest_index = None
        for i in range(self.n - 1, -1, -1):
            if self.board[i][dest] == 0:
                dest_index = i
                break
        if dest_index is None:
            print(f"Error: Peg {dest+1} is full")
            return False

        # Check legality: if destination peg is not empty, its top disk is the one in the first row (from top)
        # that is nonzero.
        top_dest = None
        for i in range(self.n):
            if self.board[i][dest] != 0:
                top_dest = self.board[i][dest]
                break
        disk = self.board[src_index][source]
        if top_dest is not None and disk > top_dest:
            print("Illegal move: cannot place a larger disk on a smaller one")
            return False

        # Make the move
        self.board[src_index][source] = 0
        self.board[dest_index][dest] = disk
        return True

    def get_top_disk(self, peg):
        """Return the disk on top of peg (zero-indexed) or None if peg is empty."""
        for i in range(self.n):
            if self.board[i][peg] != 0:
                return self.board[i][peg]
        return None

    def get_legal_moves(self):
        """Return a list of legal moves as strings."""
        moves = []
        for s in range(3):
            disk = self.get_top_disk(s)
            if disk is None:
                continue
            for d in range(3):
                if s == d:
                    continue
                dest_top = self.get_top_disk(d)
                if dest_top is None or disk < dest_top:
                    moves.append(f"Move disk {disk} from peg {s+1} to peg {d+1}")
        return moves

    def solve_move(self, move):
        """Process a move string, update state, and return the new board state string."""
        # Expected move format: "Move disk X from peg A to peg B"
        match = re.match(r"Move disk (\d+) from peg (\d+) to peg (\d+)", move)
        if match:
            disk, s, d = map(int, match.groups())
            if self.move_disk(s-1, d-1):  # adjust for zero-indexing
                return self.print_state()
            else:
                return "Move failed"
        else:
            return "Invalid move format"

def update_readme_with_move(move):
    # Number of disks (using 4 as in your C code example)
    n = 3

    # Initialize the game board as in C (peg 1 has disks [1,2,3,4] from top to bottom)
    hanoi = TowerOfHanoi(n)
    # Process the move and get the updated state
    updated_state = hanoi.solve_move(move)
    # Get the updated list of legal moves
    legal_moves = hanoi.get_legal_moves()

    # Update the README file
    readme_path = Path("README.md")
    with open(readme_path, "r") as file:
        content = file.read()
    # Build the legal moves text (each move becomes a clickable link)
    move_links = "\n".join([
        f"- [{m}](https://github.com/leonardoLavagna/leonardoLavagna/issues/new?title={m.replace(' ', '%20')})"
        for m in legal_moves
    ])
    # Replace the placeholders in README
    new_content = content.replace("<!-- GameState -->", f"<!-- GameState -->\n{updated_state}\n")
    new_content = new_content.replace("<!-- LegalMoves -->", f"<!-- LegalMoves -->\n{move_links}\n")
    with open(readme_path, "w") as file:
        file.write(new_content)
    print("README updated successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a move as an argument (e.g., \"Move disk 1 from peg 1 to peg 2\").")
    else:
        move = sys.argv[1]
        update_readme_with_move(move)
