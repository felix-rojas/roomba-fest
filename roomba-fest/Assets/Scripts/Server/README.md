# How to run server

1. Run prereqs.py first to make sure all necessary dependencies are installed. Use an environment preferrably to not change your ptyhon install.
2. Run Server.py. This will start the server and wait to serve.

## SimulationV1

This runs the simulation and imports the necessary packages to do so. It also runs the prereqs.py to check if the necessary packages are installed.

In this file you can change each of the running parameters for the simulation or generate a random grid to run for the simulation.

## Agents & OficinaModel

These are the definitions of agents and model using the mesa package to run the simulation.

## grid.txt

In case you have a custom grid for it to run, you can:
- Substitute the "grid.txt" file with your data
- Change the `file_name` variable to point towards the directory where your custom file is


