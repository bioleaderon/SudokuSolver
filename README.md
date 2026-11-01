# SudokuSolver v1.0

A Python-based Sudoku solver utilizing `pandas` and Object-Oriented Programming (OOP) principles to process and solve grid-based puzzles.

## Features
* **CSV Import:** Easily load unsolved Sudoku puzzles directly from CSV files.
* **Pandas & Native Python Integration:** The puzzle is stored internally as a `DataFrame` while supporting sequence-like access through Python dunder methods (`__getitem__`, `__setitem__`).
* **Heuristic Solver Logic:** Implements a fast checking algorithm based on row, column, and block candidate analysis.

## Current Scope & Limitations
* **Puzzle Complexity:** Designed specifically for basic/deterministic Sudoku puzzles that can be solved using direct logical inference without deep searching.
* **Algorithm Constraint:** Advanced puzzles requiring guesswork or backtracking are currently outside the scope of v1.0 and may result in unresolved grids or non-termination.
