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


def get_next_unassigned_var(state):
    return state.index(".")


def get_sorted_values(state, var):
    empty = []
    for a in symbol_set:
        empty.append(a)
    for b in neighbors[var]:
        if state[b] in empty:
            empty.remove(state[b])
    return empty


def goal_test(state):
    return "." not in state


def csp(state):
    global call_count
    if goal_test(state):
        return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        new_state = state
        new_state = replace(new_state, var, val)
        call_count += 1
        result = csp(new_state)
        if result is not None:
            return result
    return None


def replace(s, a, b):
    n = list(s)
    n[a] = b
    return ''.join(n)


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
    a = line.split()
    board = a[0]
    N = int(math.sqrt(len(a[0])))
    symbol(N)
    height_width(math.sqrt(N))
    set_constraints()
    set_neighbors()
    start = time.perf_counter()
    board = csp(board)
    end = time.perf_counter()
    total += end - start
    total_calls += call_count
    print(str(count) + ": " + str(total) + "s " + str(total_calls) + " calls " + board + " " + str(correct()))
    call_count = 0
    # if count == 50:
    #     print(board)
    #     break
    count += 1
