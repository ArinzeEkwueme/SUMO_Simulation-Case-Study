from generators.nodefilegenerator import NodeFileGenerator
from generators.edgefilegenerator import EdgeFileGenerator
from generators.tazfilegenerator import TazFileGenerator
from generators.netfilegenerator import NetFileGenerator
from generators.odtripsfilegenerator import OdTripsFileGenerator


def run_generators (): 
    #step1 generate node file from inputs
    nodefile_instance = NodeFileGenerator()
    nodefilename = nodefile_instance.generate()
    #we expect a sumoproject.nod.xml to exist

    #step 2 generate edge file from inputs
    edgefile_instance  = EdgeFileGenerator()
    edgefilename = edgefile_instance.generate()
    #we expect a sumoproject.edg.xml to exist

    #step 3 we use nod and edg files from step 1 and 2 to create net file
    netfileInstance = NetFileGenerator()
    netfilename = netfileInstance.generate(nodefilename, edgefilename)

    #step 4 we create taz file from inputs
    tazfile_instance = TazFileGenerator()
    tazfilename = tazfile_instance.generate()

    #step 5 we use the tazfilename and matrix od files 
    odtripsfile_instance = OdTripsFileGenerator()
    odtripsfilename = odtripsfile_instance.generate(tazfilename)


    return nodefilename, edgefilename, netfilename, tazfilename, odtripsfilename