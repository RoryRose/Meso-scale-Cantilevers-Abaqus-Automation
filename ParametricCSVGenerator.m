%% ParametricCSVGenerator

function WorkingDirectory_actual = ParametricCSVGenerator(NumCores)
%%
    question = 'Perform parametric analysis?';
    Quest_PA = questdlg(question,'MSCAA_main: Parametric Analysis','Yes','No','No');
    clear question

    % Need to make it load a .txt template file to use!
    filter = {'*.txt;*.py','Valid Template File Type (*.txt, *.py)'};
    [file_name,file_path] = uigetfile(filter,'Select variable template file to import:','MultiSelect','off');
    file_fullfile = fullfile(file_path,file_name);
    
    % This function I wrote converts the txt into a string array.
    Lines_1 = py2string(file_fullfile,'r');
    
    % This function I wrote extracts all of the variable names and variable
    % values from the string arrray.
    [array_var,array_val] = VarReader(Lines_1);
    
    % This allows the user to choose the number of cores to use.
    message0 = sprintf('Use X number of CPUs out of %d?',NumCores);
    NumCPUs = str2double(inputdlg(message0));
    if NumCPUs >= NumCores
        NumCPUs = NumCores-1;
    end
    
    % Finds the row in the string array which is the JobName row, and finds
    % its value.
    JobNameRow = strcmp(array_var,'JobName');
    JobName = array_val(JobNameRow);
    
    % Finds the row in the string array which is the ModelName row, and
    % finds its value.
    ModelNameRow = strcmp(array_var,'ModelName');
    ModelName = array_val(ModelNameRow);
    
    % This allows the user to choose the working directory that Matlab will
    % use to run that session.
    WorkingDirectory_actual = uigetdir('','Choose the folder that will be the working directory for ABAQUS');
    AbqFDir = sprintf('r"%s"',WorkingDirectory_actual); % This edits the above so it is formatted correctly.
    ODBName = string(replace(WorkingDirectory_actual,"\","/"));
    ODBName = join(["'",ODBName,"/","'"],''); % Same as above comment.
    
    switch Quest_PA
        case 'Yes'
            % The following case happens when the user wants to do
            % parametric analysis.
            ListOfVars = array_var; % List of variables
            
            % Below line is a list dialogue function, that gives the user
            % the option of the variables that they wish to make
            % parametric.
            [indx,~] = listdlg('ListString',ListOfVars,'PromptString','Select variables to change:','SelectionMode','multiple','Name','Parametric');
            
            NumOfTests = str2double(inputdlg('How many tests to perform?')); % This asks the user how many models they want to run.
            PreTable = nan(length(indx),NumOfTests); % Just preparing that variable.
            
            % The below goes through each of the variables that the user
            % selected to edit, and then it creates a linspace based on the
            % min values, max values, and the number of tests they chose to
            % do e.g. d1 min = 4, d1 max = 7, number of test = 4, then the
            % code will run 4 models, where each successive model will go
            % have a d1 value of 4, then 5, then 6, then 7.
            for i = 1:length(indx)
                message1 = sprintf('Enter minimum value for %s:',array_var(indx(i)));
                message2 = sprintf('Enter maximum value for %s:',array_var(indx(i)));
                prompt = {message1,message2};
                dlgtitle = 'Input';
                dims = [1 35];
                definput = {char(array_val(indx(i))),char(array_val(indx(i)))};
                answer = str2double(inputdlg(prompt,dlgtitle,dims,definput));
                PreTable(i,:) = linspace(answer(1),answer(2),NumOfTests);
            end
            
            StringPreTable = string(PreTable); % Strings the pretable above.
            Lines_1_alt = strings(length(array_var),1+NumOfTests); % Prepares string array.
            Lines_1_alt(:,1) = array_var(:); % Fills in the first column with all of the variable names.
            
            % The below goes through each model prepares it before adding
            % in the parametric values.
            for i = 1:NumOfTests
                % This is the original template data just repeated out.
                Lines_1_alt(:,i+1) = array_val(:);
                % The below two lines automatically alter the JobName and
                % ModelName values for each model to be run.
                Lines_1_alt(JobNameRow,i+1) = join(["'",strip(JobName,'both',"'"),"_",string(i),"'"],'')';
                Lines_1_alt(ModelNameRow,i+1) = join(["'",strip(ModelName,'both',"'"),"_",string(i),"'"],'')';
            end

            % This for loop goes through each of the rows for the variables
            % which the user selected to edit, and then changes the values
            % to what was chosen by the user.
            for i = 1:length(indx)
                fprintf('Working on for %s:\n',array_var(indx(i)));
                Lines_1_alt(indx(i),2:NumOfTests+1) = StringPreTable(i,:);
            end
            
            fprintf('%s: Changed input variables\n',mfilename);
        case 'No'
            fprintf('%s: Did not alter input variables\n',mfilename);
            Lines_1_alt = [array_var,array_val]; % Only one midel will be run, and it will be based on that given by the template.
    end
    
    % The below replaces the values for multiple variables which should
    % have the same value, but that is different from the initial template.
    Lines_1_alt = ReplaceRowValues(Lines_1_alt,array_var,'NumCPUs',NumCPUs);
    Lines_1_alt = ReplaceRowValues(Lines_1_alt,array_var,'AbqFDir',AbqFDir);
    Lines_1_alt = ReplaceRowValues(Lines_1_alt,array_var,'ODBName',ODBName);
    
    % The below saves the csv file in the user defined working directory
    % for ABAQUS to use.
    SaveFileName =  fullfile(WorkingDirectory_actual,'VariablesCSV.csv');
    writetable(table(Lines_1_alt), SaveFileName,'WriteVariableNames',0,'WriteRowNames',0,'QuoteStrings',0);
end
%%
function [array_var,array_val] = VarReader(InputStringArray)
    currVarNum = 1;
    for i = 1:length(InputStringArray)
        checkRow = char(InputStringArray(i));
        if checkRow(1) ~= '#'
            curr_row = split(InputStringArray(i),' ',2);
            array_var(currVarNum,1) = curr_row(1);
            array_val(currVarNum,1) = curr_row(3);
            currVarNum = currVarNum + 1;
        else
            fprintf('Row "%d" is detected as a comment...\n',i);
            continue
        end
    end
end

function LinesString = py2string(filename,permission)
    % Helped by the following URLs:
    % https://uk.mathworks.com/matlabcentral/answers/417112-how-to-write-from-a-python-file-to-another-python-script-modify-the-new-python-script-and-save-it-i
    % https://uk.mathworks.com/help/matlab/ref/feof.html
    FID = fopen(filename,permission);
    LinesString = strings(0,1);
    while ~feof(FID)
       LinesString(end+1,1) = fgetl(FID);
    end
    fclose(FID);
end

function string_array = ReplaceRowValues(string_array,array_var,varname,varvalue)
    rowA = strcmp(array_var,varname);
    string_array(rowA,2:end) = varvalue;
end