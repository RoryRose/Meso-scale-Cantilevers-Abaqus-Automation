%% Meso-scale-Cantilevers-ABAQUS-Automation
% By Robert J Scales & Rory Rose
% Last update 15/11/2020

%% Checking Compatabilities
clear % Clears all variables in workspace
clc % Clears the command window

CodeWD = cd; % This is the current working directory

fprintf('Running %s\n%s\n\n',mfilename,'Made by Robert J Scales & Rory Rose');
pause(1);

% The following evaluates what operating system is being used.
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

% This shows how many cores the current computer has.
feature('numcores');
NumCores = feature('numcores');
fprintf('\n');

% This shows how out of date your current version of MATLAB is compared to
% when this code was written.
CodeMatlabVersion = 'R2020b';
ComputerMatlabVersion = sprintf('R%s',version('-release'));
str = '-'; %This is character vector, NOT a string
DashLine = repelem(str,100); % This dashed line string is for aesthetics
fprintf('Code was written with Matlab %s\nCurrent computer is running %s\n%s\n',CodeMatlabVersion,ComputerMatlabVersion,DashLine);
pause(1);
%% Settings
fprintf('%s: Started Settings section\n\n',mfilename);

% User selecting an option for how to execute the python macro.
question = 'Have ABAQUS open whilst running script?';
Quest_GUI = questdlg(question,'MSCAA_main: GUI ON/OFF','Yes','No','No');
clear question

% This changes the answer that will be used by the system command.
switch Quest_GUI
    case 'Yes'
        GUI_ON = 'script';
    otherwise
        GUI_ON = 'noGUI';
end

% User selecting an option for how to execute the python macro.
question = 'Have log file whilst generating model?';
Quest_Int = questdlg(question,'MSCAA_main: Interactive ON/OFF','Yes','No','No');
clear question

% This changes the answer that will be used by the system command.
if strcmp(Quest_Int,'Yes') == true
    IntactiveVal = 'interactive';
else
    IntactiveVal = '';
end

fprintf('%s: Completed Settings section\n%s\n',mfilename,DashLine);
pause(1);
%% Main Bulk
fprintf('%s: Started Main Section\n\n',mfilename);

% This is a function I have written that generates the CSV file to be run.
WorkingDirectory_actual = ParametricCSVGenerator(NumCores);

% This is for selecting the method that should be run.
filter = {'*.py','Valid Method File Type (*.py)'};
[method_name,method_path] = uigetfile(filter,'Select method python script to run:','MultiSelect','off');
method_fullfile = fullfile(method_path,method_name);

% This function uses that selected method but changes the AbqFDir variable
% to the value chosen by the user earlier "WorkingDirectory_actual".
editedMethodFullFile = MSCAA_method_editor(method_fullfile,WorkingDirectory_actual);

% This is the string that will be the command run by the computer.
cmd2run = sprintf('abaqus cae %s=%s %s',GUI_ON,editedMethodFullFile,IntactiveVal);

fprintf('%s: Executing system command\n',mfilename);
system(cmd2run); % This line executes the command on both Unix and Windows supposedly.
% e.g. dos('abaqus cae script=Z:\RobScales\GitHub\Meso-scale-Cantilevers-Abaqus-Automation-Dev\Test_Frankens\Franken_Calib_Static.py');

pause(1);
fprintf('%s: Completed!!\n',mfilename);
%% Functions


