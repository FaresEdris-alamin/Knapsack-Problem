import random

def knapsack_genetic_algorithm():
    # Get user inputs
    capacity = int(input("Enter the knapsack capacity: "))
    num_items = int(input("Enter the number of items: "))
    item_weights = [int(input(f"Enter weight of item {i + 1}: ")) for i in range(num_items)]
    item_values = [int(input(f"Enter value of item {i + 1}: ")) for i in range(num_items)]

    problem_type = input("Enter '0-1' for 0-1 knapsack or 'unbounded' for unbounded knapsack: ")

    # Create initial population
    population_size = int(input("Enter the population size: "))
    population = generate_population(population_size, num_items)

    generations = int(input("Enter the number of generations: "))

    for generation in range(generations):
        # Evaluate fitness
        fitness_scores = evaluate_fitness(population, item_weights, item_values, capacity)

        # Select parents
        parents = select_parents(population, fitness_scores)

        # Crossover
        children = crossover(parents)

        # Mutation
        children = mutate(children)

        # Replace old population with new population
        population = children

    # Find the best solution in the final population
    best_solution_index = fitness_scores.index(max(fitness_scores))
    best_solution = population[best_solution_index]
    print("\nBest solution:")
    print("Selected items:", [i + 1 for i in range(num_items) if best_solution[i] == 1])
    print("Total value:", sum([item_values[i] for i in range(num_items) if best_solution[i] == 1]))

def generate_population(population_size, num_items):
    return [[random.randint(0, 1) for _ in range(num_items)] for _ in range(population_size)]

def evaluate_fitness(population, item_weights, item_values, capacity):
    fitness_scores = []
    for individual in population:
        total_weight = sum([item_weights[i] for i in range(len(individual)) if individual[i] == 1])
        total_value = sum([item_values[i] for i in range(len(individual)) if individual[i] == 1])

        # Penalize solutions that exceed capacity
        if total_weight > capacity:
            fitness_scores.append(0)
        else:
            fitness_scores.append(total_value)
    return fitness_scores

def select_parents(population, fitness_scores):
    # Using tournament selection for simplicity
    tournament_size = 3
    parents = []
    for _ in range(len(population)):
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        selected_index = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        parents.append(population[selected_index])
    return parents

def crossover(parents):
    crossover_rate = 0.8
    children = []

    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]

        if random.random() < crossover_rate:
            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
        else:
            child1 = parent1
            child2 = parent2

        children.append(child1)
        children.append(child2)

    return children

def mutate(children):
    mutation_rate = 0.1

    for i in range(len(children)):
        for j in range(len(children[i])):
            if random.random() < mutation_rate:
                children[i][j] = 1 - children[i][j]

    return children

# Run the genetic algorithm
knapsack_genetic_algorithm()
