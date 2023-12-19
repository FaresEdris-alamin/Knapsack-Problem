import random

pop_size = 8
unbounded = False
items =[(1,10),(2,15),(3,18),(4,20),(5,25)]
max_weight = 50
population =[]
generations = 100
mutation_probability = 0.02

def generate_population():     # Unbounded should choose any chromosome any number of times                # Currently it chooses it only twice and no more than that in all attempts
    count = 0        #used in the while to count the number of chromosome in the population
        #for _ in range(population_size):
    while count < pop_size:   
            #creating the chromosome 
        genes = [0, 1] if not unbounded else [i for i in range(10)]
            #genes = [0, 1] if not unbounded else [0, 1, 2, 3, 4, 5]  
        chromosome = [random.choice(genes) for _ in range(len(items))]
            
            #check if it's weight is above the max weight if it isn't it adds the chromosome to the population 
        total_weight = sum(item[0] * chromosome[i] for i, item in enumerate(items))
        if total_weight <= max_weight:
            population.append(chromosome)
            count+=1
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
            print(parents)
            #raise ValueError("At least two parents are required for crossover.")

        # Perform crossover between all pairs of parents
        children = []
        for i in range(0, len(parents), 2):
            parent1, parent2 = parents[i], parents[i + 1] if i + 1 < len(parents) else parents[i]
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]

            child1 = correct_weight(child1)
            child2 = correct_weight(child2)
            children.extend([child1, child2])
        return children

def correct_weight(chromosome):
        total_weight = sum(item[0] * chromosome[i] for i, item in enumerate(items))
        while total_weight > max_weight:
            # Randomly select an item and set its corresponding gene to 0
            index_to_reset = random.randint(0, len(chromosome) - 1)
            chromosome[index_to_reset] = 0
            total_weight = sum(item[0] * chromosome[i] for i, item in enumerate(items))
        return chromosome


def mutate(chromosome):
        mutate_point = random.randint(0, len(items) - 1)
        chromosome[mutate_point] = random.choice([i for i in range(10)])
        chromosome = correct_weight(chromosome)
        return chromosome

def mutation(chromo, p):
    # mutated chromo intial values are zeros
        mutated_chromosome = [0 for _ in range(len(items))]
        for i in range(len(items)):
            d = chromo[i]
            r = random.uniform(0, 1)
            if chromo[i] == 1.0 and r < p:
                mutated_chromosome[i] = 0
            elif chromo[i] == 0.0 and r < p:
                mutated_chromosome[i] = 1
            else:
                mutated_chromosome[i] = d
        chromo = mutated_chromosome
        return chromo

def evolve_population(population):
            for _ in range(generations):
                parents, second_half = select_chromosomes()
                children = crossover(parents)
                
                # Replace the worst-performing individuals with the children
                
                population = parents +second_half[:int(0.6 * len(second_half))] + children
                
                # Mutate some individuals based on the mutation probability
                
                for i in range(len(population)):
                    if unbounded:
                        if random.random() < mutation_probability:
                            population[i] = mutate(population[i]) # Mutates unbounded
                    else:
                        population[i] = mutation(population[i], mutation_probability) # Mutates 0-1
            return population

def get_best_solution():
        best_chromosome = max(population, key=calculate_fitness)
        total_weight = sum(item[0] * best_chromosome[i] for i, item in enumerate(items))
        total_value = sum(item[1] * best_chromosome[i] for i, item in enumerate(items))
        return best_chromosome, total_weight, total_value


generations =  2
generate_population()
parents,rest = select_chromosomes()
children = crossover(parents)
evolve_population(population)




