%% Meso-scale-Cantilevers-ABAQUS-Automation
% By Robert J Scales & Rory Rose
% Last update 15/11/2020

%% Checking Compatabilities
clear
clc

debugON = true;

fprintf('Running %s\n%s\n\n',mfilename,'Made by Robert J Scales & Rory Rose');

if ispc
    fprintf('%s is running on a Windows computer...\n\n',mfilename);
    % Code to run on Windows platform
elseif isunix
    % Code to run on Linux platform
    PopUp = helpdlg('Unfortunately Unix is currently not supported!');
    waitfor(PopUp);
    return
elseif ismac
    % Code to run on Mac platform
    PopUp = helpdlg('Unfortunately Mac is currently not supported!');
    waitfor(PopUp);
    return
else
    PopUp = helpdlg('Platform is not supported!');
    waitfor(PopUp);
    return
end

CodeMatlabVersion = 'R2020b';
ComputerMatlabVersion = sprintf('R%s',version('-release'));
str = '-'; %This is character vector, NOT a string
DashLine = repelem(str,100);
fprintf('Code was written with Matlab %s\nCurrent computer is running %s\n%s\n',CodeMatlabVersion,ComputerMatlabVersion,DashLine);

%% Questions

fprintf('%s: Started Questions section\n\n',mfilename);

question = 'Perform parametric analysis?';
Quest_PA = questdlg(question,'MSCAA_main: Parametric Analysis','Yes','No','No');
clear question

ListOfMethods = {'Standard Static','Calibration Static','Direct Dynamic','Resonant Frequency','Debug_MCAA_main'};
[indx,~] = listdlg('ListString',ListOfMethods,'PromptString','Select a method to perform:','SelectionMode','single','Name','Method Selection');

% The below checks to see if the user has selected an option
if isempty(indx) == false
    % If a valid option was selected the variable method is created which
    % is named after the chosen method.
    Method = ListOfMethods{indx};
else
    % The following occurs when no method is selected i.e. when cancelled
    % or exiting the dialogue box.
    PopUp = warndlg('User has not selected a method...');
    waitfor(PopUp);
    question = 'Restart code?';
    Quest_Restart = questdlg(question,'MSCAA_main: Restarting Code','Yes','No','Yes');
    clear question
    switch Quest_Restart
        case 'Yes'
            % This restarts this code
            run(mfilename);
            return
        otherwise
            % Just exits running this code
            return
    end
end

fprintf('%s: Completed Questions section\n%s\n',mfilename,DashLine);

%% Job Creating

fprintf('%s: Started Job Creating section\n\n',mfilename);

% x12 = '10';
% ve = '20';

% fid=fopen('Abaqus.inp','w');
% fprintf(fid,'%s','R punch_st');
% fprintf(fid,'%10.6f',x12);
% fprintf(fid,'%s','R punch_ve');
% fprintf(fid,'%10.4f\n',ve);
% fclose(fid);

% dos('abaqus job=job.inp');

% This prepares ABAQUS for the specific job based on what has been
% specified for the sample.
JobName = methodInitialise(Method);

switch Method
    case 'Standard Static'
        % This creates the job for Standard Static
        dos('abaqus cae noGUI=Create_Static_anal_job_and_BCs.py');
        
    case 'Calibration Static'
        % This creates the job for Calibration Static
        dos('abaqus cae noGUI=Static_calib_for_indent_pos.py');
        
    case 'Direct Dynamic'
        % This creates the job for Direct Dynamic
        dos('abaqus cae noGUI=Direct_Dynamic_job_and_BCs.py');
        
    case 'Resonant Frequency'
        % This creates the job for Direct Dynamic
        dos('abaqus cae noGUI=Eigenmode_Analysis_Job_and_BCs.py');
        
    case 'Debug_MCAA_main'
        fprintf('%s: Method Debug_MCAA_main was chosen\n\n',mfilename);
end

fprintf('%s: Completed Job Creating section\n%s\n',mfilename,DashLine);

%% Job Running

fprintf('%s: Starting Job Running section\n\n',mfilename);

% This will run the job for this method
CommandLineToRun = sprintf('abaqus job=%s',JobName);
if strcmp(Method,'Debug_MCAA_main') == false
    dos(CommandLineToRun);
else
    
end
fprintf('%s: Ran job = "%s"\n\n',mfilename,JobName);

fprintf('%s: Completed Job Running section\n%s\n',mfilename,DashLine);

%% Analysis

fprintf('%s: Starting Analysis section\n\n',mfilename);



fprintf('%s: Completed Analysis section\n%s\n',mfilename,DashLine);

fprintf('%s: Completed!!\n',mfilename);
%% Functions

function JobName = methodInitialise(Method)

        % Create InputVarMacro via VarCreator4ABAQUS function.
        JobName = VarCreator4ABAQUS();
        
        if strcmp(Method,'Debug_MCAA_main') == false
            % Runs the InputVarMacro.py to initialise user input variables.
            dos('abaqus cae noGUI=InputVarMacro.py');
            % Runs the script to generate the assembly etc. This is shared for
            % all methods.
            dos('abaqus cae noGUI=Create_JG_V2_Cantilever.py');
        end
        
end





