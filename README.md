# Clue-Reasoner

Term project for EECS 371  
### Team Members
[AnujIravane](https://github.com/AnujIravane), [jnbohrer](https://github.com/jnbohrer), [k-jin](https://github.com/k-jin)

## Installation

Requires [zchaff](https://www.princeton.edu/~chaff/zchaff.html)  
The zchaff installation directory is included in this repository  
Move into the directory, and run make  
Copy the zchaff executable into your path (echo $PATH to find directories on path)  
**Don't move the file as it is still required in the project directory**

## Usage

Navigate to Clue-Reasoner directory  
run the following commands:  
```
python  
import ClueGame  
game = ClueGame.ClueGame()  
game.startGame()  
```
You can run multiple games as long as startGame is run before creating the next game
