assignments = [] # This records all the board assignments
solve_diagonal = True

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
lenght_side = len(cols)

def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    
    Args:
        A: a list of string elements
        B: a list of string elements

    Returns:
        a list of concatenated A and B elements

    """
    return [A_elem+B_elem for A_elem in A for B_elem in B]

def adding_diagonal_units(considered_units):
    """
    
    Args:
        considered_units: the actual units list

    Returns:
        it updates the unit list, which contains the list of
        cell where to apply constraints, by adding the two main
        diagonals of the board

    """
    diagonals = [[r+c for r, c in zip(rows, cols)], [r+c for r, c in zip(rows, cols[::-1])]]
    return considered_units + diagonals

squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])

unitlist = adding_diagonal_units(unitlist)

units = dict((s, [u for u in unitlist if s in u])
             for s in squares)

peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in squares)

def assign_value(values, box, value):
    """
   This function has to be used to update the values dictionary.
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return dict(zip(squares, ['123456789' if c=='.' else c for c in grid]))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values:
        line = '\n+' + ('-' * 11* 3 + '+')*3 + '\n'
        for r, row in enumerate(rows):
            for c, column in enumerate(cols):
                if c % 3 == 0:
                    line += '  ' * (1 if c>0 else 0) + '| '
                vals = values[row+column]
                line += ' ' + ' '*(9-len(vals)) + vals
            if (r+1) % 3 == 0:
                line += '  |\n+' + ('-' * 11 * 3 + '+')*3 + '\n'
            else:
                line += '  |\n'

        print(line)
    else:
        print ('Not solvable')


def eliminate(values):
    """
    Pruning values using the eliminating strategy

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...} 
        containing up so far constrained opportunities for square values

    Returns:
        values(dict) updated by the eliminate strategy

    """

    for square in squares:
        if len(values[square])==1:
            solution_value = values[square]
            #print("Eliminating",values[square],"found in",square)
            for peer in peers[square]:
                values = assign_value(values, peer, values[peer].replace(solution_value,''))
    return values


def only_choice(values):
    """
    Pruning values using the only choice strategy
    
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...} 
        containing up so far constrained opportunities for square values

    Returns:
        values(dict) updated by the only choice strategy

    """

    for digit in digits:
        for unit in unitlist:
            span = [square for square in unit if digit in values[square]]
            if len(span) == 1:
                square = span[0]
                if len(values[square])>1:
                    #print (digit, "is the only choice for", square, 'in', unit)
                    values = assign_value(values, square, digit)

    return values


def naked_twins(values):
    """
    Pruning values using the naked twins strategy:
        * Find all instances of naked twins
        * Eliminate the naked twins as possibilities for their peers
    
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...} 
        containing up so far constrained opportunities for square values

    Returns:
        values(dict) updated by the naked twins strategy
    """

    for unit in unitlist:
        possible_twins = [values[square] for square in unit if len(values[square])==2]
        if len(possible_twins) > 1:
            for candidate in set(possible_twins):
                if len([twins for twins in possible_twins if twins==candidate]) == 2:
                    for square in unit:
                        if len(values[square])>1 and values[square]!= candidate and len([element for element in values[square] if element in candidate]) > 0:
                            #print("Cleaning naked twins", candidate, "from", square, ":", values[square], end=' >>> ')
                            values[square] = ''.join([key for key in values[square] if key not in candidate])
                            #print(values[square])

    return values


def check_valid(values):
    """
    
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...} 
        containing up so far constrained opportunities for square values: 

    Returns:
        a boolean revealing if the board is a valid one or not

    """
    valid = True
    for unit in unitlist:
        assigned = [values[square] for square in unit if len(values[square])==1]
        valid &= (len(assigned)==len(set(assigned)))
        if not len(assigned)==len(set(assigned)):
            print ("Non conformity problem can be retraced in unit:", unit)
    return valid


def reduce_puzzle(values):
    """
    Applying multiple strategies in series.
    
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...} 
        containing up so far constrained opportunities for square values: 

    Returns:
        values(dict) updated by the applications of the startegies

    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = (solved_values_before == solved_values_after)

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):

    """
    Using depth-first search and propagation, create a search tree on a simplified board
    (thanks to the application of reduction strategies) and it solves the sudoku (if possible).
    
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...} 
        containing up so far constrained opportunities for square values: 

    Returns:
        a solution in the form of values(dict) or a False boolean flag

    """

    # At first, reducing the puzzle using the previous function
    values = reduce_puzzle(values)

    if not values:
        return False ## It points out that it failed earlier

    if all(len(values[s]) == 1 for s in squares):
        return values  ## This is solved!

    no_options, square = min([(len(values[square]), square) for square in squares if len(values[square]) > 1])

    for value in values[square]:

        replica = values.copy()
        replica[square] = value

        attempt = search(replica)
        if attempt:  # If this branch won't lead to any valid results, it won't be returned
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)
    print("\nInitial conformity check: ", check_valid(values))
    print("Initial state of the grid:")
    display(values)

    solution = search(values)
    print("\nFinal conformity check: ", check_valid(values))

    for unit in unitlist:
        set_values = {solution[square] for square in unit}
        if len(set_values) != 9:
            print("Problems in", unit, set_values)

    return solution


if __name__ == '__main__':

    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
