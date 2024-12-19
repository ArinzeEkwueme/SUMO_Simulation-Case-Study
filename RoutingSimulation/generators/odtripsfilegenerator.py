import os
import subprocess

class OdTripsFileGenerator: 
    def __init__(self, inputsfolder="inputs", outputsfolder = "outputs"): 
        self.outputsfolder = outputsfolder
        self.inputsfolder = inputsfolder

    def generate(self, tazfile, outfilename="sumoproject"):
        try: 
            odfiles = []
            for file in os.listdir(self.inputsfolder): 
                if file.endswith(".od"):
                    odfiles.append(os.path.join(self.inputsfolder, file))  # Use os.path.join for portability
            if len(odfiles) == 0: 
                raise FileNotFoundError
            else: 
                print("Found OD matrix files \n")
        except FileNotFoundError: 
            print("OD matrix files not found, cannot proceed further ... \n Provide OD matrix files in inputs folder")
            return None  # Added return statement here to exit the method

        try: 
            outputfile = self.outputsfolder+"/"+outfilename + ".odtrips.xml"
            odfilenames = ",".join(odfiles)
            command = f"od2trips --od-matrix-files {odfilenames} --taz-files {tazfile} -o {outputfile} -W --seed 8".split(" ")
            subprocess.run(command)
        except Exception as e:
            print(e)
            raise e

        return outputfile
