import math
import random
import time


# Viesturs Jūlijs Lasmanis, vl19039
# Mazais Praktiskais Darbs
# Galvenais fails priekš "No-three-in-line" problēmas.


# --------------------------------------------------------
# Te tiek definēta problēma un tās domēns
class ThreeDotsProblem:
    # Te radu pašu go laukumu un patvaļīgu sākotnējo izkārtojumu, ja nav dots
    # Definēju domēnu: board_size, dot_count
    def __init__(self, board_size, dot_count, state=[]):
        self.board_size = board_size
        self.dot_count = dot_count
        self.state = state
        if not state:
            self.generate_start_state()
        self.score = calculate_score(self.state, self.board_size)

    # Sākuma stāvokļa ģenerēšana pielietojot "first fit" metodi
    def generate_start_state(self):
        x = 0
        best_state = []
        for i in range(self.dot_count):
            best_y = -1
            best_score = self.dot_count
            for y in range(self.board_size):
                if [x, y] not in best_state:
                    new_score = dot_score([x, y], best_state, self.board_size)
                    if new_score < best_score:
                        best_y = y
                        best_score = new_score
            if best_y != -1 and [x, best_y] not in best_state:
                best_state.append([x, best_y])
            else:
                raise ValueError("Too many dots!")
            x += 1
            if x >= self.board_size:
                x = 0
        self.state = best_state

    def update_state(self, new_state, new_score):
        self.state = new_state
        self.score = new_score

    def move_dot(self, dot, new_dot):
        new_state = self.state.copy()
        new_score = self.score
        new_state.remove(dot)
        new_score = new_score - dot_score(dot, new_state, self.board_size) + dot_score(new_dot, new_state,
                                                                                       self.board_size)
        new_state.append(new_dot)
        return new_state, new_score


# --------------------------------------------------------
# Te ir novērtējuma funkcijas
# Novērtē cik three-in-line rindās šis punkts atrodas.
# Pārspīlēti sarežģīta novērtējuma funkcija o(*￣▽￣*)ブ
def dot_score(dot, dot_set, n):
    score = 0
    unseen_dots = dot_set.copy()
    if dot in unseen_dots:
        unseen_dots.remove(dot)
    examined_dots = []
    for j in unseen_dots:
        if j not in examined_dots:
            if j[0] - dot[0] == 0:
                intersections = [[j[0], y] for y in range(n) if [j[0], y] in unseen_dots]
            else:
                a = (j[1] - dot[1]) / (j[0] - dot[0])
                b = dot[1] - a * dot[0]
                # Pašlaik uzstādīju absolūto toleranci kā 1e-9, ja rezultāts ir intervālā, tad var pieņemt 0.
                # Laikam vajadzētu strādāt līdz pat aptuveni n < 10**9, varbūt??? (っ °Д °;)っ
                intersections = [inter for inter in unseen_dots if
                                 math.isclose(a * inter[0] + b - inter[1], 0, abs_tol=1e-9)]
            for x in intersections:
                if x not in examined_dots:
                    examined_dots.append(x)
            if len(intersections) > 1:
                score += 1
    return score


# Pilns laukuma stāvokļa novērtējums
def calculate_score(state, n):
    score = 0
    state_copy = state.copy()
    unseen_dots = state.copy()
    for i in state_copy:
        unseen_dots.remove(i)
        score += dot_score(i, unseen_dots, n)
    return score


# --------------------------------------------------------
# Te ir kaut kāds mēģinājums Gājienu funkcijas un metodes aprakstei pielietojot Simulated Annealing
class SimulatedAnnealingSolver:
    def __init__(self, max_iterations, problem: ThreeDotsProblem):
        # Limitācijas Simulated Annealing pieejai
        self.max_iterations = max_iterations
        self.min_temperature = 0.01
        self.max_guess = 1000
        # Risinājuma informācija
        self.problem = problem
        self.best_solution = problem
        self.iteration = 0
        self.guesses = 0

    def temperature(self):
        return 1 - (self.iteration+1) / self.max_iterations

    # Nezinu varbūt vajadzētu pamainīt atļauto minējumu skaitu （*゜ー゜*）
    def solver(self):
        while self.temperature() > self.min_temperature and self.problem.score != 0 and self.guesses < self.max_guess:
            self.guesses += 1
            self.try_move()

    def try_move(self):
        # Ģenerē patvaļīgu gājienu patvaļīgam punktam vienas kolonnas ietvaros.
        rand1 = random.randint(0, self.problem.dot_count - 1)
        old_dot = self.problem.state[rand1]

        choices = []
        for y in range(self.problem.board_size):
            if [old_dot[0], y] not in self.problem.state:
                choices.append(y)
        if not choices:
            return
        rand2 = random.randint(0, len(choices) - 1)
        new_dot = [old_dot[0], choices[rand2]]
        new_state, new_score = self.problem.move_dot(old_dot, new_dot)

        # Pārbaudu vai ir nepieciešams akceptēt uzģenerēto gājienu
        rand3 = random.random()
        accept_chance = math.e ** ((self.problem.score - new_score) / self.temperature())
        if (self.problem.score - new_score) > 0 or rand3 < accept_chance:
            self.problem.update_state(new_state, new_score)
            self.iteration += 1
            self.guesses = 0
            if self.problem.score < self.best_solution.score:
                self.best_solution = self.problem


# --------------------------------------------------------
# Šī ir galvenā funkcija, kas izsauc risinājumu.
# Šo funkciju arī primāri izsauc testēšānas failā.
def solve_problem(n, k):
    if not isinstance(n, int) or not isinstance(k, int):
        print("Please enter a positive integer for grid size and dot amount!".format(k, n, n))
        return
    elif n < 1 or k < 1:
        print("Please enter a positive integer for grid size and dot amount!".format(k, n, n))
        return
    elif k > n * n:
        print("Impossible to place {} dots on {}x{} grid without overlapping!".format(k, n, n))
        return
    else:
        problem = ThreeDotsProblem(n, k)
        solver = SimulatedAnnealingSolver(100*k, problem)
        solver.solver()

        print("Finished searching for solution of {} dots in {}x{} grid!".format(k, n, n))
        print(solver.best_solution.state)
        print("Solution score: {}".format(solver.best_solution.score))
        print("Solution found in {} iterations".format(solver.iteration))
        return


# Paņem lietotāja ievadu priekš patvaļīgu datu ievades
def main():
    n = int(input("Enter board size: "))
    k = int(input("Enter dot count: "))
    start = time.time()
    solve_problem(n, k)
    end = time.time()
    print("Solution found in {:0.2f} seconds".format(end-start))


if __name__ == "__main__":
    main()
