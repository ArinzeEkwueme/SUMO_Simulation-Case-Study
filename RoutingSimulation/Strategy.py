from abc import abstractmethod
import subprocess
import traci
from Object_Oriented_Classes.network_components import Loader
from Object_Oriented_Classes.network_components import Network
import logging
import csv
from pathlib import Path
import re
import os
import xml.etree.ElementTree as ET

class UE_SO_Strategy:
    def __init__(self, engine_path, networkfile, tripsFile, no_iters, max_conv_dev,conv_iters,conv_steps):
        #Assert that files have been generated! 
        self.engine_path = Path(engine_path)
        self.networkfile = networkfile
        self.tripsFile = tripsFile
        self.no_iters = no_iters
        self.max_conv_dev = max_conv_dev
        self.conv_iters = conv_iters
        self.conv_steps =  conv_steps
        self.rFile = 'outputs/trips.trips.CAV.xml'
        self.tFile = 'outputs/trips.trips.xml'
    
    def split_trips_file(self, percentage=50, CAVRePr=0.1): 
        command = f"python generators/cav-hdv-filegenerator.py -P {percentage} -CAVRePr {CAVRePr}".split(" ")
        subprocess.run(command)
    
    def duaiterate_mix(self, percentageMix,CAVRePr, apply_marginal_cost=False):
        try:
            self.split_trips_file(percentageMix,CAVRePr)
        except Exception as e:
            print(f"Spliting failed with {e}")
            print("No need to proceed futher: Terminated early.")
            return 
            
        tool = self.engine_path/"duaIterateMix.py"
        if apply_marginal_cost: 
            command = f"python {tool} -n {self.networkfile} -t {self.tFile} -r {self.rFile} -l {self.no_iters} --max-convergence-deviation {self.max_conv_dev} --convergence-iterations {self.conv_iters} --mix --convergence-steps {self.conv_steps} --marginal-cost --marginal-cost.exp 1.0 --logit".split(" ")
        else:
            command = f"python {tool} -n {self.networkfile} -t {self.tFile} -r {self.rFile} -l {self.no_iters} --max-convergence-deviation {self.max_conv_dev} --convergence-iterations {self.conv_iters} --mix --convergence-steps {self.conv_steps}".split(" ")

        subprocess.run(command)

class TraciRunner: 
    def __init__(self,simulationsteps, projectcfgfile):
        self.route_changed = False 
        self.projectcfgfilename = projectcfgfile
        self.processed_vehicles = []
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='simulation.log', level=logging.DEBUG, filemode="w+")
        self.departed_vehicles =[]
        self.arrived_vehicles = []
        self.simulationsteps = simulationsteps
        self.sys_optimum_rerouted_vehicles = []
        self.vehicle_distances = {}

    def log_vehicle_on_entry(self, step, stop_range):
        if step >= stop_range: 
            return
        vehicles_in_simulation = traci.simulation.getDepartedIDList()
        if vehicles_in_simulation:
            for vehicle_id in vehicles_in_simulation:
                if vehicle_id not in self.departed_vehicles:
                    self.departed_vehicles.append(vehicle_id)
                self.logger.info(f"Vehicle {vehicle_id} has entered the network at step {step}.")

    def log_vehicle_on_exit(self, step, stop_range): 
        if step >= stop_range: 
            return
        vehicles_arrived = traci.simulation.getArrivedIDList()
        if vehicles_arrived:
            for vehicle_id in vehicles_arrived:
                distance_travelled = 0;
                if vehicle_id not in self.arrived_vehicles:
                    self.arrived_vehicles.append(vehicle_id)

                self.logger.info(f"Vehicle {vehicle_id} has left the network at step {step}.")
    
    def calculate_total_travel_time(self):
        # Dictionary to store entry and exit times for each vehicle
        vehicle_times = {}
        log_filename = 'simulation.log'

        # Regular expressions to match entry and exit log lines
        entry_pattern = re.compile(r'Strategy:Vehicle (\d+) has entered the network at step (\d+)\.')
        exit_pattern = re.compile(r'Strategy:Vehicle (\d+) has left the network at step (\d+)\.')

        # Read the log file line by line
        with open(log_filename, 'r') as log_file:
            for line in log_file:
                # Check for vehicle entry
                entry_match = entry_pattern.search(line)
                if entry_match:
                    vehicle_id = entry_match.group(1)
                    entry_time = int(entry_match.group(2))
                    #print("Entry Time: ", entry_time)
                    # Store entry time for the vehicle
                    vehicle_times[vehicle_id] = {'entry': entry_time, 'exit': None}
                
                # Check for vehicle exit
                exit_match = exit_pattern.search(line)
                if exit_match:
                    vehicle_id = exit_match.group(1)
                    exit_time = int(exit_match.group(2))
                    #print("Exit time : ", exit_time)
                    # Update exit time for the vehicle
                    if vehicle_id in vehicle_times:
                        vehicle_times[vehicle_id]['exit'] = exit_time

        # Calculate total travel time for all vehicles
        travel_times = []
        total_travel_time = 0
        for vehicle_id, times in vehicle_times.items():
            if times['entry'] is not None and times['exit'] is not None:
                travel_time = times['exit'] - times['entry']
            travel_times.append(travel_time)
            self.logger.info(f"Travel time for Vehicle {vehicle_id} is {travel_time} steps.")
        total_travel_time = sum(travel_times)
        self.logger.info(f"Total travel time for all vehicles: {total_travel_time} steps.")
        return total_travel_time
        
    def getTotalDistanceTravelled(self):
        #get trips info file from project file received 
        last_folder = os.path.split(self.projectcfgfilename)[0]
        tripinfo_file= 'tripinfo_'+last_folder+'.xml'
        tripinfo_filepath = os.path.join(last_folder,tripinfo_file)
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='travel_distance.log', level=logging.DEBUG, filemode="w+")

        tree = ET.parse(tripinfo_filepath)
        root = tree.getroot()

        for trip in root.findall('tripinfo'):
            veh_id = trip.get('id')
            distance = float(trip.get('routeLength'))
            logger.info(f"Vehicle {veh_id} traveled distance: {distance} meters")
            self.vehicle_distances[veh_id] = distance
            
        #Save to csv
        with open("Results/vehicle_distances.csv", 'w') as output:
            writer = csv.writer(output)
            writer.writerow(["vehicle_id", "distance_travelled"])
            for vehicle_id, distance in self.vehicle_distances.items(): 
                writer.writerow([vehicle_id,distance])
        return sum(self.vehicle_distances.values())
    
    # Start the simulation
    def run(self, gui=False):
        #total_travel_time = 0 
        try: 
            if gui: 
                traci_command = ["sumo-gui", "-c",  self.projectcfgfilename, "--no-step-log", "-W", "--seed", "8"]
                
            else: 
                traci_command = ["sumo", "-c",  self.projectcfgfilename, "--no-step-log", "-W", "--seed", "8"]
            traci.start(traci_command)
            # Run the simulation for 25000 steps
            for step in range(self.simulationsteps):
                traci.simulationStep()
                self.log_vehicle_on_entry(step=step, stop_range=self.simulationsteps)
                self.log_vehicle_on_exit(step=step, stop_range=self.simulationsteps)
            traci.close()
           
            travel_time = self.calculate_total_travel_time()
            total_distance_travelled = self.getTotalDistanceTravelled()
            return travel_time,total_distance_travelled
        except Exception as e: 
            self.logger.error(e)
            traci.close()