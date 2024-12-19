# Sumo_Simulation Case Study

## Summary

The research focused on implementing routing strategies to optimize road traffic system performance in a multiclass traffic assignment context involving Connected Autonomous Vehicles (CAVs) and Human-Driven Vehicles (HDVs). The study employs simulation-based methodologies using SUMO to analyze network performance, where CAVs exhibit routing and driving behaviors approximating System Optimum (SO), while HDVs adhere to User Equilibrium (UE) principles. The primary objective is to minimize overall travel time and enhance network efficiency through iterative-static vehicle rerouting.

Key tools employed include the DuaIterateMix module and the cav-hdvtripsfilegenerator script, adapted from the work of Behzad, B. M., et al. (2023). This approach integrates cutting-edge algorithms and simulation techniques to evaluate and compare the impact of SO and UE routing strategies, providing valuable insights into traffic flow optimization in mixed vehicular environments.

## How to run

- Clone this git repo
- Create a new conda environment with the 'requirements.txt' file `conda create --name <envname> --file requirements.txt`
- Activate your newly created environemnt `conda activate <envname>`
- Define your inputs in In RoutingSimulation/inputs: Current configuration is for the provided network topology (network-topology.png) and temporal and spatial distribution of demand specific for this setup.

  - edges.csv: provides information on the edges of the network (see provided network topology) and their variables.
  - nodes.yml: provides information on the nodes of the network
  - matrix.od files: provides information on the temporal and spatial distribution of vehicles in the network
  - taz.csv: maps the edges in the network to unique traffic assignment zones.

- Execute the `gen_files_script.py` script to generate the edgefile, nodefile, network file, taz file and odtrips file required for further simulation. All generated files are generated in the RoutingSimulation/outputs folder. `python gen_files_script.py`

- Define experiment parameters in RoutingSimulation/Simulation.py
  ```experiment_parameters = {
      'no_iters': 1,  #number of iterations
      'max_conv_dev': 0.01, #maximum convergence deviation
      'conv_iters': 1, #convergence iteration
      'conv_steps': 1, #convergence steps
      'percentage_mix': [100],   #percentage of CAV to run the simulation for: multiple values allowed.
      'apply_marginal_cost': [True],   # application of marginal cost, max of 2 entries, true and false
      'steps': 5000,                    # traci simulation steps to run
      'CAVRePr': [0.8]    #probability of re-routing for the CAVs, multiple values allowed.
  }
  ```
  - Execute simulation `python Simulation.py`. This would do the following:
    - Based on the inputed `percentage_mix` the cav-hdv-filegenerator.py script is used to split the initial odtrips file into `trips.trips.CAV.xml` and `trips.trips.xml` representing the Connected Autonomous Vehicles (CAV) and Human Driven Vehicles (HDV) for that simulation run.
    - The simulation then executes `duaIterateMix.py` from the RoutingSimulation/tools folder, taking the following as inputs
      - network file generated earlier
      - generate CAV and HDV trips files
      - the experiment parameters defined above
      - produces a sumo configuration file, route file, tripsinfo file and other additional files as output.
    - The simulation then runs Traci using these outputed files as input as well as the simulation steps parameter provided in the experiment parameters. Traci executes SUMO or SUMO-GUI and loads the trips and configuration into SUMO.
    - During sumo execution, vehicles entering and exiting the network are logged in a `Simulation.log` file.
    - After the execution, the total travel time, total distance travelled by each vehicle as well as for all vehicles in the network as a total are calculated, and recorded in the Results folder in files `RoutingSimulation/Results/experiment_results.csv` and `RoutingSimulation/Results/vehicle_distances.csv` files for further analysis.
