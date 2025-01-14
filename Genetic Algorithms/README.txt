
# Genetic Algorithm for Optimizing Distance Functions in Clustering

This project implements a genetic algorithm to optimize a custom distance function used in hierarchical clustering. The algorithm aims to maximize the V-measure score, a metric that evaluates the quality of clustering based on ground truth labels.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [How It Works](#how-it-works)
- [Parameters](#parameters)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Custom Distance Function**: A distance function with tunable weights is optimized using genetic algorithms.
- **Hierarchical Clustering**: Uses Agglomerative Clustering with a precomputed distance matrix.
- **Fitness Evaluation**: Measures clustering performance using the V-measure score.
- **Genetic Operations**:
  - Mutation: Randomly alters weights of the distance function.
  - Crossover: Combines weights from two parent distance functions.
  - Elitism: Retains the best individual in each generation.
- **Cross-validation**: Performs k-fold cross-validation to validate the model.
- **Configurable Parameters**: Allows users to modify population size, mutation rate, crossover rate, and other hyperparameters.

---

## Requirements

The following Python libraries are required:

- `numpy`
- `pandas`
- `scikit-learn`
- `os`
- `time`

You can install the required libraries using pip:

```bash
pip install numpy pandas scikit-learn
```

---

## Usage

1. **Prepare Data**:
   - Place your training and test datasets (`breast_cancer_coimbra_train.csv` and `breast_cancer_coimbra_test.csv`) in the project directory.

2. **Run the Code**:
   Execute the script using:
   ```bash
   python your_script_name.py
   ```

3. **Output**:
   - Results for each generation are saved to `results.csv` in the project directory.
   - Key metrics include max, min, and average fitness scores, and the equations for the best, worst, and average individuals in each generation.

---

## Code Overview

### **1. DistanceFunction**
A class representing a custom distance function used in clustering.

- **Key Methods**:
  - `calculate_distance`: Computes the weighted distance between two samples.
  - `generate_distance_matrix`: Creates a distance matrix for a dataset.
  - `mutate`: Introduces random changes to the weights.
  - `crossover`: Combines weights of two DistanceFunction objects.
  - `equation`: Returns a string representation of the distance function.

### **2. GeneticAlgorithm**
A class implementing the genetic algorithm.

- **Key Methods**:
  - `evaluate_fitness`: Calculates the V-measure score for an individual's clustering performance.
  - `tournament_selection`: Selects individuals for crossover based on fitness.
  - `run_generation`: Evolves the population for one generation.
  - `run`: Runs the genetic algorithm for a specified number of generations.

### **3. Cross-validation and Execution**
- **`cross_validate_and_run`**:
  - Loads the dataset.
  - Splits the data into training and test sets using k-fold cross-validation.
  - Runs the genetic algorithm for each fold and saves results.

---

## How It Works

1. **Initialization**:
   - A population of random `DistanceFunction` objects is created.

2. **Evaluation**:
   - Each individual is evaluated on its ability to cluster the training data.

3. **Selection**:
   - Tournament selection identifies the most fit individuals for reproduction.

4. **Reproduction**:
   - Crossover and mutation generate new individuals for the next generation.

5. **Iteration**:
   - The process repeats for a specified number of generations.

6. **Cross-validation**:
   - The algorithm is validated using multiple data splits to ensure robustness.

---

## Parameters

The following parameters can be configured:

- `population_size`: Number of individuals in the population.
- `num_generations`: Number of generations for evolution.
- `mutation_rate`: Probability of mutating an individual.
- `crossover_rate`: Probability of performing crossover.
- `tournament_size`: Number of individuals in the tournament selection.
- `k_folds`: Number of folds for cross-validation.

Example configuration:
```python
seeds = list(range(1, 11))
populations = [30, 50, 100]
generations = [30, 50, 100]
mutation_rates = [0.05, 0.1]
crossover_rates = [0.6, 0.9]
tournament_sizes = [2, 5]
```

---

## Results

- **Output File**: `results.csv`
  - Columns include:
    - `generation`: Generation number.
    - `max_fitness_train`: Maximum fitness score on the training set.
    - `min_fitness_train`: Minimum fitness score on the training set.
    - `avg_fitness_train`: Average fitness score on the training set.
    - `max_fitness_test`: Maximum fitness score on the test set.
    - `time_elapsed`: Time taken to complete the generation.
    - `best_individual`: Best distance function equation for the generation.

- **Visualization**:
  - Results can be visualized using external tools like Excel or Python plotting libraries.

---

## Contributing

Contributions are welcome! Feel free to submit pull requests or report issues.

### To Do:
- Add support for additional clustering algorithms.
- Implement advanced mutation and crossover strategies.
- Add data preprocessing utilities.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
