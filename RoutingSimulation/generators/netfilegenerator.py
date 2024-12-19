import subprocess

class NetFileGenerator: 
    def __init__(self, outputsfolder = "outputs", outfilename="sumoproject"): 
        self.outfilename = outputsfolder+"/"+outfilename

    def generate(self, nodefile, edgefile): 
        outputfile = self.outfilename + ".net.xml"
        command = f"netconvert --node-files={nodefile} --edge-files={edgefile} -o {outputfile} --no-warnings".split(" ")
        subprocess.run(command)
        print(f"Network file: {outputfile} generated successfully.")
        
        return outputfile
