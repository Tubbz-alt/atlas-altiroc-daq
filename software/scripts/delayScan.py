#!/usr/bin/env python3
##############################################################################
## This file is part of 'ATLAS ALTIROC DEV'.
## It is subject to the license terms in the LICENSE.txt file found in the 
## top-level directory of this distribution and at: 
##    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
## No part of 'ATLAS ALTIROC DEV', including this file, 
## may be copied, modified, propagated, or distributed except according to 
## the terms contained in the LICENSE.txt file.
##############################################################################

##############################################################################
# Script Settings

asicVersion = 1 # <= Select either V1 or V2 of the ASIC

DebugPrint = True

#configFile = 'config/testBojan11.yml' # <= Path to the Configuration File to be Loaded
configFile = 'config/config_v2B6_noPAprobe.yml' # <= Path to the Configuration File to be Loaded
#configFile = 'config/config_v2B6_def.yml' # <= Path to the Configuration File to be Loaded

pixel_number = 4 # <= Pixel to be Tested

DataAcqusitionTOA = 1   # <= Enable TOA Data Acquisition (Delay Sweep)
DelayRange_low = 2100     # <= low end of Programmable Delay Sweep
DelayRange_high = 2700     # <= high end of Programmable Delay Sweep
DelayRange_step = 20     # <= step size Programmable Delay Sweep
NofIterationsTOA = 50  # <= Number of Iterations for each Delay value

DataAcqusitionTOT = 0   # <= Enable TOT Data Acquisition (Pulser Sweep)
PulserRangeL = 0        # <= Low Value of Pulser Sweep Range
PulserRangeH = 40       # <= High Value of Pulser Sweep Range
PulserRangeStep = 1     # <= Step Size of Pulser Sweep Range
NofIterationsTOT = 100   # <= Number of Iterations for each Pulser Value
DelayValueTOT = 2400       # <= Value of Programmable Delay for TOT Pulser Sweep

nTOA_TOT_Processing = 0 # <= Selects the Data to be Processed and Plotted (0 = TOA, 1 = TOT) 

TOT_f_Calibration_En = 0                                       	   # <= Enables Calculation of TOT Fine-Interpolation Calibration Data and Saves them
#TOT_f_Calibration_LOAD_file = 'TestData/TOT_fine_nocalibration.txt'
TOT_f_Calibration_LOAD_file = 'TestData/TOT_fine_calibration.txt'  # <= Path to the TOT Fine-Interpolation Calibration File used in TOT Data Processing
#TOT_f_Calibration_LOAD_file = 'TestData/TOT_fine_calibration2.txt'  # <= Path to the TOT Fine-Interpolation Calibration File used in TOT Data Processing
TOT_f_Calibration_SAVE_file = 'TestData/TOT_fine_calibration2.txt'  # <= Path to the File where TOT Fine-Interpolation Calibration Data are Saved

DelayStep = 9.5582  # <= Estimate of the Programmable Delay Step in ps (measured on 10JULY2019)
LSB_TOTc = 190    # <= Estimate of TOT coarse LSB in ps
LSB_TOTc = 160
#LSB_TOTc = 1

nVPA_TZ = 0 # <= TOT TDC Processing Selection (0 = VPA TOT, 1 = TZ TOT) (!) Warning: TZ TOT not yet tested

HistDelayTOA1 = 2500  # <= Delay Value for Histogram to be plotted in Plot (1,0)
HistDelayTOA2 = 2550 # <= Delay Value for Histogram to be plotted in Plot (1,1)
HistPulserTOT1 = 5  # <= Pulser Value for Histogram to be plotted in Plot (1,0)
HistPulserTOT2 = 10  # <= Pulser Value for Histogram to be plotted in Plot (1,1)

Disable_CustomConfig = 0 # <= Disables the ASIC Configuration Customization inside the Script (Section Below) => all Configuration Parameters are taken from Configuration File   

TOTf_hist = 0
TOTc_hist = 0
Plot_TOTf_lin = 1
PlotValidCnt = 1

##############################################################################

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
                                                               ##
import statistics                                              ##
import math                                                    ##
import matplotlib.pyplot as plt                                ##
#from setASICconfig_v2B8 import *                                                               ##
from setASICconfig_v2B7 import *                                                               ##
#################################################################


def acquire_data(range_low, range_high, range_step, top, 
        asic_pulser, file_prefix, n_iterations, dataStream): 

    for i in range(range_low, range_high, range_step):
        print(file_prefix+'step = %d' %i)
        asic_pulser.set(i)

        filename = 'TestData/'+file_prefix+'%d.dat' %i
        try: os.remove(filename)
        except OSError: pass

        top.dataWriter._writer.open(filename)

        for j in range(n_iterations):
            if (asicVersion == 1):
                top.Fpga[0].Asic.LegacyV1AsicCalPulseStart()
                time.sleep(0.001)
            else:
                top.Fpga[0].Asic.CalPulse.Start()
                time.sleep(0.001)

        while dataStream.count < n_iterations: pass
        top.dataWriter._writer.close()
        dataStream.count = 0

#################################################################
def get_sweep_index(sweep_value, sweep_low, sweep_high, sweep_step):
    if sweep_value < sweep_low:
        sweep_value = sweep_low+sweep_step
        print( 'Sweep value {} outside of sweep range [{}:{}]'.format(sweep_value, sweep_low, sweep_high) )
    elif sweep_high < sweep_value:
        sweep_value = sweep_high-sweep_step
        print( 'Sweep value {} outside of sweep range [{}:{}]'.format(sweep_value, sweep_low, sweep_high) )
    if sweep_value % sweep_step != 0:
        print( 'Sweep value {} is not a multiple of sweep step {}'.format(sweep_value, sweep_step) )
    return sweep_value,int((sweep_value - sweep_low) / sweep_step)

#################################################################


#################################################################
# Set the argument parser
parser = argparse.ArgumentParser()

HistDelayTOA1, HistDelayTOA1_index  = get_sweep_index(HistDelayTOA1 , DelayRange_low, DelayRange_high, DelayRange_step)
HistDelayTOA2, HistDelayTOA2_index  = get_sweep_index(HistDelayTOA2 , DelayRange_low, DelayRange_high, DelayRange_step)
HistPulserTOT1, HistPulserTOT1_index = get_sweep_index(HistPulserTOT1, PulserRangeL, PulserRangeH, PulserRangeStep)
HistPulserTOT2, HistPulserTOT2_index = get_sweep_index(HistPulserTOT2, PulserRangeL, PulserRangeH, PulserRangeStep)


# Convert str to bool
argBool = lambda s: s.lower() in ['true', 't', 'yes', '1']

# Add arguments
parser.add_argument(
    "--ip", 
    nargs    ='+',
    required = True,
    help     = "List of IP addresses",
)  
# Get the arguments
args = parser.parse_args()

#################################################################
# Setup root class
#top = feb.Top(ip= args.ip, loadYaml= False)    
top = feb.Top(ip= args.ip)    

# Load the default YAML file
print(f'Loading {configFile} Configuration File...')
top.LoadConfig(arg = configFile)

if DebugPrint:
    # Tap the streaming data interface (same interface that writes to file)
    dataStream = feb.MyEventReader()    
    pyrogue.streamTap(top.dataStream[0], dataStream) # Assuming only 1 FPGA

#testing resets
top.Fpga[0].Asic.Gpio.RSTB_DLL.set(0x0)
time.sleep(0.001)
top.Fpga[0].Asic.Gpio.RSTB_DLL.set(0x1)
time.sleep(0.001)
top.Fpga[0].Asic.Gpio.RSTB_TDC.set(0x0)
time.sleep(0.001)
top.Fpga[0].Asic.Gpio.RSTB_TDC.set(0x1)

# Custom Configuration
if Disable_CustomConfig == 0:
    set_fpga_for_custom_config(top,pixel_number)

# Data Acquisition for TOA and TOT
if DataAcqusitionTOA == 1:
    acquire_data(DelayRange_low, DelayRange_high, DelayRange_step, top,
            top.Fpga[0].Asic.Gpio.DlyCalPulseSet, 'TOA', NofIterationsTOA, dataStream)

top.Fpga[0].Asic.Gpio.DlyCalPulseSet.set(DelayValueTOT)

if DataAcqusitionTOT == 1:
    acquire_data(PulserRangeL, PulserRangeH, PulserRangeStep, top, 
            top.Fpga[0].Asic.SlowControl.dac_pulser, 'TOT', NofIterationsTOT, dataStream)

#######################
# Data Processing TOA #
#######################

if nTOA_TOT_Processing == 0:

    Delay = []
    HitCnt = []
    TOAmean = []
    TOAsigma = []
    allHitDataTOA = []

    for delay_value in range(DelayRange_low, DelayRange_high, DelayRange_step):
        # Create the File reader streaming interface
        dataReader = rogue.utilities.fileio.StreamReader()

        # Create the Event reader streaming interface
        dataStream = feb.MyFileReader()

        # Connect the file reader ---> event reader
        pr.streamConnect(dataReader, dataStream) 

        # Open the file
        dataReader.open('TestData/TOA%d.dat' %delay_value)

        # Close file once everything processed
        dataReader.closeWait()

    
        try:
            print('Processing Data for Delay = %d...' % delay_value)
        except OSError:
            pass  

        HitDataTOA = dataStream.HitData
        allHitDataTOA.append(HitDataTOA)

        exec("%s = %r" % ('HitDataTOA%d' %delay_value, HitDataTOA))

        Delay.append(delay_value)

        HitCnt.append(len(HitDataTOA))
        if len(HitDataTOA) > 0:
            TOAmean.append(np.mean(HitDataTOA, dtype=np.float64))
            TOAsigma.append(math.sqrt(math.pow(np.std(HitDataTOA, dtype=np.float64),2)+1/12))

        else:
            TOAmean.append(0)
            TOAsigma.append(0)
  
    if len(TOAmean) == 0:
        raise ValueError('No hits were detected during delay sweep. Aborting!')

    # Average Std. Dev. Calculation; Points with no data (i.e. Std.Dev.= 0) are ignored
    index = np.where(np.sort(TOAsigma))
    MeanTOAsigma = np.mean(np.sort(TOAsigma)[index[0][0]:len(np.sort(TOAsigma))])

    # LSB estimation based on "DelayStep" value
    print(TOAmean)
    index=np.where(TOAmean)
    #avoid crashes due to fit
    #if len(index)>6:
    #    fit = np.polyfit(Delay[index[0][5]:index[0][-5]], TOAmean[index[0][5]:index[0][-5]], 1)
    #else: fit=[1,1]

    fit = np.polyfit(Delay[index[0][3]:index[0][-3]], TOAmean[index[0][3]:index[0][-3]], 1)
    LSBest = DelayStep/abs(fit[0])

#################################################################
# TOT Fine Interpolator Calibration

if nTOA_TOT_Processing == 1 and TOT_f_Calibration_En == 1:
    # Create the File reader streaming interface
    dataReader = rogue.utilities.fileio.StreamReader()

    # Create the Event reader streaming interface
    dataStream = feb.MyFileReader()

    # Connect the file reader ---> event reader
    pr.streamConnect(dataReader, dataStream) 

    for i in range(PulserRangeL, PulserRangeH):
        # Open the file
        dataReader.open('TestData/TOT%d.dat' %i)
        time.sleep(0.01)
        # Close file once everything processed
        dataReader.closeWait()
        time.sleep(0.01)
    
    if not nVPA_TZ:    
        HitDataTOTf_cumulative = dataStream.HitDataTOTf_vpa
    else:
        HitDataTOTf_cumulative = dataStream.HitDataTOTf_tz
    
    TOTf_bin_width = np.zeros(16)
    for i in range(16):
        TOTf_bin_width[i]=len(list(np.where(np.asarray(HitDataTOTf_cumulative)==i))[0])
    TOTf_bin_width = TOTf_bin_width/sum(TOTf_bin_width)

    TOTf_bin = np.zeros(18)
    for i in range(1,17):
        TOTf_bin[i]=len(list(np.where(np.asarray(HitDataTOTf_cumulative)==i-1))[0])

    index = np.where(np.sort(TOTf_bin))
    LSB_TOTf_mean = np.mean(np.sort(TOTf_bin)[index[0][0]:len(np.sort(TOTf_bin))])/sum(TOTf_bin)

    TOTf_bin = (TOTf_bin[1:18]/2 + np.cumsum(TOTf_bin)[0:17])/sum(TOTf_bin)
    TOTf_bin[16] = LSB_TOTf_mean

    try:
        print('TOT Fine Interpolator Bin-Widths:')
        print(TOTf_bin_width*2*LSB_TOTc)
        print('Average TOT LSB = %f ps' % (LSB_TOTf_mean*2*LSB_TOTc))
    except OSError:
        pass   

    np.savetxt(TOT_f_Calibration_SAVE_file,TOTf_bin)

#################################################################
# Data Processing TOT

if nTOA_TOT_Processing == 1:

    Pulser = []
    ValidTOTCnt = []
    DataMeanTOT = []
    DataStdevTOT = []
    HitDataTOTf_cumulative = []

    for i in range(PulserRangeL, PulserRangeH):
        # Create the File reader streaming interface
        dataReader = rogue.utilities.fileio.StreamReader()

        # Create the Event reader streaming interface
        dataStream = feb.MyFileReader()

        # Connect the file reader ---> event reader
        pr.streamConnect(dataReader, dataStream) 

        # Open the file
        dataReader.open('TestData/TOT%d.dat' %i)

        # Close file once everything processed
        dataReader.closeWait()

    
        try:
            print('Processing Data for Pulser = %d...' % i)
        except OSError:
            pass  

        if not nVPA_TZ:    
            HitDataTOTf = dataStream.HitDataTOTf_vpa
            HitDataTOTc = dataStream.HitDataTOTc_vpa
            HitDataTOTc_int1 = dataStream.HitDataTOTc_int1_vpa
            HitDataTOTf_cumulative = HitDataTOTf_cumulative + dataStream.HitDataTOTf_vpa
        else:
            HitDataTOTf = dataStream.HitDataTOTf_tz
            HitDataTOTc = dataStream.HitDataTOTc_tz
            HitDataTOTc_int1 = dataStream.HitDataTOTc_int1_tz
            HitDataTOTf_cumulative = HitDataTOTf_cumulative + dataStream.HitDataTOTf_tz
    
        Pulser.append(i)
    
        TOTf_bin = np.loadtxt(TOT_f_Calibration_LOAD_file) 
        LSB_TOTf_mean = TOTf_bin[16]*2*LSB_TOTc

        def calibration_correction(f,c):
            if f > 3 and c == 0:
                return 2
            else:
                if f == 0 and c == 1:
                    return -TOTf_bin[0]*2
                else:
                    return 0
        IntFVa = 1
        if IntFVa == 1:
            if len(HitDataTOTf) > 0:
                HitDataTOT = list((np.asarray(HitDataTOTc_int1)*2 + 1 - np.asarray(list(map(lambda x: TOTf_bin[x], np.asarray(HitDataTOTf, dtype=np.int))))*2)*LSB_TOTc)
            
                HitDataTOT = list(HitDataTOT + np.asarray(list(map(calibration_correction, HitDataTOTf, list(map(lambda x: x&1, np.asarray(HitDataTOTc))))))*LSB_TOTc)
            else:
                HitDataTOT = []    
        else:
            if len(HitDataTOTf) > 0:
                HitDataTOT = list((np.asarray(HitDataTOTc) + 1 - np.asarray(HitDataTOTf)/4)*LSB_TOTc)
            else:
                HitDataTOT = []  

        #HitDataTOT = HitDataTOTc

        exec("%s = %r" % ('HitDataTOT%d' %i, HitDataTOT))
        exec("%s = %r" % ('HitDataTOTf%d' %i, HitDataTOTf))
        exec("%s = %r" % ('HitDataTOTc%d' %i, HitDataTOTc))

        ValidTOTCnt.append(len(HitDataTOT))
        if len(HitDataTOT) > 0:        
            DataMeanTOT.append(np.mean(HitDataTOT, dtype=np.float64))
            DataStdevTOT.append(math.sqrt(math.pow(np.std(HitDataTOT, dtype=np.float64),2) + math.pow(LSB_TOTf_mean,2)/12))

        else:
            DataMeanTOT.append(0)
            DataStdevTOT.append(0)

    # Average Std. Dev. Calculation; Points with no data (i.e. Std.Dev.= 0) are ignored
    index = np.where(np.sort(DataStdevTOT))
    MeanDataStdevTOT = np.mean(np.sort(DataStdevTOT)[index[0][0]:len(np.sort(DataStdevTOT))])

#################################################################
# Print Data
if nTOA_TOT_Processing == 0:
    for delay_index, delay_value in enumerate(Delay):
        try:
            print('Delay = %d, HitCnt = %d, TOAmean = %f LSB, DataStDev = %f LSB' % (delay_value, HitCnt[delay_index], TOAmean[delay_index], TOAsigma[delay_index]))
        except OSError:
            pass   
    try:
        print('Maximum Measured TOA = %f LSB' % np.max(TOAmean))
        print('Mean Std Dev = %f LSB' % MeanTOAsigma)
    except OSError:
        pass
    for delay_index, delay_value in enumerate(Delay):
        try:
            print('Delay = %d, HitCnt = %d, TOAmean = %f ps, DataStDev = %f ps' % (delay_value, HitCnt[delay_index], TOAmean[delay_index]*LSBest, TOAsigma[delay_index]*LSBest))
        except OSError:
            pass
    try:
        print('Maximum Measured TOA = %f ps' % (np.max(TOAmean)*LSBest))
        print('Mean Std Dev = %f ps' % (MeanTOAsigma*LSBest))
        print('Average LSB estimate: %f ps' % LSBest)
    except OSError:
        pass
#################################################################
    #################################################################
    # Save Data
    #################################################################
    outFile = 'TestData/delayScanTOA'
    ff = open(outFile+'.txt','a')
    ff.write('Delay Scan TOA measurement ---- '+time.ctime()+'\n')
    ff.write('Pixel = '+str(pixel_number)+'\n')
    ff.write('config file = '+configFile+'\n')
    ff.write('NofIterations = '+str(NofIterationsTOA)+'\n')
    #ff.write('cmd_pulser = '+str(Qinj)+'\n')
    #ff.write('Delay DAC = '+str(DelayValue)+'\n')
    ff.write('LSBest = '+str(LSBest)+'\n')
    #ff.write('Threshold = '+str(DACvalue)+'\n')
    ff.write('N hits = '+str(HitCnt)+'\n')
    ff.write('Number of events = '+str(len(HitDataTOA))+'\n')
    ff.write('mean value = '+str(TOAmean)+'\n')
    ff.write('sigma = '+str(TOAsigma)+'\n')
    for iTOA in range(len(allHitDataTOA)):
      delay = Delay[iTOA]
      for toa in allHitDataTOA[iTOA]:
        ff.write(str(delay)+' '+str(toa)+'\n')
    #ff.write('TOAvalues = '+str(allHitDataTOA)+'\n')
    ff.write('\n')
    ff.close()

    print('Saved file '+outFile)
#################################################################
# Plot Data

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows = 2, ncols = 2, figsize=(16,7))

#LSBest = 1

if nTOA_TOT_Processing == 0:
    # Plot (0,0) ; top left
    #ax1.plot(Delay, np.multiply(TOAmean,LSBest))
    ax1.plot(Delay, TOAmean)
    ax1.grid(True)
    ax1.set_title('TOA Measurment VS Programmable Delay Value', fontsize = 11)
    ax1.set_xlabel('Programmable Delay Value [step estimate = %f ps]' % DelayStep, fontsize = 10)
    ax1.set_ylabel('Mean Value [ps]', fontsize = 10)
    ax1.legend(['LSB estimate: %f ps' % LSBest],loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
    ax1.set_xlim(left = np.min(Delay), right = np.max(Delay))
    #ax1.set_ylim(bottom = 0, top = np.max(np.multiply(TOAmean,LSBest))+100)
    ax1.set_ylim(bottom = 0, top = np.max(TOAmean)+100)
else:
    # Plot (0,0) ; top left
    ax1.plot(Pulser, DataMeanTOT)
    ax1.grid(True)
    ax1.set_title('TOT Measurment VS Injected Charge', fontsize = 11)
    ax1.set_xlabel('Pulser DAC Value', fontsize = 10)
    ax1.set_ylabel('Mean Value [ps]', fontsize = 10)
    ax1.set_xlim(left = np.min(Pulser), right = np.max(Pulser))
    ax1.set_ylim(bottom = 0, top = np.max(DataMeanTOT)*1.1)

if nTOA_TOT_Processing == 0:
    # Plot (0,1) ; top right
    ax2.scatter(Delay, np.multiply(TOAsigma,LSBest))
    ax2.grid(True)
    ax2.set_title('TOA Jitter VS Programmable Delay Value', fontsize = 11)
    ax2.set_xlabel('Programmable Delay Value', fontsize = 10)
    ax2.set_ylabel('Std. Dev. [ps]', fontsize = 10)
    ax2.legend(['Average Std. Dev. = %f ps' % (MeanTOAsigma*LSBest)], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
    ax2.set_xlim(left = np.min(Delay), right = np.max(Delay))
    ax2.set_ylim(bottom = 0, top = np.max(np.multiply(TOAsigma,LSBest))+20)
else:
    # Plot (0,1) ; top right
    if PlotValidCnt == 0:
        ax2.scatter(Pulser, DataStdevTOT)
        ax2.grid(True)
        ax2.set_title('TOT Jitter VS Injected Charge', fontsize = 11)
        ax2.set_xlabel('Pulser DAC Value', fontsize = 10)
        ax2.set_ylabel('Std. Dev. [ps]', fontsize = 10)
        ax2.legend(['Average Std. Dev. = %f ps' % MeanDataStdevTOT], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
        ax2.set_xlim(left = np.min(Pulser), right = np.max(Pulser))
        ax2.set_ylim(bottom = 0, top = np.max(DataStdevTOT)*1.1)
    else:
        ax2.plot(Pulser, ValidTOTCnt)
        ax2.grid(True)
        ax2.set_title('TOT Valid Counts VS Injected Charge', fontsize = 11)
        ax2.set_xlabel('Pulser DAC Value', fontsize = 10)
        ax2.set_ylabel('Valid Measurements', fontsize = 10)
        ax2.set_xlim(left = np.min(Pulser), right = np.max(Pulser))
        ax2.set_ylim(bottom = 0, top = np.max(ValidTOTCnt)*1.1)

if nTOA_TOT_Processing == 0:
    # Plot (1,0) ; bottom left
    exec("DataL = len(HitDataTOA%d)" % HistDelayTOA1)
    print(DataL)
    if DataL:
        #exec("ax3.hist(np.multiply(HitDataTOA%d,LSBest), bins = LSBest, align = 'left', edgecolor = 'k', color = 'royalblue')" % HistDelayTOA1)
        hist_range = 10
        binlow = ( int(TOAmean[HistDelayTOA1_index])-hist_range ) * LSBest
        binhigh = ( int(TOAmean[HistDelayTOA1_index])+hist_range ) * LSBest
        hist_bin_list = np.arange(binlow, binhigh, LSBest)
        exec("ax3.hist(np.multiply(HitDataTOA%d,LSBest), bins = hist_bin_list, align = 'left', edgecolor = 'k', color = 'royalblue')" % HistDelayTOA1)
        #exec("ax3.set_xlim(left = np.min(np.multiply(HitDataTOA%d,LSBest))-4*LSBest, right = np.max(np.multiply(HitDataTOA%d,LSBest))+4*LSBest)" % (HistDelayTOA1, HistDelayTOA1))
        ax3.set_title('TOA Measurment for Programmable Delay = %d' % HistDelayTOA1, fontsize = 11)
        ax3.set_xlabel('TOA Measurement [ps]', fontsize = 10)
        ax3.set_ylabel('N of Measrements', fontsize = 10)
        ax3.legend(['Mean = %f ps \nStd. Dev. = %f ps \nN of Events = %d' % (TOAmean[HistDelayTOA1_index]*LSBest, TOAsigma[HistDelayTOA1_index]*LSBest, HitCnt[HistDelayTOA1_index])], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
else:
    # Plot (1,0)
    #exec("print(HitDataTOT%d)" % HistPulserTOT1)
    #exec("print(HitDataTOTf%d)" % HistPulserTOT1)
    #exec("print(HitDataTOTc%d)" % HistPulserTOT1)
    #exec("print(np.asarray(list(map(lambda x: TOTf_bin[x], np.asarray(HitDataTOTf%d, dtype=np.int))))*2)" % HistPulserTOT1)
    #exec("print(list(map(lambda x: x&1, np.asarray(HitDataTOTc%d))))" % HistPulserTOT1)
    if TOTf_hist == 0 and TOTc_hist == 0:
        exec("DataL = len(HitDataTOT%d)" % HistPulserTOT1)
        if DataL:
            exec("ax3.hist(HitDataTOT%d, bins = np.multiply(np.arange(512),LSB_TOTf_mean), align = 'left', edgecolor = 'k', color = 'royalblue')" % HistPulserTOT1)
            exec("ax3.set_xlim(left = np.min(HitDataTOT%d)-10*LSB_TOTf_mean, right = np.max(HitDataTOT%d)+10*LSB_TOTf_mean)" % (HistPulserTOT1, HistPulserTOT1))
            ax3.set_title('TOT Measurment for Pulser = %d' % HistPulserTOT1, fontsize = 11)
            ax3.set_xlabel('TOT Measurement [ps]', fontsize = 10)
            ax3.set_ylabel('N of Measrements', fontsize = 10)
            ax3.legend(['Mean = %f ps \nStd. Dev. = %f ps \nN of Events = %d' % (DataMeanTOT[HistPulserTOT1_index], DataStdevTOT[HistPulserTOT1_index], ValidTOTCnt[HistPulserTOT1_index])], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
    else:
        if TOTf_hist == 1:
            exec("ax3.hist(HitDataTOTf%d, bins = np.arange(9), align = 'left', edgecolor = 'k', color = 'royalblue')" % HistPulserTOT1)
            ax3.set_xlim(left = -1, right = 8)
            ax3.set_title('TOT Measurment for Pulser = %d' % HistPulserTOT1, fontsize = 11)
            ax3.set_xlabel('TOT Measurement [ps]', fontsize = 10)
            ax3.set_ylabel('N of Measrements', fontsize = 10)
            ax3.legend(['Mean = %f ps \nStd. Dev. = %f ps \nN of Events = %d' % (DataMeanTOT[HistPulserTOT1_index], DataStdevTOT[HistPulserTOT1_index], ValidTOTCnt[HistPulserTOT1_index])], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
        else: 
            if TOTc_hist == 1:
                exec("ax3.hist(HitDataTOTc%d, bins = np.arange(129), align = 'left', edgecolor = 'k', color = 'royalblue')" % HistPulserTOT1)
                ax3.set_xlim(left = -1, right = 128)
                ax3.set_title('TOT Measurment for Pulser = %d' % HistPulserTOT1, fontsize = 11)
                ax3.set_xlabel('TOT Measurement [ps]', fontsize = 10)
                ax3.set_ylabel('N of Measrements', fontsize = 10)
                ax3.legend(['Mean = %f ps \nStd. Dev. = %f ps \nN of Events = %d' % (DataMeanTOT[HistPulserTOT1_index], DataStdevTOT[HistPulserTOT1_index], ValidTOTCnt[HistPulserTOT1_index])], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)

if nTOA_TOT_Processing == 0:
    # Plot (1,1)
    if PlotValidCnt == 0:
        exec("DataL = len(HitDataTOA%d)" % HistDelayTOA2)
        if DataL:
            hist_range = 10
            binlow = ( int(TOAmean[HistDelayTOA2_index])-hist_range ) * LSBest
            binhigh = ( int(TOAmean[HistDelayTOA2_index])+hist_range ) * LSBest
            hist_bin_list = np.arange(binlow, binhigh, LSBest)
            exec("ax4.hist(np.multiply(HitDataTOA%d,LSBest), bins = hist_bin_list, align = 'left', edgecolor = 'k', color = 'royalblue')" % HistDelayTOA2)
            #exec("ax4.set_xlim(left = np.min(np.multiply(HitDataTOA%d,LSBest))-10*LSBest, right = np.max(np.multiply(HitDataTOA%d,LSBest))+10*LSBest)" % (HistDelayTOA2, HistDelayTOA2))
            ax4.set_title('TOA Measurment for Programmable Delay = %d' % HistDelayTOA2, fontsize = 11)
            ax4.set_xlabel('TOA Measurement [ps]', fontsize = 10)
            ax4.set_ylabel('N of Measrements', fontsize = 10)
            ax4.legend(['Mean = %f ps \nStd. Dev. = %f ps \nN of Events = %d' % (TOAmean[HistDelayTOA2_index]*LSBest, TOAsigma[HistDelayTOA2_index]*LSBest, HitCnt[HistDelayTOA2_index])], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
    else:
        ax4.plot(Delay, HitCnt)
        ax4.grid(True)
        ax4.set_title('TOA Valid Counts VS Programmable Delay Value', fontsize = 11)
        ax4.set_xlabel('Programmable Delay Value', fontsize = 10)
        ax4.set_ylabel('Valid Measurements', fontsize = 10)
        ax4.set_xlim(left = np.min(Delay), right = np.max(Delay))
        ax4.set_ylim(bottom = 0, top = np.max(HitCnt)*1.1)
else:
    # Plot (1,1)
    if Plot_TOTf_lin == 0:
        exec("DataL = len(HitDataTOT%d)" % HistPulserTOT2)
        if DataL:
            exec("ax4.hist(HitDataTOT%d, bins = np.multiply(np.arange(512),LSB_TOTf_mean), align = 'left', edgecolor = 'k', color = 'royalblue')" % HistPulserTOT2)
            exec("ax4.set_xlim(left = np.min(HitDataTOT%d)-4*LSB_TOTf_mean, right = np.max(HitDataTOT%d)+4*LSB_TOTf_mean)" % (HistPulserTOT2, HistPulserTOT2))
            ax4.set_title('TOT Measurment for Pulser = %d' % HistPulserTOT2, fontsize = 11)
            ax4.set_xlabel('TOT Measurement [ps]', fontsize = 10)
            ax4.set_ylabel('N of Measrements', fontsize = 10)
            ax4.legend(['Mean = %f ps \nStd. Dev. = %f ps \nN of Events = %d' % (DataMeanTOT[HistPulserTOT2_index], DataStdevTOT[HistPulserTOT2_index], ValidTOTCnt[HistPulserTOT2_index])], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
    else:
        ax4.hist(HitDataTOTf_cumulative, bins = np.arange(9), edgecolor = 'k', color = 'royalblue')
        ax4.set_xlim(left = -1, right = 8)
        ax4.grid(True)
        ax4.set_title('TOT Fine Interpolation Linearity', fontsize = 11)
        ax4.set_xlabel('TOT Fine Code', fontsize = 10)
        ax4.set_ylabel('N of Measrements', fontsize = 10)

plt.subplots_adjust(hspace = 0.35, wspace = 0.2)
plt.show()

#################################################################

time.sleep(0.5)
# Close
top.stop()