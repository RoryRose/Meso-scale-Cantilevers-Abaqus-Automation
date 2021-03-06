%% MSCAA_PythonScriptCombiner
% Written by Robert James Scales 16/11/2020

function MSCAA_PythonScriptCombiner
%%
    fprintf('%s: Started\n',mfilename);
    path = cd;
    
    fprintf('%s: Started Questions section\n\n',mfilename);

    question = 'Perform parametric analysis?';
    Quest_PA = questdlg(question,'MSCAA_main: Parametric Analysis','Yes','No','No');
    clear question
    
%% Importing Script_0
    Lines_0 = py2string('MSCAA_Script_0_Startup.py','r');
    
%% Importing Script_1
    Lines_1 = py2string('MSCAA_Script_1_Variables.py','r');
    [array_var,array_val] = VarReader(Lines_1);
    switch Quest_PA
        case 'Yes'
            ListOfVars = array_var;
            [indx,~] = listdlg('ListString',ListOfVars,'PromptString','Select variables to change:','SelectionMode','multiple','Name','Parametric');
            NumOfTests = str2double(inputdlg('How many tests to perform?'));
            PreTable = nan(length(indx),NumOfTests);
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
            StringPreTable = string(PreTable);
            Lines_1_alt = strings(length(array_var),1+NumOfTests);
            Lines_1_alt(:,1) = array_var(:);
            for i = 1:NumOfTests
                Lines_1_alt(:,i+1) = array_val(:);
            end

            for i = 1:length(indx)
                fprintf('Working on for %s:\n',array_var(indx(i)));
                Lines_1_alt(indx(i),2:NumOfTests+1) = StringPreTable(i,:);
            end
%             Lines_1 = MSCAA_PythonScript1Altering(Lines_1);
            fprintf('%s: Changed input variables\n',mfilename);
        case 'No'
            fprintf('%s: Did not alter input variables\n',mfilename);
            array_var_and_val = [array_var,array_val];
    end
    
    Lines_1_table = table(Lines_1_alt);
    
    
    SaveName = 'VariablesCSVMatlab';
    SaveFileName = sprintf('%s.csv',SaveName);
    % Writes it as a .txt first
    writetable(Lines_1_table, SaveFileName,'WriteVariableNames',0,'WriteRowNames',0,'QuoteStrings',0);

    % Credit to the following URL for inspiring me.
    % This creates a copy of the .txt file but changes the extension to ".py".
    % https://uk.mathworks.com/matlabcentral/answers/514865-how-to-change-file-extension-via-matlab
    TextFile = fullfile(path, SaveFileName);
    [tempDir, tempFile] = fileparts(TextFile); 
    copyfile(TextFile, fullfile(tempDir, [tempFile, '.py'])); 
    fclose('all');
    delete(string(SaveFileName));
    fprintf('VarCreator4ABAQUS: Saved as %s.py\n',tempFile);

%% Importing Script_2
    Lines_2 = py2string('MSCAA_Script_2_GenModel__JG_V2_Cantilever.py','r');

%% Importing Script_3
    Lines_3 = py2string('MSCAA_Script_3_Method__Standard_Static.py','r');
    
%% Importing Script_4
    Lines_4 = py2string('MSCAA_Script_4_Saving.py','r');
    
%% Combine All Scripts
    Lines_All = vertcat(Lines_0,Lines_1,Lines_2,Lines_3,Lines_4);
    
%% Convert Lines_All into .txt and then into .py
    SaveName = 'InputVarMacroTest';

    % This will be used to generate the .txt file.
    Lines_Table = table(Lines_All);
    
    SaveNameTXT = sprintf('%s.txt',SaveName);
    % Writes it as a .txt first
    writetable(Lines_Table, SaveNameTXT,'WriteVariableNames',0,'WriteRowNames',0,'QuoteStrings',0);

    % This creates a copy of the .txt file but changes the extension to ".py".
    % Credit to the following URL for inspiring me.
    % https://uk.mathworks.com/matlabcentral/answers/514865-how-to-change-file-extension-via-matlab
    TextFile = fullfile(path, SaveNameTXT);
    [tempDir, tempFile] = fileparts(TextFile); 
    copyfile(TextFile, fullfile(tempDir, [tempFile, '.py'])); 
    fclose('all');
    delete(string(SaveNameTXT));
    fprintf('%s: Saved as %s.py\n',mfilename,tempFile);

end

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

% FID_0 = fopen('MSCAA_Script_0_Startup.py','r');
% %     line = fgetl(FID_0);
% Lines_0 = strings(0,1);
% while ~feof(FID_0)
% %        Lines_0(end+1,1) = line;
%    Lines_0(end+1,1) = fgetl(FID_0);
% end
% fclose(FID_0);