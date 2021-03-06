# Clue-Reasoner

Term project for EECS 371  
### Team Members
[AnujIravane](https://github.com/AnujIravane), [jnbohrer](https://github.com/jnbohrer), [k-jin](https://github.com/k-jin)

## Installation

Requires [python](https://www.python.org/downloads/), [zchaff](https://www.princeton.edu/~chaff/zchaff.html)  
The zchaff installation directory is included in this repository  
Move into the directory, and run make  
Copy the zchaff executable into your path (echo $PATH to find directories on path)  
**Don't move the file as it is still required in the project directory**

## Usage

Navigate to Clue-Reasoner directory  
run the following commands to start the default game:  
```
python  
import ClueGame  
game = ClueGame.ClueGame()  
game.startGame()  
```
You can create and run multiple games. However, after creating one game, you must either call `startGame()` or `reset()` before creating the next game.  
You can specify how many players to include in the game (between 2 and 6, inclusive) by passing the number to ClueGame().  
The default number of reasoners for a game is 6. Example of altering human and reasoner number:  
`game= ClueGame.ClueGame(1,4)`  
would create a game with 1 human and 4 reasoners for 5 total players.
