clc
Lines_1 = py2string('C:\Users\rober\Documents\GitHub\Meso-scale-Cantilevers-Abaqus-Automation\Example Rpt files\Direct_Dynamicstress-dist.rpt','r');
Lines_2 = Lines_1(24:end);
Lines_5 = Lines_2;
for i = 1:length(Lines_2)
    disp(i)
    current_row = Lines_2(i);
    disp(current_row);
    Lines_3 = split(current_row,' ',2);
    for j = 1:length(Lines_3)
        disp(j);
        if isstring(Lines_3(j))
            disp('Is string')
            if strcmp(Lines_3(j),"")
                disp('Is empty')
            end
        end
        disp(Lines_3(j));
    end
    Lines_4 = erase(Lines_3,"");
%     Lines_4 = Lines_3(find(~isspace(Lines_3)));
    Lines_4 = Lines_3;
%     Lines_4(strcmp(Lines_3, ' ')) = [];
    Lines_4(all(strcmp(Lines_4,""),2),:) = [];
    Lines_4 = rmmissing(Lines_4, 'MinNumMissing', size(Lines_4,2));
    Lines_5(i) = Lines_3;
end
% RPTRead('C:\Users\rober\Documents\GitHub\Meso-scale-Cantilevers-Abaqus-Automation\Example Rpt files\Direct_Dynamicstress-dist.rpt');
%%
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