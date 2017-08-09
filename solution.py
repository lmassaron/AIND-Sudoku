assignments = []

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
lenght_side = len(cols)

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [A_elem+B_elem for A_elem in A for B_elem in B]

squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in squares)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    for unit in unitlist:
        possible_twins = [values[square] for square in unit if len(values[square])==2]
        if len(possible_twins) > 1:
            for candidate in set(possible_twins):
                if len([twins for twins in possible_twins if twins==candidate]) == 2:
                    for square in unit:
                        if values[square]!= candidate and [element for element in values[square] if element in candidate]:
                            print("Cleaning naked twins", candidate, "from", square, ":", values[square], end=' >>> ')
                            values[square] = ''.join([key for key in values[square] if key not in candidate])
                            print(values[square])

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
    return {row+column: '123456789' if grid[c + r * (lenght_side-1)] == '.' else grid[c + r * (lenght_side-1)] for r, row in enumerate(rows) for c, column in enumerate(cols)}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
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
    return None

def eliminate(values):
    """

    Args:
        values:

    Returns:

    """

    for square in squares:
        if len(values[square])==1:
            print("Eliminating",values[square],"found in",square)
            for peer in peers[square]:
                if values[peer] != values[square]:
                    values[peer] = ''.join([key for key in values[peer] if key!=values[square]])

    return values

def only_choice(values):
    """

    Args:
        values:

    Returns:

    """
    for digit in digits:
        for unit in unitlist:
            span = [square for square in unit if digit in values[square]]
            square = span[0]
            if len(span) == 1 and len(values[square])>1:
                print (digit, "is the only choice for", square, 'in', unit)
                values = assign_value(values, square, digit)

        return values

def reduce_puzzle(values):

    working = True

    while working:
        initial_values = values.copy()
        # Constrained programming
        working = working & ((initial_values!=eliminate(values)) | (initial_values!=only_choice(values)) | (initial_values!=naked_twins(values)))

def search(values):
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(diag_sudoku_grid)
    display(values)

    reduce_puzzle(values)

    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
