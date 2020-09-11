import math
import time
ref = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = 0
file = open("sudoku_puzzles_1.txt")
symbol_set = ""
subblock_height = 0
subblock_width = 0
board = ""
constraints = []
neighbors = {}
call_count = 0


def get_index(x, y):
    index = 0
    index += N * x
    index += y
    return index


def display(state):
    count = 1
    for a in state:
        if count % N == 0:
            print(a + " ")
        else:
            print(a + " ", end="", flush=True)
        count += 1


def symbol(length):
    global symbol_set
    symbol_set = ""
    for a in range(0, length):
        symbol_set = symbol_set + ref[a]


def height_width(root):
    global subblock_height
    global subblock_width
    if root % 1 == 0.0:
        subblock_height = int(root)
        subblock_width = int(root)
    else:
        high = int(root)
        while N % high != 0:
            high -= 1
        subblock_height = high
        wide = int(root) + 1
        while N % wide != 0:
            wide += 1
        subblock_width = wide


def instances(board):
    symbol_instances = {}
    for a in board:
        if a in symbol_instances:
            temp = symbol_instances[a]
            symbol_instances[a] = temp + 1
        else:
            symbol_instances[a] = 0


def set_constraints():
    global constraints
    constraints = []
    for c in range(subblock_width, N + 1, subblock_width):
        max = c
        min = c - subblock_width
        subblock = []
        for d in range(min, max):
            for e in range(0, subblock_height):
                subblock.append(get_index(e, d))
        constraints.append(subblock)
    old = constraints[:]
    for g in range(0, N // subblock_height - 1):
        temp = []
        for h in old:
            temp_2 = []
            for i in range(0, len(h)):
                temp_2.append(h[i] + (subblock_height * N))
            temp.append(temp_2)
            constraints.append(temp_2)
        old = temp[:]
    for a in range(0, N):
        row = []
        column = []
        for b in range(0, N):
            row.append(a * N + b)
            column.append(a + b * N)
        if row not in constraints:
            constraints.append(row)
        if column not in constraints:
            constraints.append(column)


def set_neighbors():
    global neighbors
    neighbors = {}
    for a in constraints:
        for b in range(0, len(a)):
            for c in range(b + 1, len(a)):
                if a[b] in neighbors:
                    if a[c] not in neighbors[a[b]]:
                        temp = neighbors[a[b]]
                        temp.append(a[c])
                        neighbors[a[b]] = temp
                else:
                    neighbors[a[b]] = [a[c]]
                if a[c] in neighbors:
                    if a[b] not in neighbors[a[c]]:
                        temp = neighbors[a[c]]
                        temp.append(a[b])
                        neighbors[a[c]] = temp
                else:
                    neighbors[a[c]] = [a[b]]


def set_possible(state):
    temp = {}
    for a in range(0, len(state)):
        if state[a] != ".":
            temp[a] = state[a]
        else:
            empty = symbol_set
            for b in neighbors[a]:
                if state[b] in empty:
                    empty.replace(state[b], "")
            temp[a] = empty
    return temp


def sudoku_logic_2_ext(cons):
    toReturn = cons.copy()
    change = False
    for a in constraints:
        for b in symbol_set:
            count = 0
            for c in a:
                if b in toReturn[c]:
                    count += 1
                    index = c
                    num = b
            if count == 1:
                toReturn[index] = num
                change = True
    return toReturn, change


def sudoku_logic_1_ext(cons):
    toReturn = cons.copy()
    solved = []
    change = False
    for a in toReturn:
        if len(toReturn[a]) == 1:
            solved.append(a)
    while len(solved) > 0:
        s = solved.pop()
        for b in neighbors[s]:
            if toReturn[s] in toReturn[b]:
                toReturn[b] = toReturn[b].replace(toReturn[s], "")
                change = True
                if len(toReturn[b]) == 1:
                    solved.append(b)
    return toReturn, change


def get_next_unassigned_var(cons):
    pos = -1
    m = 10000000000
    for a in cons:
        if 1 < len(cons[a]) < m:
            if len(cons[a]) == 2:
                return a
            m = len(cons[a])
            pos = a
    return pos


def goal_test(state):
    return "." not in state


def build_board(cons):
    temp = []
    for a in range(0, N * N):
        temp.append(cons[a])
    return ''.join(temp)


def csp_ext(state, cons):
    global call_count
    if goal_test(state):
        return state
    var = get_next_unassigned_var(cons)
    if var == -1:
        return build_board(cons)
    for val in cons[var]:
        new_state = state[:var] + val + state[var + 1:]
        (new_constraints, changed) = sudoku_logic_1_ext(sudoku_logic_2_ext(modify_possible(cons, var, val))[0])
        count = 0
        while changed:
            if count % 2 == 0:
                (new_constraints, changed) = sudoku_logic_2_ext(new_constraints)
            else:
                (new_constraints, changed) = sudoku_logic_1_ext(new_constraints)
            count += 1
        if impossible_state(new_constraints):
            continue
        call_count += 1
        result = csp_ext(new_state, new_constraints)
        if result is not None:
            return result
    return None


def modify_possible(cons, var, val):
    toReturn = cons.copy()
    toReturn[var] = val
    return toReturn


def impossible_state(cons):
    for a in cons:
        if len(cons[a]) < 1:
            return True
    return False


def correct():
    for a in constraints:
        ref = {}
        for b in a:
            if board[b] in ref:
                ref[board[b]] = ref[board[b]] + 1
            else:
                ref[board[b]] = 1
        for c in ref:
            if ref[c] > 1:
                return False
    return True


count = 0
total = 0
total_calls = 0
for line in file:
    if count == 105:
        count += 1
        continue
    a = line.split()
    board = a[0]
    N = int(math.sqrt(len(a[0])))
    symbol(N)
    height_width(math.sqrt(N))
    set_constraints()
    set_neighbors()
    starting = sudoku_logic_1_ext(sudoku_logic_2_ext(set_possible(board))[0])[0]
    start = time.perf_counter()
    board = csp_ext(board, starting)
    end = time.perf_counter()
    total += end - start
    total_calls += call_count + 1
    print(str(count) + ": " + str(total) + "s " + str(total_calls) + " calls" + " " + board + " " + str(correct()))
    call_count = 0
    count += 1
