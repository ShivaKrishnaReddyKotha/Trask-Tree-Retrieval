# Task Tree Retrieval from Cooking Recipes for Robotic Cooking
### Project Overview
This project focuses on developing search algorithms for Functional Object-Oriented Networks (FOON) to enable robotic cooking automation. The goal is to generate an optimal sequence of actions for a robot to successfully prepare a given recipe using available ingredients, utensils, and functional units in a kitchen environment.

### Two search algorithms were implemented:

Iterative Deepening Search (IDS)
Greedy Best-First Search (GBFS) with two heuristic functions
The performance of these algorithms was evaluated in generating task trees for different recipes.

### Methodology
FOON Creation: A structured network representing relationships between objects, motions, and functional units.
Task Tree Generation: Implementing search algorithms to determine the most efficient action sequence.
Search Algorithms:
Iterative Deepening Search (IDS): A systematic depth-first approach that gradually increases search depth.
Greedy Best-First Search (GBFS):
Heuristic 1 (h1): Prioritizes paths based on motion success rates.
Heuristic 2 (h2): Prioritizes paths requiring fewer input objects.
Performance Evaluation: Comparing task tree sizes and computational efficiency.

### Key Results
Goal Node	IDS	GBFS (h1)	GBFS (h2)
Whipped Cream	16	16	15
Greek Salad	37	41	41
Macaroni	9	12	9
Sweet Potato	3	3	3
Ice	1	1	1
IDS produced more comprehensive task trees.
GBFS with h2 was more efficient in some cases.
GBFS with h1 resulted in larger task trees in complex recipes.

### Technologies Used
Python for implementation
Graph Data Structures for FOON representation
Search Algorithms (IDS, GBFS)
Data Visualization for task tree representation

### Future Work
Improve heuristic functions for better efficiency.
Explore hybrid search approaches.
Implement real-world robotic cooking applications.


