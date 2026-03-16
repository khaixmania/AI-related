"""NAMES OF THE AUTHOR(S): Alice Burlats <alice.burlats@uclouvain.be>"""

from pycsp3 import *


def solve_minesweeper(clues: list[list[int]]) -> list[(int, int)]:
    n = len(clues)
    m = len(clues[0])
    x = VarArray(size=[n, m], dom = {0,1})
    #bombre représentée par -1
    satisfy(
        #[(x[i][j] < 6) for i in [0, n-1] for j in range(1, m-1)], check if les éléments en bordures horizontal on un nombre possible de bombes (<6)
        #[(x[i][j] < 6) for i in range(1, n-1) for j in [0, m-1]], #check if les éléments en bordures verticales on un nombre possible de bombes (<6)
        #[(x[i][j] < 4) for i in [0, n-1] for j in [0, m-1]], #check if the corner are < 4
        [(x[i][j] == 0)
        for i in range(n)
        for j in range(m)
        if clues[i][j] != -1],

        #Tout ce qui n'est pas en bordure (8 cases à vérifier)
        [Sum((x[i+dec_i][j+dec_j])
         for dec_i in [-1,0,1]
         for dec_j in [-1,0,1]
         if not(dec_i == 0 and dec_j == 0)) == clues[i][j]
         for i in range(1, n-1)
         for j in range(1, m-1)
         if clues[i][j] != -1],

        #BORDURE sauf les coins (5cases à verifier)
        #bordure du bas
        [Sum((x[n-1+dec_i][j+dec_j])
         for dec_i in [-1,0]
         for dec_j in [-1,0,1]
         if not(dec_i == 0 and dec_j == 0)) == clues[n-1][j]
         for j in range(1, m-1)
         if clues[n-1][j] != -1],

         #bordure du haut
         [Sum((x[0+dec_i][j+dec_j])
         for dec_i in [0,1]
         for dec_j in [-1,0,1]
         if not(dec_i == 0 and dec_j == 0)) == clues[0][j]
         for j in range(1, m-1)
         if clues[0][j] != -1],

         #bordure de gauche
         [Sum((x[i+dec_i][0+dec_j])
         for dec_i in [-1,0,1]
         for dec_j in [0,1]
         if not(dec_i == 0 and dec_j == 0)) == clues[i][0]
         for i in range(1, n-1)
         if clues[i][0] != -1],

         #bordure de droite
         [Sum((x[i+dec_i][m-1+dec_j])
         for dec_i in [-1,0,1]
         for dec_j in [-1,0]
         if not(dec_i == 0 and dec_j == 0)) == clues[i][m-1]
         for i in range(1, n-1)
         if clues[i][m-1] != -1],

         #COIN
         #hg
         [Sum((x[dec_i][dec_j])
         for dec_i in [0,1]
         for dec_j in [0,1]
         if not(dec_i == 0 and dec_j == 0)) == clues[0][0]]
         if clues[0][0] != -1 else [],

         #bg
         [Sum((x[n-1+dec_i][dec_j])
         for dec_i in [0,-1]
         for dec_j in [0,1]
         if not(dec_i == 0 and dec_j == 0)) == clues[n-1][0]]
         if clues[n-1][0] != -1 else [],

         #hd
         [Sum((x[dec_i][m-1+dec_j])
         for dec_i in [0,1]
         for dec_j in [-1,0]
         if not(dec_i == 0 and dec_j == 0)) == clues[0][m-1]]
         if clues[0][m-1] != -1 else [],

         #bd
         [Sum((x[n-1+dec_i][m-1+dec_j])
         for dec_i in [-1,0]
         for dec_j in [-1,0]
         if not(dec_i == 0 and dec_j == 0)) == clues[n-1][m-1]]
         if clues[n-1][m-1] != -1 else [],
    )
    # Solve the problem and print the solution if found
    if solve(solver=CHOCO) is SAT:
        print("SATISFIABLE")
        vals = values(x)
        bombs = []
        for i in range(n):
            for j in range(m):
                if vals[i][j] == 1:
                    bombs.append((i,j))
        return bombs 
    else:
        print("UNSATISFIABLE")
        return None


def check_solution(clues: list[list[int]], solution: list[(int, int)]) -> bool:
    n = len(clues)
    m = len(clues[0])
    mines_count = [[0 for _ in range(m)] for _ in range(n)]
    for x, y in solution:
        if clues[x][y] != -1:
            print(f"A mine is placed on a clue at position ({x},{y}), invalid solution")
            return False

        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if 0 <= x+a < n and 0 <= y + b < m and (a != 0 or b != 0):
                    mines_count[x + a][y + b] += 1

    for i in range(n):
        for j in range(m):
            if mines_count[i][j] != clues[i][j] and clues[i][j] != -1:
                print(f"The clue at position ({i},{j}) is not respected: there is {mines_count[i][j]} mines instead of {clues[i][j]}")
                return False

    return True


def parse_instance(input_file: str) -> list[list[int]]:
    with open(input_file) as input:
        lines = input.readlines()
    clues = []
    for line in lines:
        row = []
        for cell in line.strip().split(" "):
            row.append(int(cell))
        clues.append(row)
    return clues


if __name__ == '__main__':
    clues = parse_instance("instances/sat/i01.txt")
    solution = solve_minesweeper(clues)
    if solution is not None:
        if check_solution(clues, solution):
            print("The returned solution is valid")
        else:
            print("The returned solution is not valid")
    else:
        print("No solution found")
