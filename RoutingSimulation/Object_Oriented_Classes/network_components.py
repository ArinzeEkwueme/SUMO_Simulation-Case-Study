import xml.etree.ElementTree as ET

class Node:
    def __init__(self, id, x, y, node_type, tl_type):
        self.id = id
        self.x = x
        self.y = y
        self.node_type = node_type
        self.tl_type = tl_type  # Traffic light type

    def __repr__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y}, type={self.node_type}, tlType={self.tl_type})"

    # Getter methods
    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_node_type(self):
        return self.node_type

    def get_tl_type(self):
        return self.tl_type
    
class Edge:
    def __init__(self, id, from_node, to_node, priority, num_lanes, speed):
        self.id = id
        self.from_node = from_node
        self.to_node = to_node
        self.priority = priority
        self.num_lanes = num_lanes
        self.speed = speed

    def __repr__(self):
        return f"Edge(id={self.id}, from={self.from_node}, to={self.to_node}, priority={self.priority}, numLanes={self.num_lanes}, speed={self.speed})"
    
    # Getter methods
    def get_id(self):
        return self.id
    
    def get_from_node(self):
        return self.from_node
    
    def get_to_node(self):
        return self.to_node
    
    def get_priority(self):
        return int(self.priority)
    
    def get_num_lanes(self):
        return int(self.num_lanes)
    
    def get_speed(self):
        return float(self.speed)

class Vehicle:
    def __init__(self, id, depart, from_taz, to_taz, route_edges):
        self.id = id
        self.depart = depart
        self.from_taz = from_taz
        self.to_taz = to_taz
        self.edges = route_edges  # Path (list of edges for unique OD pair)
        self.step_entry = 0
        self.step_exit = 0
        self.travel_time = 0

    def __repr__(self):
        return f"Vehicle(id={self.id}, depart={self.depart}, fromTaz={self.from_taz}, toTaz={self.to_taz}, edges={self.edges})"
    
    # Getter methods
    def get_id(self):
        return self.id
    
    def get_depart(self):
        return self.depart
    
    def get_from_taz(self):
        return self.from_taz
    
    def get_to_taz(self):
        return self.to_taz
    
    def get_edges(self):
        return self.edges
    
    def set_time_entry(self, step_entry):
        self.step_entry = step_entry
    
    def set_time_exit(self, step_exit):
        self.step_exit = step_exit

    def get_travel_time(self):
        travel_time = self.travel_time = self.step_exit - self.step_entry
        return travel_time

class Network:
    def __init__(self, nodes, edges, vehicles):
        # Initialize lists to hold instances
        self.nodes = nodes
        self.edges = edges
        self.vehicles = vehicles
        self.od_pair_library = set()
        self.determine_od_pairs()

    def __repr__(self):
        return f"Network(nodes={len(self.nodes)}, edges={len(self.edges)}, vehicles={len(self.vehicles)})"
    
    def get_node_instance_by_id(self, node_id): 
        """Fetch the node instance from network by its ID."""
        found_node = next((n for n in self.nodes if n.get_id() == node_id), None)
        if found_node:
            return found_node
        
    def get_edge_instance_by_id(self, edge_id): 
        """Fetch the edge instance from network by its ID."""
        found_edge = next((e for e in self.edges if e.get_id() == edge_id), None)
        if found_edge:
            return found_edge
    
    def get_vehicle_instance_by_id(self, vehicle_id): 
        """Fetch the vehicle instance from network by its ID."""
        found_vehicle = next((v for v in self.vehicles if v.get_id() == vehicle_id), None)
        if found_vehicle:
            return found_vehicle
            
    def determine_od_pairs(self):
        for vehicle in self.vehicles:
            origin = vehicle.edges[0]
            destination = vehicle.edges[-1]
            od_pair = (origin, destination)
            self.od_pair_library.add(od_pair)
    

class Loader:
    @staticmethod
    def load_nodes(nodefilename):
        tree = ET.parse(nodefilename)
        root = tree.getroot()
        nodes = []
        for node in root.findall('node'):
            id = node.get('id')
            x = float(node.get('x'))
            y = float(node.get('y'))
            node_type = node.get('type')
            tl_type = node.get('tlType', '')
            nodes.append(Node(id, x, y, node_type, tl_type)) #instantiate a node for each line in node file
        return nodes

    @staticmethod
    def load_edges(edgefilename):
        tree = ET.parse(edgefilename)
        root = tree.getroot()
        edges = []
        for edge in root.findall('edge'):
            id = edge.get('id')
            from_node = edge.get('from')
            to_node = edge.get('to')
            priority = int(edge.get('priority', 0))
            num_lanes = int(edge.get('numLanes', 1))
            speed = float(edge.get('speed', 13.89))  # Default speed in m/s
            edges.append(Edge(id, from_node, to_node, priority, num_lanes, speed))
        return edges

    @staticmethod
    def load_vehicles(routefilename):
        tree = ET.parse(routefilename)
        root = tree.getroot()
        vehicles = []
        for vehicle in root.findall('vehicle'):
            vehicle_id = vehicle.get('id')
            depart = vehicle.get('depart')
            from_taz = vehicle.get('fromTaz')
            to_taz = vehicle.get('toTaz')
            edges = vehicle.find('route').get('edges', '').split()  # Get edges from route
            vehicles.append(Vehicle(vehicle_id, depart, from_taz, to_taz, edges))
        return vehicles
