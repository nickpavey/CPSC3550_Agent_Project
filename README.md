# CPSC3550 Checkers AI – Terminal Edition

## Project Description

This is a fully functional two-player Checkers game built in Python, where a human player competes against a simple AI opponent using the **Minimax** algorithm. The game is played directly in the terminal with a **Battleship-style grid system**.

Features include:
- Human vs. AI gameplay
- Legal move validation
- King promotion
- KeyboardInterrupt (`Ctrl+C`) exit handling
- Clean, readable board format
- Input cancellation with `'b'` to go back during move selection

---

## How to Install and Run

1. **Clone the Repository:**
   ```bash
   git clone hhttps://github.com/nickpavey/CPSC3550_Agent_Project.git
   cd CPSC3550_Agent_Project
   ```

2. **Run the Game:**
   Ensure you have Python 3 installed. Then run:
   ```bash
   python Agent_Project.py
   ```

No third-party dependencies are required, it runs with just standard Python libraries.

---

## How to Use the Software

- When the game starts, the board will display in the terminal like a normal checkers board

- You will be prompted to:
  - **Select a piece** using a row letter and column number (e.g., `F 0`)
  - **Select a destination** for that piece (e.g., `E 1`)
  - Type `'b'` during either step to **cancel and go back**

- The AI will make its move automatically after yours.
- The game continues until one side has no pieces remaining.
- Press `Ctrl+C` at any time to gracefully exit the game.

---

##  How This Was Built

The game logic was implemented from scratch in Python using the following architecture:

- **Board Representation:** An 8x8 grid with characters: `'r'` (Red), `'b'` (Black), and uppercase for kings.
- **Move Generation:** Pieces move diagonally; jumps over opponents are prioritized if available.
- **Minimax Algorithm:** The AI uses a depth-limited minimax strategy to evaluate potential moves and maximize its board advantage.
- **Evaluation Function:** Assigns point values to pieces and kings to determine board advantage.
- **Interactive CLI:** Input is broken into clear steps: selecting and placing with Battleship-style row labels and error feedback.

---
