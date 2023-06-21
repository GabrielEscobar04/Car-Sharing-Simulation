# Car Sharing Simulation

This project aims to create a simulation environment for emulating a car-sharing system in the Eixample district of Barcelona. The program takes two inputs: a randomly generated list of clients distributed throughout the day, with varying weights for each hour to reflect realistic demand patterns, and the number of cars for the simulation. The simulation considers different scenarios by adjusting the number of cars available.

The main objective of the code is to showcase the benefits of implementing a car-sharing system. By running the simulation, the code is intended to demonstrate that car sharing can effectively reduce the total number of cars needed to meet transportation demands. This reduction in the number of cars is achieved while maintaining a minimal increase in travel time for each client. 

## Prerequisites

Python: Python is an interpreted high-level general-purpose programming language. It was created by Guido van Rossum and first released in 1991. Python's design philosophy emphasizes code readability with its notable use of significant whitespace. Its language constructs and object-oriented approach aim to help programmers write logical and clear code for both small and large-scale projects. More information about Python can be found at https://www.python.org/.

**Libraries Used**

The following libraries are utilized in this project:

- csv: This library provides functionality for reading and writing CSV files, which is used to handle the input data for the simulation.
matplotlib: This library is used for creating visualizations and plots, which may be utilized to analyze the results of the car-sharing simulation.
- NetworkX: This library is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks. It may be used in this project to model and analyze the network of clients and their travel routes.

## Usage 

To use this program, follow these steps:

- Ensure that Python is installed on your system. You can download it from https://www.python.org/.
- Clone or download the project repository from GitHub: https://github.com/username/project.
- Install the required libraries by running the following command:
```
pip install -r requirements.txt
```
- Run the simulation program by executing the main script:
```
python simulation.py
```

Please refer to the documentation and code in the repository for further details on the program's functionality and customization options.

## Credits

This project was developed by Gabriel Escobar and submitted as its baccalaureate thesis.