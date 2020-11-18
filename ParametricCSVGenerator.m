%% ParametricCSVGenerator

function ParametricCSVGenerator(NumCores)
%%
    question = 'Perform parametric analysis?';
    Quest_PA = questdlg(question,'MSCAA_main: Parametric Analysis','Yes','No','No');
    clear question

    % Need to make it load a .txt template file to use!
    Lines_1 = py2string('Variable-List-txt.txt','r');
    [array_var,array_val] = VarReader(Lines_1);
    
    message0 = sprintf('Use X number of CPUs out of %d?',NumCores);
    NumCPUs = str2double(inputdlg(message0));
    if NumCPUs >= NumCores
        NumCPUs = NumCores-1;
    end
    
    JobNameRow = strcmp(array_var,'JobName');
    JobName = array_val(JobNameRow);
    
    ModelNameRow = strcmp(array_var,'ModelName');
    ModelName = array_val(ModelNameRow);
    
    WorkingDirectory_actual = uigetdir();
    AbqFDir = sprintf('r"%s"',WorkingDirectory_actual);
%     AbqFDir = join(["'",AbqFDir,"'"],'');
    ODBName = string(replace(WorkingDirectory_actual,"\","/"));
    ODBName = join(["'",ODBName,"/","'"],'');
    
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
                Lines_1_alt(JobNameRow,i+1) = join(["'",strip(JobName,'both',"'"),"_",string(i),"'"],'')';
                Lines_1_alt(ModelNameRow,i+1) = join(["'",strip(ModelName,'both',"'"),"_",string(i),"'"],'')';
            end

            for i = 1:length(indx)
                fprintf('Working on for %s:\n',array_var(indx(i)));
                Lines_1_alt(indx(i),2:NumOfTests+1) = StringPreTable(i,:);
            end
%             Lines_1 = MSCAA_PythonScript1Altering(Lines_1);
            fprintf('%s: Changed input variables\n',mfilename);
        case 'No'
            fprintf('%s: Did not alter input variables\n',mfilename);
            Lines_1_alt = [array_var,array_val];
    end
    
    Lines_1_alt = ReplaceRowValues(Lines_1_alt,array_var,'NumCPUs',NumCPUs);
    Lines_1_alt = ReplaceRowValues(Lines_1_alt,array_var,'AbqFDir',AbqFDir);
    Lines_1_alt = ReplaceRowValues(Lines_1_alt,array_var,'ODBName',ODBName);
%     rowA = strcmp(array_var,'NumCPUs');
%     Lines_1_alt(rowA,2:end) = NumCPUs;
    
    Lines_1_table = table(Lines_1_alt);
    
    SaveName = 'VariablesCSVMatlab';
    SaveFileName = sprintf('%s.csv',SaveName);
    writetable(Lines_1_table, SaveFileName,'WriteVariableNames',0,'WriteRowNames',0,'QuoteStrings',0);
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