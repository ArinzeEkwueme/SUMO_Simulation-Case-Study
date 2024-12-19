from pathlib import Path
import ast
import csv

from Strategy import TraciRunner, UE_SO_Strategy

networkfile = "outputs/sumoproject.net.xml"
# edgefile = "outputs/sumoproject.edg.xml"
# nodefile = "outputs/sumoproject.nod.xml"
tripsfile = "outputs/sumoproject.odtrips.xml"
#routesfile = "outputs/sumoproject.rou.xml"
#engine_path = "/usr/local/Cellar/sumo/1.20.0/share/sumo/tools/assign" # Apply yours here 
engine_path = Path("tools") 

def checkFiles(): 
    print("Checking for network and trips file...")
    netfile = Path(networkfile)
    tripfile = Path(tripsfile)
    # file3 = Path(edgefile)
    # file4 = Path(nodefile)
    if not netfile.exists() or not tripfile.exists():
        raise FileNotFoundError("Please run gen_files_script.py first")
    else: 
        print("Required files exist. Proceeding ..")


def get_last_cfg_from_log(): 
    matching_lines = []
    with open('dua.log', 'r') as file:
        for line in file:
            if ".sumocfg" in line:
                matching_lines.append(line.strip())
    if len(matching_lines) > 1:
        last_execution = matching_lines[-1]
    else: 
        last_execution = matching_lines[0]
    command = ast.literal_eval(last_execution)
    return command[-1]


def run_ue_so_duaiterate_mix(no_iters,max_conv_dev,conv_iters,conv_steps, percentage_mix, CAVRePr, apply_marginal_cost=False ):
    try:
        print(f"Running Strategy with duaIterateMix engine, percent_mix = {percentage_mix}, CAVRePr = {CAVRePr} and apply_marginal_cost = {apply_marginal_cost}")
        simulation_strategy = UE_SO_Strategy( engine_path = engine_path,
                                    networkfile = networkfile , 
                                    tripsFile = tripsfile,
                                    no_iters = no_iters,
                                    max_conv_dev = max_conv_dev,
                                    conv_iters = conv_iters,
                                    conv_steps = conv_steps,
                                    )
        simulation_strategy.duaiterate_mix(percentage_mix, CAVRePr, apply_marginal_cost)
    except Exception as e: 
        raise e 
    
    configFilePath = get_last_cfg_from_log()
    return configFilePath

def run_traci(sumo_cfg_file, steps=10000):
    traci_runner = TraciRunner(
            simulationsteps=steps, 
            projectcfgfile = sumo_cfg_file
        )
    total_travel_time, total_distance = traci_runner.run(gui=True)
    
    print(f"\nTotal Travel Time recorded : {total_travel_time} \n\n")
    print(f"\nTotal Travel Distance recorded : {total_distance} \n\n")
    return total_travel_time, total_distance

# Define experiment parameters
experiment_parameters = {
    'no_iters': 10,
    'max_conv_dev': 0.01,
    'conv_iters': 5,
    'conv_steps': 10,
    'percentage_mix': [0],  
    'apply_marginal_cost': [False],        
    'steps': 60000,                    # Only for 'run_traci'        # Only for 'run_traci' Not used any more 
    'CAVRePr': [1.0]
}

# Experiment runner function
def experiment_runner():
    no_iters = experiment_parameters['no_iters'];
    max_conv_dev = experiment_parameters['max_conv_dev'];
    conv_iters = experiment_parameters['conv_iters'];
    conv_steps = experiment_parameters['conv_steps'];
    # Open CSV file for writing results
    with open('Results/experiment_results.csv', mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header row for CSV
        csv_writer.writerow([
            'no_iters', 'max_conv_dev', 'conv_iters', 'conv_steps', 'percentage_mix', 'CAVRePr','marginal_cost_applied','total_travel_time','total_distance_travelled'
        ])

        # Run 
        for apply_marginal_cost in experiment_parameters['apply_marginal_cost']:
            for CAVRePr in experiment_parameters['CAVRePr']:
                for percentage_mix in experiment_parameters['percentage_mix']:
                    cfg_file = run_ue_so_duaiterate_mix(no_iters, max_conv_dev, conv_iters, conv_steps, percentage_mix, CAVRePr,apply_marginal_cost)
                    print(f"Running Sumo with the last config: {cfg_file}")
                    travel_time, dist_travelled = run_traci(sumo_cfg_file=cfg_file, steps=experiment_parameters['steps'])
                    
                    csv_writer.writerow([no_iters, max_conv_dev, conv_iters, conv_steps, percentage_mix, CAVRePr, apply_marginal_cost, travel_time,dist_travelled])

    print("Experiment completed. Results saved to 'experiment_results.csv'")


if __name__ == "__main__":
    def start():
        try:
            checkFiles()
            #configFilePath = run_ue_so_duaiterate_mix(no_iters=1, max_conv_dev=0.01,conv_iters=1,conv_steps=1,percentage_mix=10,CAVRePr=0.2,apply_marginal_cost=False)
            experiment_runner()
        except Exception as e: 
            print(e)
            raise e
        #print(f"Run Sumo with the last config: {configFilePath}")
        #run_traci(steps=10000,sumo_cfg_file=configFilePath)
    start()