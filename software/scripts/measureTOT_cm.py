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
NofIterationsTOT = 20  # <= Number of Iterations for each Delay value
DelayStep = 9.5582  # <= Estimate of the Programmable Delay Step in ps (measured on 10JULY2019)
LSB_TOTc = 160    # <= Estimate of TOT coarse LSB in ps
riseEdge = 2400
fallEdge = 3000

TOTf_hist = True
TOTc_hist = True
Plot_TOTf_lin = 1
PlotValidCnt = 1

TOT_f_Calibration_SAVE_file = 'TestData/TOT_fine_calibration2.txt'  # <= Path to the File where TOT Fine-Interpolation Calibration Data are Saved

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
#from setASICconfig_v2B6 import *                               ##
from setASICconfig_v2B2 import *                               ##
from setASICconfig_v2B3 import *                               ##
from setASICconfig_v2B7 import *                               ##
from setASICconfig_v2B8 import *                               ##
                                                               ##
#################################################################


def acquire_data(top, pulser, PulserRange, using_TZ_TOT): 
    pixel_stream = feb.PixelReader()    
    pyrogue.streamTap(top.dataStream[0], pixel_stream) # Assuming only 1 FPGA
    pixel_data = {
        'allTOTdata' : [],
        'HitDataTOTf': [],
        'HitDataTOTc': [],
        'HitDataTOTc_int1': []
    }
    

    for pulse_value in PulserRange:
        print('Scanning Pulse value of ' + str(pulse_value))
        pulser.set(pulse_value)

        for pulse_iteration in range(NofIterationsTOT):
            if (asicVersion == 1):
                top.Fpga[0].Asic.LegacyV1AsicCalPulseStart()
                time.sleep(0.001)
            else:
                top.Fpga[0].Asic.CalPulse.Start()
                time.sleep(0.001)

        if using_TZ_TOT:
            pixel_data['HitDataTOTf'].append( pixel_stream.HitDataTOTf_tz.copy() )
            pixel_data['HitDataTOTc'].append( pixel_stream.HitDataTOTc_tz.copy() )
            pixel_data['HitDataTOTc_int1'].append( pixel_stream.HitDataTOTc_int1_tz.copy() )
        else:
            pixel_data['allTOTdata'].append( pixel_stream.HitDataTOT.copy() )
            pixel_data['HitDataTOTf'].append( pixel_stream.HitDataTOTf_vpa.copy() )
            pixel_data['HitDataTOTc'].append( pixel_stream.HitDataTOTc_vpa.copy() )
            pixel_data['HitDataTOTc_int1'].append( pixel_stream.HitDataTOTc_int1_vpa.copy() )

        while pixel_stream.count < NofIterationsTOT: pass
        pixel_stream.clear()

    return pixel_data
#################################################################


def parse_arguments():
    parser = argparse.ArgumentParser()
    
    # Convert str to bool
    argBool = lambda s: s.lower() in ['true', 't', 'yes', '1']
    
    #default parameters
    pixel_number = 4
    DAC_Vth = 320
    Qinj = 13 #10fc
    config_file = 'config/config_v2B6_noPAprobe.yml'
    pulserMin = 0
    pulserMax = 20
    pulserStep = 1
    using_TZ_tot = False # <= TOT TDC Processing Selection (0 = VPA TOT, 1 = TZ TOT)
    outFile = 'TestData/TOTmeasurement'
    
    
    # Add arguments
    parser.add_argument( "--ip", nargs ='+', required = False, default = ['192.168.1.10'], help = "List of IP addresses")
    parser.add_argument( "--board", type = int, required = False, default = 7,help = "Choose board")
    parser.add_argument( "--useExt", type = bool, required = False, default = False,help = "Use external trigger")
    parser.add_argument("--cfg", type = str, required = False, default = config_file, help = "config file")
    parser.add_argument("--ch", type = int, required = False, default = pixel_number, help = "channel")
    parser.add_argument("--Q", type = int, required = False, default = Qinj, help = "injected charge DAC")
    parser.add_argument("--DAC", type = int, required = False, default = DAC_Vth, help = "DAC vth")
    parser.add_argument("--useTZ", type = bool, required = False, default = using_TZ_tot, help = "TOT TDC Processing")
    parser.add_argument("--pulserMin",  type = int, required = False, default = pulserMin,  help = "pulser start")
    parser.add_argument("--pulserMax",  type = int, required = False, default = pulserMax,  help = "pulser stop")
    parser.add_argument("--pulserStep", type = int, required = False, default = pulserStep, help = "pulser step")
    parser.add_argument("--out", type = str, required = False, default = outFile, help = "output file")

    # Get the arguments
    args = parser.parse_args()
    return args
#################################################################


def measureTOT( argsip,
      board,
      useExt,
      Configuration_LOAD_file,
      pixel_number,
      Qinj,
      DAC,
      using_TZ_TOT,
      pulserMin,
      pulserMax,
      pulserStep,
      outFile):

    args = parse_arguments()
    PulserRange = range( pulserMin, pulserMax, pulserStep )
    
    # Setup root class
    top = feb.Top(ip= argsip)
    
    # Load the default YAML file
    print('Loading {Configuration_LOAD_file} Configuration File...')
    top.LoadConfig(arg = Configuration_LOAD_file)
    
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
    if board == 7:
      set_fpga_for_custom_config_B7(top,pixel_number)
    elif board == 8:
      set_fpga_for_custom_config_B8(top,pixel_number)
    elif board == 3:
      set_fpga_for_custom_config_B3(top,pixel_number)
    elif board == 2:
      set_fpga_for_custom_config_B2(top,pixel_number)

    top.Fpga[0].Asic.SlowControl.DAC10bit.set(DAC)
    top.Fpga[0].Asic.SlowControl.dac_pulser.set(Qinj)
    top.Fpga[0].Asic.Gpio.DlyCalPulseReset.set(fallEdge)

    if useExt: #scan with external trigger
        top.Fpga[0].Asic.SlowControl.disable_pa[pixel_number].set(0x1)
        top.Fpga[0].Asic.SlowControl.ON_discri[pixel_number].set(0x0)
        top.Fpga[0].Asic.SlowControl.EN_hyst[pixel_number].set(0x1)
        top.Fpga[0].Asic.SlowControl.EN_trig_ext[pixel_number].set(0x1)
        top.Fpga[0].Asic.SlowControl.ON_Ctest[pixel_number].set(0x0)
        pixel_data = acquire_data(top, top.Fpga[0].Asic.Gpio.DlyCalPulseSet, PulserRange, using_TZ_TOT)

    #scan changing Qinj
    else:
        top.Fpga[0].Asic.Gpio.DlyCalPulseSet.set(riseEdge)
        pixel_data = acquire_data(top, top.Fpga[0].Asic.SlowControl.dac_pulser, PulserRange, using_TZ_TOT)
    
    #################################################################
    # TOT Fine Interpolator Calibration
    HitDataTOTf_cumulative = []
    for HitDataTOT in pixel_data['HitDataTOTf']: HitDataTOTf_cumulative += HitDataTOT
    
    TOTf_value_range = 16
    TOTf_bin_width = np.zeros(TOTf_value_range)
    for TOTf_value in range(TOTf_value_range):
        TOTf_bin_width[TOTf_value] = HitDataTOTf_cumulative.count(TOTf_value)
    TOTf_bin_width = TOTf_bin_width/sum(TOTf_bin_width)
    
    TOTf_bin = np.zeros(TOTf_value_range+2)
    for TOTf_value in range(1,TOTf_value_range+1):
        TOTf_bin[TOTf_value] = HitDataTOTf_cumulative.count(TOTf_value-1)
    
    LSB_TOTf_mean = np.mean( TOTf_bin[TOTf_bin != 0]  )/sum(TOTf_bin)
    
    TOTf_bin = (TOTf_bin[1:18]/2 + np.cumsum(TOTf_bin)[0:17])/sum(TOTf_bin)
    TOTf_bin[16] = LSB_TOTf_mean
    
    print('TOT Fine Interpolator Bin-Widths:')
    print(TOTf_bin_width*2*LSB_TOTc)
    print('Average TOT LSB = %f ps' % (LSB_TOTf_mean*2*LSB_TOTc))
    np.savetxt(TOT_f_Calibration_SAVE_file,TOTf_bin)
    
    #################################################################
    # Data Processing TOT
    ValidTOTCnt = []
    DataMeanTOT = np.zeros( len(PulserRange) )
    DataStdevTOT = np.zeros( len(PulserRange) )

    HitDataTOT_list = []

    for pulser_index, pulser_value in enumerate(PulserRange):
        print('Processing Data for Pulser = %d...' % pulser_value)

        HitDataTOTf = np.asarray( pixel_data['HitDataTOTf'][pulser_index] )
        HitDataTOTc = np.asarray( pixel_data['HitDataTOTc'][pulser_index] )
        HitDataTOTc_int1 = np.asarray( pixel_data['HitDataTOTc_int1'][pulser_index] )
        ValidTOTCnt.append(len(HitDataTOTf))
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
        HitDataTOT = []
        if len(HitDataTOTf) > 0:
            if IntFVa == 1:
                HitDataTOT = list((np.asarray(HitDataTOTc_int1)*2 + 1 - np.asarray(list(map(lambda x: TOTf_bin[x], np.asarray(HitDataTOTf, dtype=np.int))))*2)*LSB_TOTc)
                HitDataTOT = list(HitDataTOT + np.asarray(list(map(calibration_correction, HitDataTOTf, list(map(lambda x: x&1, np.asarray(HitDataTOTc))))))*LSB_TOTc)

                #for f, c, int1 in zip(HitDataTOTf, HitDataTOTc, HitDataTOTc_int1):
                #    pre_correction = 2 * ( int1*2+1-TOTf_bin[f] ) * c
                #    if f > 3 and (c&1) == 0: correction = 2
                #    elif f == 0 and (c&1) == 1: correction = -TOTf_bin[0]*2
                #    else: correction = 0
                #    HitDataTOT.append(pre_correction + correction*LSB_TOTc)
            else:
                HitDataTOT = list( (1 + HitDataTOTc - HitDataTOTf/4) * LSB_TOTc )
    
            DataMeanTOT[pulser_index] = np.mean(HitDataTOT, dtype=np.float64)
            DataStdevTOT[pulser_index] = math.sqrt(math.pow(np.std(HitDataTOT, dtype=np.float64),2) + math.pow(LSB_TOTf_mean,2)/12)
        HitDataTOT_list.append(HitDataTOT)
    
    # Average Std. Dev. Calculation; Points with no data (i.e. Std.Dev.= 0) are ignored
    MeanDataStdevTOT = np.mean( DataStdevTOT[DataStdevTOT!=0] )
   
   #################################################################
    # Save Data
    #################################################################
    #outFile = 'TestData/TOTmeasurement'
    
    if os.path.exists(outFile+'.txt'):
      ts = '_'+str(int(time.time()))
      outFile = outFile+ts
    
    ff = open(outFile+'.txt','a')
    if useExt:
        ff.write('TOT measurement with ext trigger ---- '+str(time.ctime())+'\n')
    else:
        ff.write('TOT measurement with charge scan ---- '+str(time.ctime())+'\n')
    ff.write('Pixel = '+str(pixel_number)+'\n')
    ff.write('config file = '+Configuration_LOAD_file+'\n')
    ff.write('NofIterations = '+str(NofIterationsTOT)+'\n')
    #ff.write('cmd_pulser = '+str(Qinj)+'\n')
    #ff.write('Delay DAC = '+str(DelayValue)+'\n')
    ff.write('LSBest = '+str(LSB_TOTc)+'\n')
    #ff.write('Threshold = '+str(DACvalue)+'\n')
    ff.write('N hits = '+str(ValidTOTCnt)+'\n')
    ff.write('Number of events = '+str(len(HitDataTOT))+'\n')
    ff.write('mean value = '+str(DataMeanTOT)+'\n')
    ff.write('sigma = '+str(DataStdevTOT)+'\n')
    ff.write('Pulse width   TOT   TOTc   TOTf'+'\n')
    for ipuls, pulser in enumerate(PulserRange):
      pulser = pulser-fallEdge
      for itot in range(len(pixel_data['HitDataTOTc'][ipuls])):
        ff.write(str(pulser)+' '+str(pixel_data['allTOTdata'][ipuls][itot])+' '+str(pixel_data['HitDataTOTc'][ipuls][itot])+' '+str(pixel_data['HitDataTOTf'][ipuls][itot])+'\n')
    #ff.write('TOAvalues = '+str(HitDataTOT)+'\n')
    ff.close()
    
    print('Saved file '+outFile)


    #################################################################
    # Plot Data
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows = 2, ncols = 2, figsize=(16,7))
    
    # Plot (0,0) ; top left
    ax1.plot(PulserRange, DataMeanTOT)
    ax1.grid(True)
    ax1.set_title('TOT Measurment VS Injected Charge', fontsize = 11)
    ax1.set_xlabel('Pulser DAC Value', fontsize = 10)
    ax1.set_ylabel('Mean Value [ps]', fontsize = 10)
    ax1.set_xlim(left = PulserRange.start, right = PulserRange.stop)
    ax1.set_ylim(bottom = 0, top = np.max(DataMeanTOT)*1.1)
    
    # Plot (0,1) ; top right
    if PlotValidCnt == 0:
        ax2.scatter(PulserRange, DataStdevTOT)
        ax2.grid(True)
        ax2.set_title('TOT Jitter VS Injected Charge', fontsize = 11)
        ax2.set_xlabel('Pulser DAC Value', fontsize = 10)
        ax2.set_ylabel('Std. Dev. [ps]', fontsize = 10)
        ax2.legend(['Average Std. Dev. = %f ps' % MeanDataStdevTOT], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
        ax2.set_xlim(left = PulserRange.start, right = PulserRange.stop)
        ax2.set_ylim(bottom = 0, top = np.max(DataStdevTOT)*1.1)
    else:
        ax2.plot(PulserRange, ValidTOTCnt)
        ax2.grid(True)
        ax2.set_title('TOT Valid Counts VS Injected Charge', fontsize = 11)
        ax2.set_xlabel('Pulser DAC Value', fontsize = 10)
        ax2.set_ylabel('Valid Measurements', fontsize = 10)
        ax2.set_xlim(left = PulserRange.start, right = PulserRange.stop)
        ax2.set_ylim(bottom = 0, top = np.max(ValidTOTCnt)*1.1)
    
    # Plot (1,0)
    
    TOT_index_to_plot = -1
    for pulse_index, pulse_value in enumerate(PulserRange): #find a good delay value to plot
        #I'd say having 80% of hits come back is good enough to plot
        if ValidTOTCnt[pulse_index] > NofIterationsTOT * 0.8:
            TOT_index_to_plot = pulse_index
            break

    HitDataTOTf = pixel_data['HitDataTOTf'][TOT_index_to_plot]
    HitDataTOTc = pixel_data['HitDataTOTc'][TOT_index_to_plot]
    HitDataTOT = HitDataTOT_list[TOT_index_to_plot]
    
    if TOT_index_to_plot != -1:
        if TOTf_hist:
            ax3.hist(HitDataTOTf, bins = np.arange(9), align = 'left', edgecolor = 'k', color = 'royalblue')
            ax3.set_xlim(left = -1, right = 8)
        elif TOTc_hist:
            ax3.hist(HitDataTOTc, bins = np.arange(129), align = 'left', edgecolor = 'k', color = 'royalblue')
            ax3.set_xlim(left = -1, right = 128)
        elif len(HitDataTOT) > 1:
            ax3.hist(HitDataTOT, bins = np.multiply(np.arange(512),LSB_TOTf_mean), align = 'left', edgecolor = 'k', color = 'royalblue')
            ax3.set_xlim(left = np.min(HitDataTOT)-10*LSB_TOTf_mean, right = np.max(HitDataTOT)+10*LSB_TOTf_mean)
        ax3.set_title('TOT Measurment for Pulser = %d' % TOT_index_to_plot, fontsize = 11)
        ax3.set_xlabel('TOT Measurement [ps]', fontsize = 10)
        ax3.legend(['Mean = %f ps \nStd. Dev. = %f ps \nN of Events = %d' % (DataMeanTOT[TOT_index_to_plot], DataStdevTOT[TOT_index_to_plot], ValidTOTCnt[TOT_index_to_plot])], loc = 'upper right', fontsize = 9, markerfirst = False, markerscale = 0, handlelength = 0)
        ax3.set_ylabel('N of Measrements', fontsize = 10)
    
    # Plot (1,1)
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
#################################################################


if __name__ == "__main__":
    args = parse_arguments()
    print(args)

    measureTOT(args.ip, args.board, args.useExt, args.cfg, args.ch, args.Q, args.DAC, args.useTZ, args.pulserMin, args.pulserMax, args.pulserStep, args.out)