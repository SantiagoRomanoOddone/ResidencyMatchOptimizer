# ResidencyMatchOptimizer

A Linear Programming Approach to Optimize Medical Residency Placement

## Overview

ResidencyMatchOptimizer is a tool that leverages linear programming to optimize medical residency placement. It uses an optimization model that considers both residency program preferences and applicant rankings to determine the most efficient match. This tool can enhance the satisfaction of residency programs and applicants by ensuring an optimal placement.

## Features

- **Linear Programming-based Matching**: Employs linear programming (LP) to solve the residency matching problem.
- **Customizable Parameters**: Allows customization to adapt to different requirements of residency programs and applicants.
- **Optimal Matching**: Provides an optimal match output based on the objective functions and constraints defined in the model.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/SantiagoRomanoOddonde/ResidencyMatchOptimizer.git
    cd ResidencyMatchOptimizer
    ```

Dependencies include:
- `cplex` - for modeling and solving the linear programming problem.
- `NumPy` - for numerical operations.

## Usage

1. Run the main script :

    ```bash
    python python resident_assignment.py
    ```

2. Check the output, which will include the final match results and additional metrics. For instance:

## Methodology

The model uses linear programming to minimize the "mismatch cost," calculated from the ranking preferences of both applicants and residency programs. The LP objective function and constraints ensure that the placements maximize alignment with preferences and optimize slot utilization.

### Objective Function

The objective function is designed to:
- Minimize total mismatch costs, prioritizing applicants and programs' highest-ranked preferences.

### Constraints

1. **Capacity Constraint**: Ensures that each residency program fills only the slots it has available.
2. **Applicant Constraint**: Ensures that each applicant is matched to at most one residency program.
3. **Ranking Constraint**: Incorporates ranking preferences of both residency programs and applicants.

## Variables & Model Description

The primary variables in the model are as follows:
- `x[i, j]`: Binary decision variable indicating whether applicant `i` is matched to residency program `j`.
- `p[i, j]`: Preference ranking of residency program `j` for applicant `i`.
- `a[i, j]`: Preference ranking of applicant `i` for residency program `j`.

The linear programming model uses these variables to calculate and minimize the overall mismatch cost across all placements.

## Results

The output of the model will include:
- The optimal match between applicants and residency programs.
- Metrics on preference alignment, showing the satisfaction levels for both parties.

Example output:

    ```--------------RESULTADOS CONSOLIDADOS--------------------------
        lp_results_global:  [9878.0, 9888.0, 9942.0, 9855.0, 9906.0, 9849.0, 9846.0, 9915.0, 9960.0, 9841.0]
        lp_count_pref_res:  [477, 478, 477, 474, 475, 481, 479, 482, 478, 475]
        lp_count_pref_hos:  [87, 90, 79, 81, 83, 78, 87, 79, 94, 80]
        lp_count_pref_global:  [64, 68, 56, 55, 58, 59, 66, 61, 72, 55]
        count_res_not_desired_lp_global:  [413, 410, 421, 419, 417, 422, 413, 421, 406, 420]
        desired_position_hos_for_res_lp_global:  [2.03, 2.07, 1.86, 1.97, 1.95, 1.96, 1.91, 1.82, 2.02, 1.96]
        ----------------------------------------
        greedy_results_global [9590.0, 9595.0, 9607.0, 9518.0, 9595.0, 9476.0, 9495.0, 9644.0, 9717.0, 9556.0]
        greedy_count_pref_res:  [473, 474, 472, 474, 466, 472, 464, 473, 466, 470]
        greedy_count_pref_hos:  [93, 87, 79, 78, 85, 78, 93, 81, 101, 82]
        greedy_count_pref_global:  [73, 69, 58, 58, 60, 59, 67, 61, 72, 58]
        count_res_not_desired_greedy_global:  [407, 413, 421, 422, 415, 422, 407, 419, 399, 418]
        desired_position_hos_for_res_greedy_global: [2.36, 2.27, 2.15, 2.19, 2.27, 2.31, 2.38, 2.13, 2.39, 2.27]
        ----------------------------------------
        gap_results:  [0.03, 0.0305, 0.0349, 0.0354, 0.0324, 0.0394, 0.037, 0.0281, 0.025, 0.0298]
        gap_mean:  3.225 %
    ```

If you want to see the problem in detail, you can check the `enunciado.pdf` file.

