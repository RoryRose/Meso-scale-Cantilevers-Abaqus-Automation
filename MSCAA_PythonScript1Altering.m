%% MSCAA_PythonScript1Altering
% By Robert James Scales Nov 2020
% This code is designed ...

function OutputStringArray = MSCAA_PythonScript1Altering(InputStringArray,variablesList)
%%
    debugON = false;

    % The below looks for rows that aren't columns, and by seperating out
    % the strings by using spaces as delimiters, it then replaces the third
    % value (i.e. d = 3, would be 3) with the value given in variablesList. 
    currVarNum = 1;
    for i = 1:length(InputStringArray)
        checkRow = char(InputStringArray(i));
        if checkRow(1) ~= '#'
            curr_row = split(InputStringArray(i),' ',2);
            original3rd = curr_row(3);
            curr_row(3) = variablesList(currVarNum);
            new3rd = curr_row(3);
            curr_row = join(curr_row, ' ');
            OutputStringArray(i) = curr_row;
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

    fprintf('MSCAA_PythonScript1Altering: Complete!\n\n')
end
