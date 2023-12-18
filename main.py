import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import random

class GeneticKnapsackSolver:
    def __init__(self, weights, values, max_weight, population_size, mutation_probability, generations, unbounded=False):
        self.items = list(zip(weights, values))
        self.max_weight = max_weight
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.generations = generations
        self.unbounded = unbounded
        self.population = self.generate_population()

    def generate_population(self):     # Unbounded should choose any chromosome any number of times 
        population = []                # Currently it chooses it only twice and no more than that in all attempts
        for _ in range(self.population_size):
            genes = [0, 1] if not self.unbounded else [0, 1, 2]  # Add 2 for unbounded knapsack
            chromosome = [random.choice(genes) for _ in range(len(self.items))]
            population.append(chromosome)
        return population

    def calculate_fitness(self, chromosome):
        total_weight = sum(item[0] * chromosome[i] for i, item in enumerate(self.items))
        total_value = sum(item[1] * chromosome[i] for i, item in enumerate(self.items))
        return total_value if total_weight <= self.max_weight or not self.unbounded else 0

    def select_chromosomes(self):
        fitness_values = [self.calculate_fitness(chromosome) for chromosome in self.population]
        fitness_values = [float(i) / sum(fitness_values) for i in fitness_values]

        #choose 20% of the population as parents
        sorted_population = [x for _, x in sorted(zip(fitness_values, self.population), reverse=True)]
        parents = sorted_population[:int(0.2 * len(self.population))]

        return parents

    def crossover(self, parents):
        crossover_point = random.randint(0, len(self.items) - 1)

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


    def mutate(self, chromosome):
        mutate_point = random.randint(0, len(self.items) - 1)
        chromosome[mutate_point] = random.choice([0, 1, 2]) if self.unbounded else 1
        return chromosome

    def evolve_population(self):
        for _ in range(self.generations):
            parents = self.select_chromosomes()
            children = self.crossover(parents)

           # second_half = parents[]

    def get_best_solution(self):
        best_chromosome = max(self.population, key=self.calculate_fitness)
        total_weight = sum(item[0] * best_chromosome[i] for i, item in enumerate(self.items))
        total_value = sum(item[1] * best_chromosome[i] for i, item in enumerate(self.items))
        return best_chromosome, total_weight, total_value

class KnapsackSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Solver")

        self.font_style = ('Helvetica', 12)  # Adjust font size and style here

        self.weights_label = ttk.Label(root, text="Weights(separated by , ):", font=self.font_style)
        self.weights_entry = ttk.Entry(root, font=self.font_style)
        self.weights_label.grid(row=0, column=0, sticky=tk.W)
        self.weights_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W + tk.E)

        self.values_label = ttk.Label(root, text="Values(separated by , ):", font=self.font_style)
        self.values_entry = ttk.Entry(root, font=self.font_style)
        self.values_label.grid(row=1, column=0, sticky=tk.W)
        self.values_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W + tk.E)

        self.max_weight_label = ttk.Label(root, text="Max Weight:", font=self.font_style)
        self.max_weight_entry = ttk.Entry(root, font=self.font_style)
        self.max_weight_label.grid(row=2, column=0, sticky=tk.W)
        self.max_weight_entry.grid(row=2, column=1, columnspan=3, sticky=tk.W + tk.E)

        self.population_label = ttk.Label(root, text="Population Size:", font=self.font_style)
        self.population_entry = ttk.Entry(root, font=self.font_style)
        self.population_label.grid(row=3, column=0, sticky=tk.W)
        self.population_entry.grid(row=3, column=1, columnspan=3, sticky=tk.W + tk.E)

        self.mutation_label = ttk.Label(root, text="Mutation Probability:", font=self.font_style)
        self.mutation_entry = ttk.Entry(root, font=self.font_style)
        self.mutation_label.grid(row=4, column=0, sticky=tk.W)
        self.mutation_entry.grid(row=4, column=1, columnspan=3, sticky=tk.W + tk.E)

        self.generations_label = ttk.Label(root, text="Generations:", font=self.font_style)
        self.generations_entry = ttk.Entry(root, font=self.font_style)
        self.generations_label.grid(row=5, column=0, sticky=tk.W)
        self.generations_entry.grid(row=5, column=1, columnspan=3, sticky=tk.W + tk.E)

        # Add a dropdown menu for knapsack type
        self.knapsack_type_label = ttk.Label(root, text="Knapsack Type:", font=self.font_style)
        self.knapsack_type_combobox = ttk.Combobox(root, values=["0-1 Knapsack", "Unbounded Knapsack"], font=self.font_style)
        self.knapsack_type_label.grid(row=6, column=0, sticky=tk.W)
        self.knapsack_type_combobox.grid(row=6, column=1, columnspan=3, sticky=tk.W + tk.E)

        self.solve_button = ttk.Button(root, text="Solve", command=self.solve_knapsack, style='TButton', cursor='hand2')
        self.solve_button.grid(row=7, column=0, columnspan=4, pady=10)

    def solve_knapsack(self):
        try:
            weights_str = self.weights_entry.get()
            values_str = self.values_entry.get()

            weights = [int(weight) for weight in weights_str.split(',')]
            values = [int(value) for value in values_str.split(',')]

            max_weight = int(self.max_weight_entry.get())
            population_size = int(self.population_entry.get())
            mutation_probability = float(self.mutation_entry.get())
            generations = int(self.generations_entry.get())

            knapsack_type = self.knapsack_type_combobox.get()
            unbounded = knapsack_type == "Unbounded Knapsack"

            solver = GeneticKnapsackSolver(weights, values, max_weight, population_size, mutation_probability, generations, unbounded)
            solver.evolve_population()
            best_chromosome, total_weight, total_value = solver.get_best_solution()

            result_str = f"The best solution:\nChromosome: {best_chromosome}\nWeight: {total_weight}\nValue: {total_value}"
            messagebox.showinfo("Knapsack Solver Result", result_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numerical values.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackSolverGUI(root)
    root.mainloop()
