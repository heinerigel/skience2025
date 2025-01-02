# skience2025

Welcome!

This is the github Project for the 2025 Skience Winter School. Training material for the lectures and practices is provided here.

https://www.skience.de/2025


## Setup of Conda Environment for Skience24

[Miniconda/Anaconda3](https://docs.conda.io/en/latest/miniconda.html) has to be installed for this to work!

1) Download the [__skience25.yaml__](https://raw.githubusercontent.com/heinerigel/skience2024/main/skience24.yaml) file from this repository! This file specifies all required packages for the environment. Warning: make sure the content of the file is correct and not raw html!

2) Using the Anaconda Prompt (or your favorite console if it works): use conda to create an environment: 
  
   ` conda env create -f <path_to_yaml_file> `

3) After this terminated successfully, you should be able to list the environment: 
   
   ` conda env list `
   
   and to activate it using: 
   
   ` conda activate skience25 `

   When activated, your command line should show:
   
   ` (skience25) $ `  
   
4) Test the environment using: 
   
   (skience25) $ ` obspy-runtests --report`
   
   (skience24) $ ` msnoise utils test `
   

5) Clone the git repository

    in the console, in a folder of your choice (change directory with "cd"), activate the environment and run:
   
    (skience25) $ ` git clone https://github.com/heinerigel/skience2025.git `

If you have issues with the setup, please share the error messages on Mattermost -> Channel "Installation - Software Issues" !



To eventually delete the environment again type (after the workshop, of course):

    ` conda env remove --name skience25 `
