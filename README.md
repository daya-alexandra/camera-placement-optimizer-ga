# Camera Placement Optimizer GA

This repository contains my implementation of a genetic algorithm for the camera placement optimization problem on a grid map with obstacles and visibility constraints.

## Goal
Place a fixed number of cameras on a 2D grid map to maximize coverage of important points while reducing overlap and avoiding invalid placements.

## Method
The optimization is performed with a Genetic Algorithm (GA). Each candidate solution represents a set of camera coordinates, and solutions are evaluated using the provided score function.

## Output
The project is intended to produce:
- the final camera placement,
- the optimization score,
- convergence plots,
- and visualization of the resulting map.

## Status
Initial project setup completed. Baseline verification runs successfully.
