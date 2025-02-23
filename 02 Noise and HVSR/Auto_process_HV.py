#!/usr/bin/env python

###################
#
# This script automatically performs an HVSR calculation for all available filenames in a folder and generates .hv output files
# KOEN VAN NOTEN
# ROYAL OBSERVATORY OF BELGIUM
# please cite Van Noten et al. 2022 when using as the initial products for this code where developed in that paper
#
# Van Noten, K., Devleeschouwer, X., Goffin, C., Meyvis, B., Molron, J., Debacker, T.N. & Lecocq, T. 2022. 
# Brussels’ bedrock paleorelief from borehole-controlled powerlaws linking polarised H/V resonance frequencies 
# and sediment thickness. Journal of Seismology 26, 35-55. https://doi.org/10.1007/s10950-021-10039-8
#
###################

import os
from obspy import read
import pandas as pd
import datetime
import subprocess
from datetime import date, timedelta
import numpy as np
import traceback


# Linux
#geopsy_exe = "geopsy-hv"
# Windows - locate the Geopsypack.win64-3.4.2 folder
#geopsy_exe = 'C:/Users/koenvn/geopsypack-win64-3.4.2/bin/geopsy-hv.exe'



def get_paramString():
    """
    Creation of an empty ParamString that can be filled in with optional parameters. 
    This creates a .log file, similar as when Geopsy is used manually
    """
    ## We create a default PARAM multiline string with the static components for whole processing 
    ## and formatters for variables
    paramsString = '''PARAMETERS_VERSION=1    \nFROM_TIME_TYPE=Absolute\nFROM_TIME_TEXT={tStart}\nTO_TIME_TYPE=Absolute\nTO_TIME_TEXT={tEnd}\nREFERENCE=\nCOMMON_TIME_WINDOWS=false\nWINDOW_LENGTH_TYPE=Exactly\nWINDOW_MIN_LENGTH(s)={winLen}\nWINDOW_MAX_LENGTH(s)={winLen}\nWINDOW_MAX_COUNT=0\nWINDOW_MAXIMUM_PRIME_FACTOR=11\nBAD_SAMPLE_TOLERANCE (s)=0\nBAD_SAMPLE_GAP (s)=0\nWINDOW_OVERLAP (%)={overlap}\nBAD_SAMPLE_THRESHOLD_TYPE={threshold}\nBAD_SAMPLE_THRESHOLD_VALUE (%)={threshold_pct}\nANTI-TRIGGERING_ON_RAW_SIGNAL (y/n)=n\nANTI-TRIGGERING_ON_FILTERED_SIGNAL (y/n)=n\nSEISMIC_EVENT_TRIGGER (y/n)=n\nSEISMIC_EVENT_DELAY (s)=-0.1\nWINDOW_TYPE=Tukey\nWINDOW_REVERSED=n\nWINDOW_ALPHA=0.1\nSMOOTHING_METHOD=Function\nSMOOTHING_WIDTH_TYPE=Log\nSMOOTHING_WIDTH={KO}\nSMOOTHING_SCALE_TYPE=Log\nSMOOTHING_WINDOW_TYPE=KonnoOhmachi\nSMOOTHING_WINDOW_REVERSED=n\nMINIMUM_FREQUENCY={minFreq}\nMAXIMUM_FREQUENCY={maxFreq}\nSCALE_TYPE_FREQUENCY=Log\nSTEP_TYPE_FREQUENCY=Count\nSAMPLES_NUMBER_FREQUENCY={N_samples}\n#STEP_FREQUENCY=1.00231\nHIGH_PASS_FREQUENCY=0\nHORIZONTAL_COMPONENTS={horizontals}\nHORIZONTAL_AZIMUTH={azimuth}\nROTATION_STEP={rotSteps}\nFREQUENCY_WINDOW_REJECTION_MINIMUM_FREQUENCY={rej_min_freq}\nFREQUENCY_WINDOW_REJECTION_MAXIMUM_FREQUENCY={rej_max_freq}\nFREQUENCY_WINDOW_REJECTION_STDDEV_FACTOR={rej_stdev}\nFREQUENCY_WINDOW_REJECTION_MAXIMUM_ITERATIONS={rej_it}\n'''
    return paramsString

def run_HV(wf):
    ## Grab the station info
    st = read(wf)
    tr = st[0]
    start = tr.stats.starttime
    end = tr.stats.endtime
    station = '%s_%s'%(tr.stats.network, tr.stats.station)
    print('station: %s'%station)

    delta = end-start
    print("start: %s"%start)
    print("end: %s"%end) 
    print("We get %s .hv files of %ss length out of stream"%(int(delta/process_len), process_len))


    for i in np.arange(start, end, process_len):
            time = i
            print(time)
            tStart = '%s%02d%02d%02d%02d%#05.2f'%(time.year, time.month, time.day, time.hour, time.minute, time.second)
            tStart_hv = '%s%02d%02d%02d%02d%#02d'%(time.year, time.month, time.day, time.hour, time.minute, time.second)
            endtime = time + process_len
            tEnd = '%s%02d%02d%02d%02d%#05.2f'%(endtime.year, endtime.month, endtime.day, endtime.hour, endtime.minute, endtime.second)

            # get the empty auto-paramString
            paramsString = get_paramString()

            # adapt an auto-PARAM file with the given parameters so that for each processing loop the same param is used
            with open('geopsy-hv-auto.params', 'w') as f:
                f.write(paramsString.format(
                    # Select start and end time from waveform
                    tStart=tStart,
                    # Select end time from waveform
                    tEnd=tEnd,
                    # Adapt the parameters of previously chosen parameters 
                    threshold=threshold,
                    threshold_pct=threshold_pct,
                    KO=KO,
                    winLen=time_window_len,
                    overlap=win_overlap,
                    N_samples=N_samples,
                    minFreq=min_freq,
                    maxFreq=max_freq,
                    horizontals=horizontals_method,
                    azimuth=azimuth,
                    rotSteps=rotation_steps,
                    rej_min_freq=rej_min_freq, 
                    rej_max_freq=rej_max_freq, 
                    rej_stdev=rej_stdev,
                    rej_it = rej_it
                    ))

            ### Make a folder for each station output
            os.makedirs(output_folder+node_ID, exist_ok=True)
            out_folder = ''.join(output_folder+node_ID)

            ### Run geopsy for each step in the loop
            #!{''.join(geopsy_exe)} -hv {''.join(wf)} -param geopsy-hv-auto.params -o {''.join(output_folder+node_ID)}
            subprocess.call(['geopsy-hv', '-hv', wf, '-param', 'geopsy-hv-auto.params', '-o', os.path.join(output_folder,node_ID)])

            ### Rename the .hv output file and the .log to save a unique files for each processed process_len
            ### saving the .log files is useful as these can be loaded in Geopsy to manually check the processed data 
            print(node_ID, station)
            os.renames(os.path.join(output_folder, '{0}/{1}.hv'.format(node_ID, station)), os.path.join(output_folder, '{0}/{1}.{2}.hv'.format(node_ID, station, tStart_hv)))
            os.renames(os.path.join(output_folder, '{0}/{1}.log'.format(node_ID, station)), os.path.join(output_folder, '{0}/{1}.{2}.log'.format(node_ID, station, tStart_hv)))

            # if want_rotation is selected, also the HV rotate module will be executed and stored in the outfolder  
            
            if want_rotation:

                # run the geopsy rotation
                subprocess.call(['geopsy-hv', '-rotate', wf, '-param', 'geopsy-hv-auto.params', '-o', os.path.join(output_folder,node_ID)])

                ### Rename the .hv.grid output file
                os.renames(os.path.join(output_folder, '{0}/{1}.hv'.format(node_ID, station)), os.path.join(output_folder, '{0}/{1}.{2}.hv.grid'.format(node_ID, station, tStart_hv)))
            
            print('**********************************')


########################
##### Main program  ####
########################

# import OptionParser class 
# from optparse module.
from optparse import OptionParser

# create a OptionParser
parser = OptionParser()
     
### param details
parser.add_option('-p', '--process_len', type = 'int',
                      default = 3600, dest = 'process_len',
                      help = "Overall processing lengths - time for which we compute the total HV-curve")
parser.add_option("-w", "--time_window_len", type == 'int', 
                  default = 60, dest = 'time_window_len',
                  help = "window length for each HV curve")
parser.add_option("-t", "--threshold_pct", type == 'float', 
                  default = 0.5, dest = 'threshold_pct',
                  help = "window length for each HV curve")
parser.add_option("-o", "--win_overlap", type == 'int', default = 50,
                  dest = 'win_overlap',
                      help = "% overlapping windows")
parser.add_option("-k", "--KO", type == 'float', default = 0.2, dest = 'KO',
                      help = "Konno-Omachi Smoothing")
parser.add_option("-l", "--min_freq", type == 'float', default = 0.2, dest = 'min_freq',
                      help = "lower frequency bound")
parser.add_option("-u", "--max_freq", type == 'float', default = 50, dest = 'max_freq',
                      help = "upper frequency bound")
parser.add_option("-n", "--N_samples", type == 'int', default = 500, dest = 'N_samples',
                      help = "Nr of SAMPLES_NUMBER_FREQUENCY={S_N_FREQ}")
parser.add_option("-r", "--want_rotation", default = False, action="store_true", dest = 'want_rotation',
                      help = "True if you want run the HV rotate module ")
parser.add_option("-d", "--rotation_steps", type == 'int', default = 10, dest = 'rotation_steps',
                      help = "degree of rotation steps in the rotate module")

(options, args) = parser.parse_args()

# overall processing lengths (time for which we compute the total HV-curve)
#process_len = 3600. # [s] standard 1 hour
process_len = options.process_len # [s] standard 1 hour

# window length for each HV curve
#time_window_len = 360. # [s] standard 60 or 120s
time_window_len = options.time_window_len # [s] standard 60 or 120s

#overlapping windows
#win_overlap = 50
win_overlap = options.win_overlap

#threshold_pct = 0.4
threshold_pct = options.threshold_pct

#Smoothing (in digits)
#KO = 0.2
KO = options.KO

# lower frequency bound
#min_freq = 0.1 # [Hz]
min_freq = options.min_freq

# upper frequency bound
#max_freq = 100 # [Hz]
max_freq = options.max_freq 

# Nr of SAMPLES_NUMBER_FREQUENCY={S_N_FREQ}
#N_samples = 2000
N_samples = options.N_samples

# in case you want run the HV rotate module (see exercise 4)
#want_rotation = False # True, False
want_rotation = options.want_rotation # True, False

#rotation_steps = 10 # [degree]
rotation_steps = options.rotation_steps


# fixed params
threshold = 'RelativeSampleThreshold'
# how to calculate horizontals (Squared, Energy, Azimuth, Geometric)
horizontals_method = 'Squared' # standard 'Squared'
##HORIZONTAL_AZIMUTH is used only when HORIZONTAL_COMPONENTS== 'Azimuth'
azimuth = 0

# Using the Cox et al. 2020 filtering 
#FREQUENCY_WINDOW_REJECTION_MINIMUM_FREQUENCY
rej_min_freq = 0.5
#FREQUENCY_WINDOW_REJECTION_MAXIMUM_FREQUENCY
rej_max_freq = 50
#FREQUENCY_WINDOW_REJECTION_STDDEV_FACTOR
rej_stdev = 1.8
#FREQUENCY_WINDOW_REJECTION_MAXIMUM_ITERATIONS
rej_it = 500


#################### loop

### for smartSolo node data
def read_files(directory):   
    files = []
    # Loop through the files in the directory
    for filename in os.listdir(directory):
        # Split the filename to get the base name and component
        node = filename.split('.')[0]
        basefile = filename.rsplit('.', 2)[0]
        files.append(basefile)
    
    files = np.unique(files)
    return files

# for FDSN data
def read_files(directory):   
    files = []
    # Loop through the files in the directory
    for filename in os.listdir(directory):
        try:
            # Split the filename to get the base name and component
            l = list(filename)
            l[13] = '*'
            basefile = ''.join(l)
            #basefile = filename.rsplit('.', 2)[0]
            #filename[14] = '*'
            #basefile = filename
            print(filename)
            files.append(basefile)
        except Exception:
            print(l)
            traceback.print_exc()
            continue
    
    files = np.unique(files)
    return files


current_folder = os.getcwd()
#current_folder = '/mnt/LargeMEM/SKIENCE25/DATA/MSEED'

# Specify the directory containing the waveform files
#directory = os.path.join(current_folder, 'Raw_Data')
directory = 'Raw_Data'

# Give outputfolder where to save the .hv files
output_folder = os.path.join(current_folder, 'Analysed_Skience25/')
files = read_files(directory)

for file in files:
    node_ID = str(os.path.split(file)).split('.')[1]
    wf = os.path.join(directory, file)
    print(wf)

    try:
        run_HV(wf)
    except:
        continue

print('Job Done')
