# Meso-scale-Cantilevers-Abaqus-Automation

## Introduction
This code works in conjunction with *ABAQUS* and with *ABAQUS2MATLAB* to allow basic parametric analysis of cantilever testing to be run via Matlab.
## Acknowledgements & IP
**Clear acknowledgement** of the use of this code, whether that be by using it for data analysis, or by the modification or merging of this code with another, would be very much appreciated as many hours have been put into writing this code. **Also**, following the **MIT license** agreement (contained within this repository) **is mandatory**.
Unless stated by comments within the code assume that the code was written by Rory Rose & Robert J Scales.
## How to Use
Some basic cantilever analyses have been created already, such as *standard static* to see the deflection of the cantilever under a known load.
However, this code works by effectively breaking up the macros which can be recorded in ABAQUS into different sections.
This breaking up allows editing of the:
 - ***User input variables***: This is the variables which the *cantilever design* and the *method* use. This is changed depending on what file the user selects **OR** the range of values the user inputs in the parametric stage.
 - ***Cantilever design***: This is advised to be created via the macro recording within ABAQUS, and this will generate the assembely of the model including meshing it. It is important to define useful sets when creating the cantilever. Change the values to those of the user input variables.
 - ***Method***: This stage is where loads, boundary conditions, and steps are defined. Field output and history output requests are also defined here. This can then be used to act on different cantilever models if the variable names are kept consisted between the model design stage and this stage.

The code then compiles these python codes (including the edited user *input variables*) into one python file, which is then executed via the system to ABAQUS.
Each intended job is not run, but is instead saved as a ***.inp*** file, which therefore saves operation time and is what is required by *ABAQUS2MATLAB* in order for it to analyse the data.

The results from *ABAQUS2MATLAB* are analysed differently by this code depending on the method; these are the ***post-processing*** functions.
Once the analysis is done, the code asks the user if they want the figures and output files to be automatically saved. 
