import csv 

class TazFileGenerator: 
    def __init__(self, inputsfolder="inputs", outputsfolder="outputs", taz_csv_file='taz.csv'): 
        self.input_csv_tazfile = inputsfolder + "/" + taz_csv_file
        self.outputsfolder = outputsfolder
        self.tazs = []
        try:
            with open(self.input_csv_tazfile, newline='') as tazfile: 
                tazreader = csv.reader(tazfile, delimiter=',')
                self.tazs = list(tazreader)[1:]  # Read all lines and skip the header
        except FileNotFoundError: 
            print("No taz csv file found, cannot proceed further ... \n Provide an inputs/taz.csv file")

    def __get_taz_lines(self): 
        taz_lines = []
        for taz in self.tazs:
            taz_id = taz[0].strip()
            edges = taz[1].strip()
            
            taz_record = f'    <taz id="{taz_id}" edges="{edges}"/>\n'
            taz_lines.append(taz_record)
        return taz_lines

    def generate(self, filename='sumoproject'):
        taz_filename = self.outputsfolder+ "/" +filename + '.taz.xml'
        with open(taz_filename, 'w') as xfile:
            xfile.write("<tazs>\n")
            taz_records = self.__get_taz_lines()
            for line in taz_records: 
                xfile.write(line)
            xfile.write("</tazs>")
        print(f"taz file: {taz_filename} generated successfully. Filename returned")
        
        return taz_filename
