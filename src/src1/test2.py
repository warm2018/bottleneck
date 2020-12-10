from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import optparse
import subprocess
import random
import traci
import math
import xlsxwriter

from copy import deepcopy

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
     from sumolib import checkBinary
else:   
     sys.exit("please declare environment variable 'SUMO_HOME'")



def run(): 
    STEP = 0
    StepLength = 0.01
    while STEP < 1800: 
        traci.simulationStep()  
        STEP += StepLength
    workbook.close()
    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
     default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options
    # this is the main entry point of this script



if __name__ == "__main__":


    options = get_options()
    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    #"--collision.action", "none",
    #"--collision.mingap-factor", "0",
    traci.start([sumoBinary, "-c", "cfg/freeway.sumocfg",
                             "--tripinfo-output", "result/tripinfo.xml",
                             "--step-length","0.01",
                             "--device.emissions.probability", "1.0",])


    run()

