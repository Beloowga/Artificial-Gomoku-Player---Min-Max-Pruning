# Artificial-Gomoku-Player---MiniMax-Pruning
Project in collaboration with Mustapha KHERIF and Vaitea LE
<br>Sept 2024 - Jan 2025

## Overview
This project implements an artificial intelligence agent capable of playing Gomoku (Five-in-a-Row) on a 15×15 board.
The AI was developed as part of a university competition project and ranked Top 8 out of 400 participants.
The agent uses Minimax search with Alpha–Beta pruning, combined with heuristic board evaluation and move-space reduction strategies to balance performance and decision quality.

## Features
- Features
- Full Gomoku game logic on a 15×15 grid
- Human vs AI gameplay in the terminal
- Minimax decision algorithm
- Alpha–Beta pruning to reduce search complexity
- Heuristic evaluation function for board states
- Immediate win detection (four-in-a-row completion)
- Move filtering to limit the branching factor
- Basic performance optimisation through depth control

## Approach
### Game State Representation
The board is represented as a 15×15 matrix where:
0 = empty cell
1 = player X
2 = player O

## Move Generation
Instead of evaluating every empty square, the AI:
- Focuses on cells near already-played stones
- Applies early-game placement constraints
- Reduces the branching factor significantly
- This improves performance without heavily sacrificing strategic quality.
- Each turn updates the board and switches the active player

## Evaluation Function
A heuristic scoring system evaluates board positions by analysing:
- Consecutive stone sequences
- Open and semi-open lines
- Offensive and defensive patterns

Scores increase for strong player patterns and decrease for opponent threats.
The evaluation is used when the maximum search depth is reached.

## Minimax with Alpha–Beta Pruning
The core decision engine is a Minimax search tree enhanced with Alpha–Beta pruning:
- Minimax explores possible future moves assuming optimal play from both sides.
- Alpha–Beta pruning eliminates branches that cannot influence the final decision.
- A depth limit is used to keep computation time reasonable.

This allows the AI to make competitive decisions within a short time.

## Immediate Win Detection
- Before running a full search, the AI checks whether a move results in:
- An immediate victory
- A critical defensive block
- This shortcut improves both speed and tactical strength.

## Technologies Used
- Programming Language: Python
- Standard libraries (itertools, time)
- Terminal-based interface

##  How to use
1. Ensure Python 3 is installed.
2. Run the script
3. Choose whether the human or AI starts first.
4. Enter moves using a 'row column' format
   For example: A player wants to play on the 5th row and 8th column, then the player will enter: 5 8 into the console

## Project Context
This AI was developed as part of a competitive academic project focused on algorithmic decision-making and game theory.
The final agent achieved a Top 8 / 400 ranking in a tournament-style evaluation against other student-developed agents.

## Possible Improvements
- Iterative deepening search
- Parallel evaluation
- Graphical user interface
- More advanced heuristic pattern recognition
