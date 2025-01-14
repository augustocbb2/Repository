import pandas as pd
import numpy as np
import random
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import v_measure_score
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import KFold
import time
import os

class DistanceFunction:
    """
    A class to define a custom distance function with evolutionary capabilities.

    Attributes:
        weights (numpy.ndarray): Array of weights used for distance calculation.
        max_size (int): Maximum number of features to consider for distance calculation.
    """

    def __init__(self, weights=None, max_size=7):
        """
        Initializes the DistanceFunction object.

        Args:
            weights (list or numpy.ndarray, optional): Weights for the distance calculation. Defaults to random weights.
            max_size (int): Maximum size of the weights array. Defaults to 7.
        """
        self.max_size = max_size
        self.weights = np.random.rand(max_size) if weights is None else np.array(weights[:max_size])

    def calculate_distance(self, sample1, sample2):
        """
        Calculates the weighted distance between two samples.

        Args:
            sample1 (numpy.ndarray): First sample.
            sample2 (numpy.ndarray): Second sample.

        Returns:
            float: Weighted distance between the two samples.
        """
        return np.sum(self.weights * np.abs(sample1[:len(self.weights)] - sample2[:len(self.weights)]))

    def generate_distance_matrix(self, data):
        """
        Generates a pairwise distance matrix for a dataset.

        Args:
            data (numpy.ndarray): Dataset for which to calculate the distance matrix.

        Returns:
            numpy.ndarray: Pairwise distance matrix.
        """
        num_samples = data.shape[0]
        distance_matrix = np.zeros((num_samples, num_samples))
        
        for i in range(num_samples):
            for j in range(i + 1, num_samples):
                distance_matrix[i, j] = distance_matrix[j, i] = self.calculate_distance(data[i], data[j])
                
        return distance_matrix

    def mutate(self, mutation_rate):
        """
        Mutates the weights of the distance function based on a mutation rate.

        Args:
            mutation_rate (float): Probability of mutating a weight.
        """
        if np.random.rand() < mutation_rate:
            mutation_index = np.random.randint(len(self.weights))
            self.weights[mutation_index] += np.random.normal(0, 0.1)

    def crossover(self, other):
        """
        Performs crossover with another DistanceFunction object to create a new one.

        Args:
            other (DistanceFunction): Another DistanceFunction object.

        Returns:
            DistanceFunction: A new DistanceFunction with combined weights.
        """
        child_weights = (self.weights + other.weights) / 2
        return DistanceFunction(weights=child_weights[:self.max_size])

    def equation(self):
        """
        Returns a string representation of the weighted distance function.

        Returns:
            str: Equation of the weighted distance function.
        """
        return " + ".join([f"{w:.2f}*x{i}" for i, w in enumerate(self.weights)])


class GeneticAlgorithm:
    """
    A class to implement a Genetic Algorithm for optimizing the DistanceFunction.

    Attributes:
        population (list): List of DistanceFunction objects.
        num_generations (int): Number of generations to run the algorithm.
        mutation_rate (float): Probability of mutation for individuals.
        crossover_rate (float): Probability of crossover between individuals.
        tournament_size (int): Number of individuals participating in the tournament selection.
        elitism (bool): Whether to retain the best individual from the previous generation.
    """

    def __init__(self, population_size, num_generations, mutation_rate, crossover_rate, tournament_size, elitism):
        """
        Initializes the GeneticAlgorithm object.

        Args:
            population_size (int): Size of the population.
            num_generations (int): Number of generations to evolve.
            mutation_rate (float): Mutation rate for individuals.
            crossover_rate (float): Crossover rate between individuals.
            tournament_size (int): Number of individuals in tournament selection.
            elitism (bool): Whether to retain the best individual from the previous generation.
        """
        self.population = [DistanceFunction() for _ in range(population_size)]
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def evaluate_fitness(self, individual, data, labels):
        """
        Evaluates the fitness of an individual.

        Args:
            individual (DistanceFunction): Individual to evaluate.
            data (numpy.ndarray): Dataset for clustering.
            labels (numpy.ndarray): Ground truth labels for the dataset.

        Returns:
            float: V-measure score of the clustering.
        """
        distance_matrix = individual.generate_distance_matrix(data)
        clustering = AgglomerativeClustering(n_clusters=len(np.unique(labels)), metric="precomputed", linkage="average")
        predicted_labels = clustering.fit_predict(distance_matrix)
        return v_measure_score(labels, predicted_labels)

    def tournament_selection(self):
        """
        Selects an individual using tournament selection.

        Returns:
            DistanceFunction: Selected individual.
        """
        selected = random.sample(self.population, self.tournament_size)
        fitness_scores = [self.evaluate_fitness(ind, X_train, y_train) for ind in selected]
        return selected[np.argmax(fitness_scores)]

    def run_generation(self, data, labels):
        """
        Evolves the population for one generation.

        Args:
            data (numpy.ndarray): Dataset for clustering.
            labels (numpy.ndarray): Ground truth labels for the dataset.

        Returns:
            tuple: Statistics of the generation (max, min, avg fitness, equations of best, worst, and avg individuals).
        """
        fitness_scores = [self.evaluate_fitness(ind, data, labels) for ind in self.population]
        max_fitness = max(fitness_scores)
        min_fitness = min(fitness_scores)
        avg_fitness = np.mean(fitness_scores)
        
        best_individual = self.population[np.argmax(fitness_scores)]
        worst_individual = self.population[np.argmin(fitness_scores)]
        avg_individual = self.population[np.argsort(fitness_scores)[len(fitness_scores) // 2]]

        new_population = [best_individual] if self.elitism else []

        while len(new_population) < len(self.population):
            if np.random.rand() < self.crossover_rate:
                parent1, parent2 = self.tournament_selection(), self.tournament_selection()
                child = parent1.crossover(parent2)
            else:
                child = self.tournament_selection()
            child.mutate(self.mutation_rate)
            new_population.append(child)

        self.population = new_population
        return (max_fitness, min_fitness, avg_fitness, 
                best_individual.equation(), worst_individual.equation(), avg_individual.equation())

    def run(self, data, labels):
        """
        Runs the genetic algorithm for the specified number of generations.

        Args:
            data (numpy.ndarray): Dataset for clustering.
            labels (numpy.ndarray): Ground truth labels for the dataset.

        Returns:
            list: Results for each generation.
        """
        results = []
        for generation in range(self.num_generations):
            max_fitness, min_fitness, avg_fitness, best_eq, worst_eq, avg_eq = self.run_generation(data, labels)
            results.append((generation, max_fitness, min_fitness, avg_fitness, best_eq, worst_eq, avg_eq))
        return results

def cross_validate_and_run(seeds, populations, generations, mutation_rates, crossover_rates, tournament_sizes, k_folds=10):
    # Load and preprocess data
    data = pd.read_csv('breast_cancer_coimbra_train.csv')
    X = MinMaxScaler().fit_transform(data.iloc[:, :-1].values)
    y = LabelEncoder().fit_transform(data.iloc[:, -1].values)

    results_file = "results.csv"
    columns = ["seed", "population_size", "num_generations", "mutation_rate", "crossover_rate", 
               "tournament_size", "generation", "max_fitness_train", "min_fitness_train", 
               "avg_fitness_train", "max_fitness_test", "min_fitness_test", 
               "avg_fitness_test", "time_elapsed", "best_individual", 
               "worst_individual", "avg_individual"]

    if not os.path.isfile(results_file):
        pd.DataFrame(columns=columns).to_csv(results_file, index=False)

    for seed in seeds:
        random.seed(seed)
        np.random.seed(seed)

        for population_size in populations:
            for num_generations in generations:
                for mutation_rate in mutation_rates:
                    for crossover_rate in crossover_rates:
                        for tournament_size in tournament_sizes:
                            kf = KFold(n_splits=k_folds, shuffle=True, random_state=seed)
                            for fold, (train_index, test_index) in enumerate(kf.split(X)):
                                X_train, y_train = X[train_index], y[train_index]
                                X_test, y_test = X[test_index], y[test_index]

                                ga = GeneticAlgorithm(population_size=population_size, num_generations=num_generations,
                                                      mutation_rate=mutation_rate, crossover_rate=crossover_rate, 
                                                      tournament_size=tournament_size, elitism=True)
                                
                                start_time = time.time()
                                generation_results = ga.run(X_train, y_train)
                                elapsed_time = time.time() - start_time

                                for generation, max_fit_train, min_fit_train, avg_fit_train, best_eq, worst_eq, avg_eq in generation_results:
                                    max_fit_test = ga.evaluate_fitness(ga.population[0], X_test, y_test)
                                    min_fit_test = max_fit_test
                                    avg_fit_test = max_fit_test

                                    result_row = {
                                        "seed": seed, "population_size": population_size, "num_generations": num_generations,
                                        "mutation_rate": mutation_rate, "crossover_rate": crossover_rate,
                                        "tournament_size": tournament_size, "generation": generation,
                                        "max_fitness_train": max_fit_train, "min_fitness_train": min_fit_train,
                                        "avg_fitness_train": avg_fit_train, "max_fitness_test": max_fit_test,
                                        "min_fitness_test": min_fit_test, "avg_fitness_test": avg_fit_test,
                                        "time_elapsed": elapsed_time, "best_individual": best_eq, 
                                        "worst_individual": worst_eq, "avg_individual": avg_eq
                                    }
                                    pd.DataFrame([result_row]).to_csv(results_file, mode="a", header=False, index=False)
                                    print(f"Saved generation {generation} results for population {population_size}, "
                                          f"generations {num_generations}, mutation rate {mutation_rate}, "
                                          f"crossover rate {crossover_rate}, tournament size {tournament_size}")
# Load training and test data
train_data = pd.read_csv('breast_cancer_coimbra_train.csv')
test_data = pd.read_csv('breast_cancer_coimbra_test.csv')
X_train = train_data.iloc[:, :-1].values
print(X_train)
y_train = train_data.iloc[:, -1].values

X_test = test_data.iloc[:, :-1].values
y_test = test_data.iloc[:, -1].values
# Normalize the features to the range [0, 1]
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert the categorical variable y_train and y_test to numerical values

label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
y_test = label_encoder.transform(y_test)
# Parameters for testing
seeds = list(range(1, 11))
populations = [30, 50, 100, 500]
generations = [30, 50, 100, 500]
mutation_rates = [0.05, 0.3]
crossover_rates = [0.9, 0.6]
tournament_sizes = [2, 5]

if __name__ == "__main__":
    cross_validate_and_run(seeds, populations, generations, mutation_rates, crossover_rates, tournament_sizes, k_folds=10)
