#!/usr/bin/env python3
#convert testbeam data into txt
#################################################################
                                                               ##
import sys                                                     ##
import rogue                                                   ##
import time                                                    ##
import random                                                  ##
import argparse                                                ##
                                                               ##
import pyrogue as pr                                           ##
import pyrogue.gui                                             ##
import numpy as np                                             ##
import common as feb                                           ##
                                                               ##
import os                                                      ##
import rogue.utilities.fileio                                  ##
#################################################################
def parse_arguments():
    parser = argparse.ArgumentParser()

    # Convert str to bool
    argBool = lambda s: s.lower() in ['true', 't', 'yes', '1']
    
    parser.add_argument("--in", nargs ='+',required = True, help = "input files")

    # Get the arguments
    args = parser.parse_args()
    return args
#################################################################

def convertTBdata(inFiles):
    
    for inFile in inFiles:
        print("Opening file "+inFile)

        HitData = []
        overflowTOA = []
        HitDataTOTc = []
        HitDataTOTf = []
        overflowTOT = []
        cntTOA = 0
        cntTOT = 0

        # Create the File reader streaming interface
        dataReader = rogue.utilities.fileio.StreamReader()

        # Create the Event reader streaming interface
        dataStream = feb.MyFileReader()

        # Connect the file reader ---> event reader
        pr.streamConnect(dataReader, dataStream)

        # Open the file
        dataReader.open(inFile)

        # Close file once everything processed
        dataReader.closeWait()

        HitData = dataStream.HitData
        HitDataTOTc = dataStream.HitDataTOTc_vpa
        HitDataTOTf = dataStream.HitDataTOTf_vpa
        overflowTOA = dataStream.OvfTOA
        overflowTOT = dataStream.OvfTOT

        cntTOA = len(HitData)
        cntTOT = len(HitDataTOTc)

        #name output equal to input
        outFile = inFile[:inFile.find('dat')-2]+'.txt'
        if os.path.exists(outFile)
            ts = str(int(time.time()))
            outFile = outFile[:outFile.find('txt')-2]+ts+'.txt'
            print('File exists, will be saved as '+outFile)
        myfile = open(outFile,'w+')
    
#################################################################
if __name__ == "__main__":
    args = parse_arguments()
    print(args)    
    convertTBdata(agrs.in)