LandM_Classifier='''
import numpy as np

class Perceptron:
    def __init__(self,input_size):
        self.weights = np.random.rand(input_size)
        self.bias = np.random.rand(1)

    def activation(self, x):
        return 1 if x > 0 else 0
    
    def predict(self,X):
        summation = np.dot(X, self.weights) + self.bias
        return self.activation(summation)
    
    def train(self, X, y, learning_rate, epochs):
        for _ in range(epochs):
            for input,label in zip(X,y):
                pred = self.predict(input)
                error = label - pred
                self.weights += learning_rate*error*input
                self.bias += learning_rate*error

#This is a 5x4 matrix which resembles an L
# 10000
# 10000
# 10000
# 11111

#This is a 5x4 matrix which represents an M
# 10001
# 11011
# 10101
# 10001

input_data = np.array([
    [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,1,1,1], #L ko ek single array mai daal diya hai
    [1,0,0,0,1,1,1,0,1,1,1,0,1,0,1,1,0,0,0,1] #Same for M
])

labels = np.array([0,1]) #0 for L, 1 for M

perceptron = Perceptron(input_size=20)

perceptron.train(input_data,labels,learning_rate=0.1,epochs=100)

for x in input_data:
    pred = perceptron.predict(x)
    print(f"Input = {x}, prediction - {pred}")
'''

a_star='''
class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis
    
    def get_neighbors(self, v):
        return self.adjac_lis[v]
    
    def heuristic(self, n):
        H = {
            'S': 15,
            '1': 14,
            '2': 10,
            '3': 8,
            '4': 12,
            '5': 10,
            '6': 10,
            '7': 0
        }
        return H[n]
    
    def a_star(self, start, stop):
        open_list = set([start])
        closed_list = set([])
        distance = {} # Distance from Start.
        distance[start] = 0
        adjacent_nodes = {} # Adjacent Mapping of all Nodes
        adjacent_nodes[start] = start
        
        while len(open_list) > 0:
            n = None
            for v in open_list:
                if n is None or distance[v] + self.heuristic(v) < distance[n] + self.heuristic(n):
                    n = v
            
            if n is None:
                print('Path does not exist!')
                return None
            
            if n == stop: # If the current node is the stop, we have found the path
                reconst_path = []
                while adjacent_nodes[n] != n:
                    reconst_path.append(n)
                    n = adjacent_nodes[n]
                reconst_path.append(start)
                reconst_path.reverse()
                print('\\nPath found: {}\\n'.format(reconst_path))
                return reconst_path
            
            for (m, weight) in self.get_neighbors(n): # Neighbors of the current node
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    adjacent_nodes[m] = n
                    distance[m] = distance[n] + weight
                else: # Check if it's quicker to visit n than m
                    if distance[m] > distance[n] + weight:
                        distance[m] = distance[n] + weight
                        adjacent_nodes[m] = n          
                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)
            
            open_list.remove(n) # Since all neighbors are inspected
            closed_list.add(n)
            
            print("OPEN LIST: ", end="")
            print(open_list)
            print("CLOSED LIST: ", end="")
            print(closed_list)
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        
        print('Path does not exist!')
        return None

adjacent_list2 = {
    'S': [('1', 3), ('4', 4)],
    '1': [('S', 3), ('2', 4), ('4', 5)],
    '2': [('1', 4), ('3', 4), ('5', 5)],
    '3': [('2', 4)],
    '4': [('S', 4), ('1', 5), ('5', 2)],
    '5': [('4', 2), ('2', 5), ('6', 4)],
    '6': [('5', 4), ('7', 3)],
    '7': [('6', 3)],
}

g = Graph(adjacent_list2)
g.a_star('S', '7')
'''

bfs_dfs_dfid='''
from collections import deque

def dfs(graph, start, visited):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start, end=' ')
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def dfid(graph, start, depth, visited=None):
    if visited is None:
        visited = set()
    if depth > 0:
        print(start, end=' ')
        visited.add(start)
        for neighbor in graph[start]:
            if neighbor not in visited:
                dfid(graph, neighbor, depth - 1, visited)

# Example usage:

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    while queue:
        node = queue.popleft()
        print(node, end=' ')
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# Example usage:
print("\\nBFS traversal:")
bfs(graph, 'A')
print("\\nDFID traversal:")
dfid(graph, 'A', 2)
print("\\nDFS traversal:")
dfs(graph, 'A',None)
'''

genetic_algo='''
from numpy.random import randint, rand
import math

def crossover(parent1, parent2, r_cross):
    child1, child2 = parent1.copy(), parent2.copy()
    r = rand()
    point = 0
    if r > r_cross:
        point = randint(1, len(parent1) - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2, point

def mutate(chromosome, r_mut):
    for i in range(len(chromosome)):
        if rand() < r_mut:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

def bin_to_dec(bin):
    decimal = 0
    for i in range(len(bin)):
        decimal += bin[i] * pow(2, 4 - i)
    return decimal

def dec_to_bin(dec):
    binaryVal = []
    while dec > 0:
        binaryVal.append(dec % 2)
        dec = math.floor(dec / 2)
    for _ in range(5 - len(binaryVal)):
        binaryVal.append(0)
    binaryVal = binaryVal[::-1]
    return binaryVal

def fitness_function(x):
    return pow(x, 2)

def genetic_algorithm(iterations, population_size, r_cross, r_mut):
    input = [randint(0, 32) for _ in range(population_size)]
    pop = [dec_to_bin(i) for i in input]
    for generation in range(iterations):
        print(f"\\nGeneration : {generation + 1}", end="\\n\\n")
        decimal = [bin_to_dec(i) for i in pop]
        fitness_score = [fitness_function(i) for i in decimal]
        f_by_sum = [fitness_score[i] / sum(fitness_score) for i in range(population_size)]
        exp_cnt = [fitness_score[i] / (sum(fitness_score) / population_size) for i in range(population_size)]
        act_cnt = [round(exp_cnt[i]) for i in range(population_size)]
        print("SELECTION\\n\\nInitial Population\\tDecimal Value\\tFitness Score\\tFi/Sum\\tExpected count\\tActual Count")
        for i in range(population_size):
            print(
                pop[i],
                "\\t",
                decimal[i],
                "\t\t",
                fitness_score[i],
                "\t\t",
                round(f_by_sum[i], 2),
                "\t\t",
                round(exp_cnt[i], 2),
                "\t\t",
                act_cnt[i],
            )
        print("Sum : ", sum(fitness_score))
        print("Average : ", sum(fitness_score) / population_size)
        print("Maximum : ", max(fitness_score), end="\\n")
        max_count = max(act_cnt)
        min_count = min(act_cnt)
        max_count_index = 0
        for i in range(population_size):
            if max_count == act_cnt[i]:
                max_count_index = i
                break
        for i in range(population_size):
            if min_count == act_cnt[i]:
                pop[i] = pop[max_count_index]
        crossover_children = list()
        crossover_point = list()
        for i in range(0, population_size, 2):
            child1, child2, point_of_crossover = crossover(pop[i], pop[i + 1], r_cross)
            crossover_children.append(child1)
            crossover_children.append(child2)
            crossover_point.append(point_of_crossover)
            crossover_point.append(point_of_crossover)
        print("\\nCROSS OVER\\n\\nPopulation\\t\\tMate\\t Crossover Point\\t Crossover Population")
        for i in range(population_size):
            if (i + 1) % 2 == 1:
                mate = i + 2
            else:
                mate = i
            print(
                pop[i],
                "\\t",
                mate,
                "\\t",
                crossover_point[i],
                "\\t\\t\\t",
                crossover_children[i],
            )
        mutation_children = list()
        for i in range(population_size):
            child = crossover_children[i]
            mutation_children.append(mutate(child, r_mut))
        new_population = list()
        new_fitness_score = list()
        for i in mutation_children:
            new_population.append(bin_to_dec(i))
        for i in new_population:
            new_fitness_score.append(fitness_function(i))
        print("\\nMUTATION\\n\\nMutation population\\t New Population\\t Fitness Score")
        for i in range(population_size):
            print(
                mutation_children[i],
                "\t",
                new_population[i],
                "\\t\\t",
                new_fitness_score[i],
            )
        print("Sum : ", sum(new_fitness_score))
        print("Maximum : ", max(new_fitness_score))
        pop = mutation_children

genetic_algorithm(iterations=2, population_size=4, r_cross=0.5, r_mut=0.05)
'''

hill_climb='''
# import random

# def random_solution(tsp):
#     cities = list(range(len(tsp)))
#     solution = []
#     for i in range(len(tsp)):
#         random_city = cities[random.randint(0, len(cities) - 1)]
#         solution.append(random_city)
#         cities.remove(random_city)
#     return solution

# def route_length(tsp, solution):
#     length = 0
#     for i in range(len(solution)):
#         length += tsp[solution[i - 1]][solution[i]]
#     return length

# def get_neighbours(solution):
#     neighbours = []
#     for i in range(len(solution)):
#         for j in range(i + 1, len(solution)):
#             neighbour = solution.copy()
#             neighbour[i] = solution[j]
#             neighbour[j] = solution[i]
#             neighbours.append(neighbour)
#     return neighbours

# def get_best_neighbour(tsp, neighbours):
#     best_length = route_length(tsp, neighbours[0])
#     best_neighbour = neighbours[0]
#     for neighbour in neighbours:
#         current_length = route_length(tsp, neighbour)
#         if current_length < best_length:
#             best_length = current_length
#             best_neighbour = neighbour
#     return best_neighbour, best_length

# def hill_climbing(tsp):
#     current_solution = random_solution(tsp)
#     current_length = route_length(tsp, current_solution)
#     neighbours = get_neighbours(current_solution)
#     best_neighbour, best_length = get_best_neighbour(tsp, neighbours)
#     while best_length < current_length:
#         current_solution = best_neighbour
#         current_length = best_length
#         neighbours = get_neighbours(current_solution)
#         best_neighbour, best_length = get_best_neighbour(tsp, neighbours)
#     return current_solution, current_length

# def main():
#     tsp = [
#         [0, 100, 700, 50],
#         [100, 0, 330, 1200],
#         [700, 330, 0, 400],
#         [50, 1200, 400, 0]
#     ]
#     print(hill_climbing(tsp))

# if __name__ == "__main__":
#     main()

def f(x):
    value = x
    return value


def hillclimb():
    graph = [
        [5, 12, 8, 3, 19, 25, 10, 7],
        [15, 22, 18, 13, 29, 35, 20, 17],
        [25, 32, 28, 23, 39, 45, 30, 27],
        [35, 42, 38, 33, 49, 55, 40, 37],
        [45, 52, 48, 43, 59, 65, 50, 47],
        [55, 62, 58, 53, 69, 75, 60, 57],
        [65, 72, 68, 63, 79, 85, 70, 67],
        [75, 82, 78, 73, 89, 95, 80, 77]
    ]

    state = [0, 0]
    max_val = float('-inf')
    while True:
        old_val = max_val
        x = state[0]
        y = state[1]
        possible_moves = [[x+1, y], [x-1, y], [x+1, y+1],
                          [x-1, y-1], [x+1, y-1], [x-1, y+1], [x, y-1], [x, y+1]]
        for x1, y1 in possible_moves:
            if 0 <= x1 < 8 and 0 <= y1 < 8:
                val = f(graph[x1][y1])
                if val > max_val:
                    print(val)
                    max_val = val
                    state = [x1, y1]
        if old_val == max_val:
            print(state)
            break

    print(f"Max Value is {max_val} at state {state}")


hillclimb()
'''

perceptron='''
import numpy as np

class Perceptron:
    def __init__(self, input_size, learning_rate=0.1, epochs=100):
        self.weights = np.random.rand(input_size)
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.bias = np.random.rand(1)
    
    def activate(self, x):
        return 1 if x >= 0 else 0
    
    def predict(self, inputs):
        summation = np.dot(inputs, self.weights) + self.bias
        return self.activate(summation)
    
    def train(self, training_data, labels):
        for _ in range(self.epochs):
            for inputs, label in zip(training_data, labels):
                prediction = self.predict(inputs)
                self.weights += self.learning_rate * (label - prediction) * inputs
                self.bias += self.learning_rate * (label - prediction)

def main():
    # AND gate training data
    training_data = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    labels = np.array([0, 0, 0, 1])
    
    # Create a perceptron with 2 input neurons (matching the AND gate input size)
    perceptron = Perceptron(input_size=2)
    
    # Train the perceptron
    perceptron.train(training_data, labels)
    
    # Test the perceptron
    test_data = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    
    print("Test Results:")
    for inputs in test_data:
        prediction = perceptron.predict(inputs)
        print(f"Inputs: {inputs}, Prediction: {prediction}")

if __name__ == "__main__":
    main()
'''

rulebasedsystem='''
class LeaveApprovalExpertSystem:
    def __init__(self, leave_balance, team_workload):
        self.leave_balance = leave_balance
        self.team_workload = team_workload

    def process_leave_request(self, leave_duration):
        if leave_duration <= self.leave_balance:
            return "Leave Approved"
        elif leave_duration > self.leave_balance and leave_duration <= (self.leave_balance + 5):
            return "Leave Approved with Deduction"
        elif self.team_workload == "High":
            return "Leave Denied - High Workload"
        else:
            return "Leave Denied - Unknown Reason"

# Example Usage:
leave_system = LeaveApprovalExpertSystem(10, "Medium")

# Employee requests leave for 8 days
result = leave_system.process_leave_request(8)
print(result)

# Employee requests leave for 15 days
result = leave_system.process_leave_request(15)
print(result)

# Employee requests leave during a high workload period
leave_system.team_workload = "High"
result = leave_system.process_leave_request(5)
print(result)
'''

wumpus_world='''
import random

class WumpusWorldAgent:
    def __init__(self, size):
        self.size = size
        self.visited = [[False] * size for _ in range(size)]
        self.current_location = (0, 0)
    
    def move(self, direction):
        x, y = self.current_location
        if direction == 'up' and x > 0:
            self.current_location = (x - 1, y)
        elif direction == 'down' and x < self.size - 1:
            self.current_location = (x + 1, y)
        elif direction == 'left' and y > 0:
            self.current_location = (x, y - 1)
        elif direction == 'right' and y < self.size - 1:
            self.current_location = (x, y + 1)
    
    def explore(self):
        while True:
            self.visited[self.current_location[0]][self.current_location[1]] = True
            print(f"Current Location: {self.current_location}")
            
            if self.check_for_gold():
                print("Agent found the gold!")
                break
            
            safe_moves = self.get_safe_moves()
            if not safe_moves:
                print("Agent is trapped or couldn't find the gold.")
                break
            
            next_move = random.choice(safe_moves)
            self.move(next_move)
    
    def check_for_gold(self):
        x, y = self.current_location
        # Simulating the presence of gold at coordinates (size-1, size-1)
        return x == self.size - 1 and y == self.size - 1
    
    def get_safe_moves(self):
        x, y = self.current_location
        safe_moves = []
        
        # Check and add safe moves
        if x > 0 and not self.visited[x - 1][y]:
            safe_moves.append('up')
        if x < self.size - 1 and not self.visited[x + 1][y]:
            safe_moves.append('down')
        if y > 0 and not self.visited[x][y - 1]:
            safe_moves.append('left')
        if y < self.size - 1 and not self.visited[x][y + 1]:
            safe_moves.append('right')
        
        return safe_moves

# Create a Wumpus World agent with a 4x4 grid
agent = WumpusWorldAgent(size=4)

# Start exploring the world
agent.explore()
'''

ai_exp={
    "LandM_Classifier.py":LandM_Classifier,
    "a_star.py":a_star,
    "bfs_dfs_dfid.py":bfs_dfs_dfid,
    "genetic_algo.py":genetic_algo,
    "hill_climb.py":hill_climb,
    "perceptron.py":perceptron,
    "rulebasedsystem.py":rulebasedsystem,
    "wumpus_world.py":wumpus_world
}

def ai_():
    for filename, content in ai_exp.items():
        print(filename)
    exp = input("Enter Code : ")
    with open(exp, 'w') as file:
        file.write(ai_exp[exp])