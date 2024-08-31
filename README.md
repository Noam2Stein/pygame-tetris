# pygame-tetris

![image](https://github.com/user-attachments/assets/69c7d18d-dfbb-476d-a46f-389e757becad)

Had a school project to make a game using pygame so i made Tetris.
This is a very simple version of Tetris that is missing sprites, the score-counter, any text, as well as a game over screen meaning that when you loose the window just closes.

* Intended to run with python 3.12 and pygame 2.5.

# design

The board is stored with a list of int-vec2 coordinates that represent filled cells, as well as a single instance of Piece which represents a positioned Tetris-piece.

A Piece is represented by its position, a PieceShape enum, and a rotation int.
A list of rects that represents both the hitbox and the graphics of the piece can be calculated from it.

Input-detection and collision-detection are used to move the piece until it lands,
resulting in its cells being added to the filled-cells list and a new Piece being initiated using a PieceShape taken from a next-piece queue.

# first experience with python & pygame

This project was my first "real" thing made with python, so i was curious if ill like it. i didn't like it.

Python's pro is supposed to be development-productivity,
but i found Python to actually slow me down duo to constant runtime-errors that could have been instantly fixable "compile-time" errors.
This problem originates from Python not being strongly-typed,
so if a function returns a bool, i can use it as a list and start running the code being unaware of any mistakes.
surprisingly it's easy to make syntatic mistakes that only get discovered at runtime, instead of an error by the IDE.
All of that made it so that writing Tetris even in rust, would take less time.
