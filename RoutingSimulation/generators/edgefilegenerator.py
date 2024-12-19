import csv

class EdgeFileGenerator(): 
    def __init__(self, inputsfolder="inputs", outputsfolder="outputs", edges_csv_file='edges.csv'): 
        self.edge_file_name = inputsfolder+"/"+edges_csv_file
        self.edges = []
        self.outputsfolder = outputsfolder
        try:
            with open(self.edge_file_name, newline='') as edgesfile: 
                edgereader = csv.reader(edgesfile, delimiter=',')
                for row in edgereader: 
                    edge = ', '.join(row)
                    self.edges.append(edge)
        except FileNotFoundError: 
            print("No Edges csv file found, cannot proceed further ... \n Provide an inputs/edges.csv file")

        self.edges = self.edges[1:]
        
    def __get_edges(self): 
        forward_edges = []
        # reverse_edges = []
        for edge in self.edges:
            edge_details = edge.split(',')
            edge_id = edge_details[0].strip()
            edge_from = edge_details[1].strip()
            edge_to = edge_details[2].strip()
            edge_priority = edge_details[3].strip()
            edge_numlanes = edge_details[4].strip()
            edge_speed = edge_details[5].strip()
            
            forward_edge = f'<edge id="{edge_id}" from="{edge_from}" to="{edge_to}" priority="{edge_priority}" numLanes="{edge_numlanes}" speed="{edge_speed}"/>\n'
            # reverse_edge = f'<edge id="r{edge_id}" from="{edge_to}" to="{edge_from}" priority="{edge_priority}" numLanes="{edge_numlanes}" speed="{edge_speed}"/>\n'
            forward_edges.append(forward_edge)
            # reverse_edges.append(reverse_edge)
        return forward_edges
        # return reverse_edges
        

    def generate(self, filename='sumoproject'): 
        edge_filename = self.outputsfolder + "/" + filename + '.edg.xml'
        with open(edge_filename, 'w') as xfile:
            xfile.write("<edges>\n")
            forward = self.__get_edges()
            for line in forward: 
                xfile.write(line)
            # #for line in reverse: 
            #     xfile.write(line)
            xfile.write("</edges>\n")  # Added newline for better formatting
        print(f"edge file: {edge_filename} generated successfully. Filename returned")

        return edge_filename
