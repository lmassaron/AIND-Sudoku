# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

A: In the reduction phase, when we try to exclude that certain cells cannot take certain numbers in the final solution, we apply another rule of exclusion, after elimination and only choice, based on the naked twins strategy.

Naked Twins (also known as a Conjugate Pair) are a set of two candidate numbers sited in two cells that reside in the same row, column or box. Clearly in this situation, the solution will contain those values in those two cells (one in one, the other in the other), and all other candidates with those numbers can be safely removed from the row, column or box they have in common.

As a consequence of this furthermore reduction, possible values on unit of rows, columns and boxes have values eliminated when naked twins are present, simplifying the subsequent search process, which is described in more detail the following second question.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
  
A: Even if elimination, only choice and naked twins are strategies that can reduce the complexity in board (by reducing the numbers that a square can actually take) they will seldom simply solve the game for you. 

You need to search among the possible solutions until you find one. In order to do so you use constrained search (search is used throughout AI from Game-Playing to Route Planning to efficiently find solutions), a search that takes into account the limitations in the numbers that a cell can take based on the situation of the other cells.

Simple search just systematically tries all possible solutions on a board until it hits one that works. Actually that is not guaranteed to be fast, instead it might take forever to run: there are 4.62838344192 × 10^38 potential solutions (not certainly all correct one) for the whole puzzle. Constrained search doesn't try anything, it starts trying a possible solution by deciding on a cell's value and if that doesn't work it learns to exclude all other possible configurations that contain the cell's value that doesn't work. A value doesn't work if it breaks any of the limitations we mentioned above. 

This means that of all the possible solutions, a constrained search will quickly find only those which satisfy fully the constraints we imposed. By default we impose the constraints required by the game by ordering to the search not repeating the same number on any row, column or squares in the board. 

In the same fashion we can require that numbers won't be repeated also on the diagonalas. Thus, we add other two constraints (after rows, columns and squares) representing the main diagonals of the the board and start the search. That will suffice to find a valid solution that respects the diagonal sudoku problem.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

