# ANT COLONY OPTIMIZATION
import numpy as np
import random


class AntColony:
    def __init__(
        self, dist_matrix, n_ants, n_best, n_iterations, decay, alpha=1, beta=2
    ):
        self.dist_matrix = dist_matrix
        self.pheromone = np.ones(dist_matrix.shape) / len(dist_matrix)
        self.all_inds = range(len(dist_matrix))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for _ in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone *= 1 - self.decay
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.dist_matrix[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.dist_matrix[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for _ in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.path_distance(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for _ in range(len(self.dist_matrix) - 1):
            move = self.pick_move(self.pheromone[prev], self.dist_matrix[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))  # return to start
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone**self.alpha * ((1.0 / dist) ** self.beta)
        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move

    def path_distance(self, path):
        total = 0
        for ele in path:
            total += self.dist_matrix[ele]
        return total


def run_aco():
    # Sample distance matrix (you can modify this)
    cities = 5
    np.random.seed(42)
    dist_matrix = np.random.randint(1, 100, size=(cities, cities))
    np.fill_diagonal(dist_matrix, 999999)  # large number to prevent loops

    aco = AntColony(dist_matrix, n_ants=10, n_best=5, n_iterations=50, decay=0.1)
    path, distance = aco.run()
    return path, distance
