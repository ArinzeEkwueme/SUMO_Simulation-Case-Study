import yaml  # type: ignore
import numpy as np  # type: ignore

class NodeFileGenerator: 
    def __init__(self, inputsfolder ="inputs", outputsfolder ="outputs", inputs_yaml_file='nodes.yml'):
        self.inputfilename = inputsfolder+"/"+inputs_yaml_file
        self.outputsfolder = outputsfolder
        try:
            with open(self.inputfilename) as f: 
                node_inputs = yaml.safe_load(f)
                nodeFileDetails = node_inputs['nodes']
                self.count = nodeFileDetails['count']
                self.priority_type = nodeFileDetails['type']
                self.tl_type = nodeFileDetails['tlType']
                self.x_spacing = nodeFileDetails['xSpacing']
                self.y_spacing = nodeFileDetails['ySpacing']
                self.y_max = nodeFileDetails['yMax']
                
        except FileNotFoundError: 
            print("No Nodes yml file found, cannot proceed further ... \n Provide an inputs/node.yml file")
            self.count = 0  # Initialize count to avoid errors later
            self.priority_type = ''
            self.tl_type = ''
            self.x_spacing = 0
            self.y_spacing = 0
            self.y_max = 0
        
        self.nodes_per_line = self.y_max // self.y_spacing

    def __generate_grid(self, number_count, max_rows):
        # Determine the number of columns based on the number count and max rows
        num_cols = (number_count + max_rows - 1) // max_rows  # Use ceiling division
        
        # Create an empty array filled with zeros or another placeholder
        grid = np.full((max_rows, num_cols), fill_value=np.nan)  # Fill with NaN for better handling
        
        # Populate the grid with numbers
        for row in range(max_rows):
            for col in range(num_cols):
                num = col * max_rows + row + 1  # Calculate the number in each cell
                if num <= number_count:
                    grid[row, col] = num  # Place the number
        return grid

    def __create_coordinate_map(self, input_grid, x_spacing, y_spacing):
        rows, cols = input_grid.shape  # Get the shape of the input grid
        coordinate_map = {}
    
        for i in range(rows):
            for j in range(cols):
                # Calculate the x and y coordinates based on spacing and position in grid
                x = j * x_spacing
                y = -i * y_spacing  # Negative because y decreases as we go down the grid
                
                # Map the grid element to its coordinate
                if input_grid[i, j] is not np.nan:  # Avoid mapping NaN values
                    coordinate_map[input_grid[i, j]] = (x, y)
        
        return coordinate_map
    
    def __get_xy_value(self, i): 
        grid = self.__generate_grid(self.count, self.nodes_per_line)
        coordinate_map = self.__create_coordinate_map(grid, self.x_spacing, self.y_spacing)
        return coordinate_map
        
    def __get_file_content(self): 
        content = []
        for i in range(1, self.count + 1):  # Loop from 1 to count (inclusive)
            dict_map = self.__get_xy_value(i)[i]
            line = f'<node id="{i}" x="{dict_map[0]}" y="{dict_map[1]}" type="{self.priority_type}" tlType="{self.tl_type}"/>\n'
            content.append(line)
        return content

    def generate(self, filename='sumoproject'): 
        node_filename = self.outputsfolder+"/"+filename + '.nod.xml'
        
        with open(node_filename, 'w') as xfile:
            xfile.write("<nodes>\n")
            lines = self.__get_file_content()
            for line in lines: 
                xfile.write(line)
            xfile.write("</nodes>")
        
        print(f"node file: {node_filename} generated successfully. Filename returned.")
        
        return node_filename
