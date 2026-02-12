Teeko AI Game Engine 🤖
An advanced game-playing agent designed for the board game Teeko, featuring a decision-making engine built on adversarial search principles. This agent utilizes a Minimax strategy with deep-state evaluation to compete against human or AI opponents.

🧠 Core Architecture
The "brain" of the agent is built on three primary pillars:

1. Adversarial Search (Minimax)
The agent utilizes a Minimax algorithm to simulate future turns. It recursively explores the game tree to maximize the agent's potential advantage while assuming the opponent will play optimally to minimize it.

2. State-Space Successors
The engine handles two distinct game phases:

Drop Phase: Managing the initial placement of 8 pieces on the 5x5 grid.

Move Phase: Calculating valid adjacent moves (including diagonals) once all pieces are in play, ensuring a strict adherence to Teeko's movement constraints.

3. Intelligent Heuristic Evaluation
Since the state space for Teeko can be vast, the agent uses a custom Heuristic Evaluation Function to score non-terminal board states:

Material Advantage: A baseline score based on active piece count.

Clustering Logic: A sophisticated "Pairwise Distance" algorithm that rewards the agent for keeping its pieces in close proximity, increasing the probability of forming winning configurations (4-in-a-row or 2x2 squares).

🛠️ Technical Implementation
Language: Python 3

Search Depth: Configured to a depth of 3 (expandable) to balance computational efficiency with strategic foresight.

Robustness: Includes custom error-handling and fallback logic (random move selection) to ensure the game loop never hangs during unexpected state transitions.

Memory Management: Utilizes deep copying for state simulation to prevent side effects during recursive search calls.

🚀 Getting Started
Prerequisites
Python 3.x installed on your machine.

Installation
Clone the repository:

Bash

git clone https://github.com/sraman9/teekoplayer.git
cd teekoplayer
Run the game:

Bash

python3 game.py
📈 Future Enhancements
Alpha-Beta Pruning: Implementing pruning to allow for significantly deeper search depths within the same time constraints.

Opening Book: Incorporating a database of optimal first-moves to secure early-game center control.
