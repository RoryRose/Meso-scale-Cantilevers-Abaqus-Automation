%% Meso-scale-Cantilevers-ABAQUS-Automation
% By Robert J Scales & Rory Rose
% Last update 15/11/2020

%% Checking Compatabilities
clear
clc

CodeWD = cd;

% debugON = true;

fprintf('Running %s\n%s\n\n',mfilename,'Made by Robert J Scales & Rory Rose');

if ispc || isunix
    % Code to run on Windows platform or Code to run on Linux platform
    fprintf('%s is running on a compatible OS...\n\n',mfilename);
elseif ismac
    % Code to run on Mac platform
    PopUp = helpdlg('Unfortunately Mac OS is currently not supported!');
    waitfor(PopUp);
    return
else
    PopUp = helpdlg('This operating system is not supported!');
    waitfor(PopUp);
    return
end

feature('numcores');
NumCores = feature('numcores');
fprintf('\n');

CodeMatlabVersion = 'R2020b';
ComputerMatlabVersion = sprintf('R%s',version('-release'));
str = '-'; %This is character vector, NOT a string
DashLine = repelem(str,100);
fprintf('Code was written with Matlab %s\nCurrent computer is running %s\n%s\n',CodeMatlabVersion,ComputerMatlabVersion,DashLine);

%% Settings
fprintf('%s: Started Settings section\n\n',mfilename);

question = 'Display results in ABAQUS whilst generating model?';
Quest_GUI = questdlg(question,'MSCAA_main: GUI ON/OFF','Yes','No','No');
clear question

switch Quest_GUI
    case 'Yes'
        GUI_ON = 'script';
    otherwise
        GUI_ON = 'noGUI';
end

question = 'Display results in ABAQUS whilst generating model?';
Quest_Int = questdlg(question,'MSCAA_main: Interactive ON/OFF','Yes','No','No');
clear question

if scrmp(Quest_Int,'Yes') == true
    IntactiveVal = 'interactive';
else
    IntactiveVal = '';
end

fprintf('%s: Completed Settings section\n%s\n',mfilename,DashLine);

%% Main Bulk
fprintf('%s: Started PythonScriptCombiner section\n\n',mfilename);

MSCAA_PythonScriptCombiner

% Dir_work_ABAQUS = uigetdir(CodeWD,'Select the working directory for ABAQUS');




fprintf('%s: Completed!!\n',mfilename);
%% Functions


