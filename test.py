import random

pop_size = 10
unbounded = False
items =[(25,10),(15,15),(20,18),(30,20),(10,5)]
max_weight = 50
population =[]


def generate_population():     # Unbounded should choose any chromosome any number of times 
                       # Currently it chooses it only twice and no more than that in all attempts
        count = 0
        #for i in range(pop_size):
        while count < pop_size:    
            genes = [0, 1] if not unbounded else [0, 1, 2]  # Add 2 for unbounded knapsack
            chromosome = [random.choice(genes) for _ in range(len(items))]
            total_weight = sum(item[0] * chromosome[i] for i, item in enumerate(items))
            if total_weight <= max_weight:
                population.append(chromosome)
                count +=1
        return population

def calculate_fitness(chromosome):
        total_weight = sum(item[0] * chromosome[i] for i, item in enumerate(items))
        total_value = sum(item[1] * chromosome[i] for i, item in enumerate(items))
        return total_value if total_weight <= max_weight or not unbounded else 0

def select_chromosomes():
        
        fitness_values = [calculate_fitness(chromosome) for chromosome in population]
        fitness_values = [float(i) / sum(fitness_values) for i in fitness_values]

        #choose 20% of the population as parents
        sorted_population = [x for _, x in sorted(zip(fitness_values, population), reverse=True)]
        parents = sorted_population[:int(0.2 * len(population))]
        second_half = sorted_population[int(0.2 * len(population)):]

        return parents,second_half

def crossover(parents):
        crossover_point = random.randint(0, len(items) - 1)

        # Ensure there are at least two parents
        if len(parents) < 2:
            raise ValueError("At least two parents are required for crossover.")

        # Perform crossover between all pairs of parents
        children = []
        for i in range(0, len(parents), 2):
            parent1, parent2 = parents[i], parents[i + 1] if i + 1 < len(parents) else parents[i]
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            children.extend([child1, child2])
        return children

def mutate(chromosome):
        
        mutate_point = random.randint(0, len(items) - 1)
        chromosome[mutate_point] = random.choice([0, 1, 2]) if unbounded else 1
        return chromosome

def mutation(chromosome, p):
    # mutated chromosome intial values are zeros
    mutated_chromosome = [0 for _ in range(len(items))]
    for i in range(len(items)):
        d = chromosome[i]
        r = random.uniform(0, 1)
        if chromosome[i] == 1.0 and r < p:
            mutated_chromosome[i] = 0
        elif chromosome[i] == 0.0 and r < p:
            mutated_chromosome[i] = 1
        else:
            mutated_chromosome[i] = d
    return mutated_chromosome



generate_population()
parent,rest = select_chromosomes()
childern = crossover(parent)
MC = mutation(rest[0],.2)

print(rest[0])

print(MC)

