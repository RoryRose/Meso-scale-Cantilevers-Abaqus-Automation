%% VarCreator4ABAQUS
% By Robert James Scales Nov 2020
% This code is designed to take a .py code that has variables used in the
% macros in ABAQUS models, and then it can change the values of these
% variables and produces a .py file to be run by Matlab for ABAQUS to use.
%
% You can run this code by itself. OR you can enter a valid value for
% DefaultOption, which can take on the following values:
% - You can leave it blank and the code will ask you what you want.
% - Type 'Default' to use the  values stored in this function.
% - Type 'Excel' to load a filled in Excel spreadsheet template made
%   by RJ Scales (called VariablesExcel).
% - Type 'Do Nothing' to leave the original Python file

function VarCreator4ABAQUS(DefaultOption)
    %% Loading variable list python file
    % This gets a UI interface to load the variables list python file,
    % which can be run just by itself.
    [file,path] = uigetfile('*.py');
    % This combines the filename and path name into one string.
    readFile = fullfile(path,file);

    disp('VarCreator4ABAQUS: Fullfile name achieved...')
    %% Main Body
    
    % dbstack() describes what functions are being called.
    ST = dbstack();
    if length(ST) > 1
        % The below happens if this is being called from another function.
        if nargin == 0
            % This happens if the number of input arguments is zero.
            PopUpAns = questdlg('Want to load an Excel or use default values?','Settings','Excel','Default','Do Nothing','Default');
        else
            PopUpAns = DefaultOption;
        end
    else
        % The below happens if this function is being run by itself.
        PopUp = helpdlg('Function is detected as running by itself.');
        waitfor(PopUp);
        PopUpAns = questdlg('Want to load an Excel or use default values?','Settings','Excel','Default','Do Nothing','Default');
    end

    % The switch allows different answers to have different consequences.
    switch PopUpAns
        case 'Default'
            % The below are the default variable names and values.
            d1 = 0.3e-03; %length of cantilever between arc and end block
            d2 = 0.6e-03; %lenth of end block
            d3 = 0.6e-03; %length of cantilever between built in and free end
            d4 = 0.4E-03; %width of disk arc
            h1 = 0.2e-03; %width of cantilever
            h2 = 1.0e-03; %width of free end
            r1 = 0.9e-03; %radius of cantilever arc
            r2 = 2.0e-03; %radius of disc
            t =  125e-06; %thickness of sheet
            E = 200e+09; %material elastic modulus
            dens = 8000; %material density
            PRat = 0.29; %material poissons ratio
            EncName = 'encastre'; %name of encarcarate BC set
            TopSetName = 'Cant_top_set'; %name of set for top of cantilever surface
            CentFreeName = 'center_of_free_end'; %name of set for center of free end (nanoindent location)
            WholePrt = 'Whole-Part'; %name of set for the whole part
            MeshSeedSize = 2e-05; %size of mesh seed
            SName = 'nanoindenter'; %name of loading step
            ForceName = 'nanoindent';%name of nanoindenter load
            JobName = 'nanoindent'; %name of job
            IndentLocName = 'nanoindenter'; %name of the set (not created here) for the nanoindenter position
            ModelName = 'Model-1'; %name of the model
            PrtName = 'Part-1'; %Name of Part
            InstName = 'Inst-1'; %Name of Instance
            
            %only for direct dynamic analysis%
            MinFreq = 19000; %minimum frequency for the frequency step
            MaxFreq = 20000; %maximum frequency for the frequency step
            VertDisp = 1e-05; %vertical displacement of the built in end
            
            %only for static cantilever calibration%
            SName2 = 'disk'; %name of loading step  with indent nearer the disk
            SName3 = 'end'; %name of loading step with indent nearer the end
            DiskFreeName = 'near_disk'; %name of set for the indent nearer the disk side of the tongue (quater of the way along and on center line)
            EndFreeName = 'near_end'; %name ofset for the indent nearer the end side of the tongue (three quaters of the way along and on center line)
            
            % This generates a list which will be used by the code to replace
            % the variable values in the .py code.
            variablesList = [QC(d1);QC(d2);QC(d3);QC(d4);QC(h1);QC(h2)
                QC(r1);QC(r2);QC(t);QC(E);QC(dens);QC(PRat);QC(EncName);
                QC(TopSetName);QC(CentFreeName);QC(WholePrt);
                QC(MeshSeedSize);QC(SName);QC(ForceName);QC(JobName);
                QC(IndentLocName);QC(ModelName);QC(PrtName);QC(InstName);
                QC(MinFreq);QC(MaxFreq);QC(VertDisp);QC(SName2);
                QC(SName3);QC(DiskFreeName);QC(EndFreeName)];
            
                newCode = tableWrite(readFile,variablesList);
                SaveAsPy(newCode,path,'InputVarMacro');

        case 'Excel'
            disp('Working on loading an Excel file');
            % Finds the name and path of the Excel file.
            [Excel_file,Excel_path] = uigetfile('*.xlsx');
            Excel_readFile = fullfile(Excel_path,Excel_file);
            variablesList = importfile(Excel_readFile);
            newCode = tableWrite(readFile,variablesList);
            SaveAsPy(newCode,path,'InputVarMacro');
        
        case 'Do Nothing'
            % This just copies the original file but renames it.
            disp('Option "Do Nothing" was chosen, hence macro will be copied and resaved as "InputVarMacro.py"...')
            copyfile(readFile, fullfile(path,'InputVarMacro.py')); 
            fclose('all');
            disp('VarCreator4ABAQUS: Saved as .py')    
            
        otherwise
            PopUp = errordlg('The variable "DefaultOption" must be either empty (i.e. ""), OR to preselect option it must be either "Excel" or "Default"!');
            waitfor(PopUp);
            return
    end
    
    
disp('VarCreator4ABAQUS: Complete!')


end

%% Other Functions

% This is a quick compose function that formats the default variables in
% this function into the correct format.
function output = QC(value)
    IsNum = isa(value,'numeric');
    IsString = isa(value,'string') || isa(value,'char');
    if IsNum == true
        output =string(value);
    elseif IsString == true
        output = compose("'%s'",value);
    else
        errordlg('Invalid value entered of %s',string(value));
    end
end

% This code works to generate a table that is the same as the initially
% loaded in python file but with the values changed to what is on
% variablesList.
function newCode = tableWrite(readFile,variablesList)
    debugON = false;

    % Helped by the following URL to read the .py file.
    % from https://uk.mathworks.com/matlabcentral/answers/417112-how-to-write-from-a-python-file-to-another-python-script-modify-the-new-python-script-and-save-it-i
    fid = fopen(readFile, 'r');
    line = fgetl(fid);
    linesString = strings(0,1);
    while(ischar(line))
       linesString(end+1,1) = line;
       line = fgetl(fid);
    end
    fclose(fid);
    disp('VarCreator4ABAQUS: File Accessed and Read...')

    linesString_NEW = linesString;

    % The below looks for rows that aren't columns, and by seperating out
    % the strings by using spaces as delimiters, it then replaces the third
    % value (i.e. d = 3, would be 3) with the value given in variablesList. 
    currVarNum = 1;
    for i = 1:length(linesString)
        checkRow = char(linesString(i));
        if checkRow(1) ~= '#'
            curr_row = split(linesString(i),' ',2);
            original3rd = curr_row(3);
            curr_row(3) = variablesList(currVarNum);
            new3rd = curr_row(3);
            curr_row = join(curr_row, ' ');
            linesString_NEW(i) = curr_row;
            if debugON == true
                fprintf('Replacing "%s" with "%s"\n',original3rd,new3rd);
                fprintf('New line of code reads\n %s\n\n',curr_row);
            end
            currVarNum = currVarNum + 1;
        else
            if debugON == true
                fprintf('Row "%d" is detected as a comment...\n\n',i);
            end
            continue
        end
    end
    clear curr_row row_num i currVarNum

    % This will be used to generate the .txt file in the next section
    newCode = table(linesString_NEW);

    clear linesString_NEW

    disp('VarCreator4ABAQUS: Table written...')
end

% The job of this function is to save the table as a txt and then converts
% it effectively into a python file; naming it as SaveName and placing it
% in the same folder.
function SaveAsPy(newCode,path,SaveName)

    SaveNameTXT = sprintf('%s.txt',SaveName);
    % Writes it as a .txt first
    writetable(newCode, SaveNameTXT,'WriteVariableNames',0,'WriteRowNames',0,'QuoteStrings',0);

    % Credit to the following URL for inspiring me.
    % This creates a copy of the .txt file but changes the extension to ".py".
    % https://uk.mathworks.com/matlabcentral/answers/514865-how-to-change-file-extension-via-matlab
    TextFile = fullfile(path, SaveNameTXT);
    [tempDir, tempFile] = fileparts(TextFile); 
    copyfile(TextFile, fullfile(tempDir, [tempFile, '.py'])); 
    fclose('all');
    delete(string(SaveNameTXT));
    disp('VarCreator4ABAQUS: Saved as .py')
end

%% Interesting stuff

%
%     p = mfilename('fullpath');
%     disp('p = ');
%     disp(p);


% The following could be used for multiple file generation
% maybe.
%     SheetNames = sheetnames(Excel_readFile);
%     for u = 1:length(SheetNames)
%         variablesList = importfile(Excel_readFile);
%         newCode = tableWrite(readFile,variablesList);
%         SaveAsPy(newCode,path,'InputVarMacro');
%     end
