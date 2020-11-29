%% MSCAA_method_editor
% By Robert J Scales

function editedMethodFullFile = MSCAA_method_editor(method_fullfile,WorkingDirectory_actual)
%%
    fprintf('%s: Started\n',mfilename)

    MethodString = py2string(method_fullfile,'r'); % The below function converts the method python macro file into a string array.
    
    Row2Change = find(contains(MethodString,'AbqFDir'),1,'first'); % This produces a logic array of what lines contain 'AbqFDir' abd then it selects the row index of the first line it appears in!
    
    ActualRow = MethodString(Row2Change,:); % This selects the data actually in the first line in which 'AbqFDir' appears.
    path2use = strip(WorkingDirectory_actual,'right','\'); % This is the string which will replace the one that Rory typically uses in his python macro scripts.
    EditedRow = replace(ActualRow,'C:\Users\trin3150\Documents\Abaqus\liltemp',path2use); % This replaces the string to the new string.
    
    MethodString_edited = MethodString;
    MethodString_edited(Row2Change,:) = EditedRow; % This and the above line achieve just creating a copy of the initial string array but changing the appropriate line only.
    
    % This is the full location and name for which the txt file will be
    % saved under.
    TextFile = fullfile(WorkingDirectory_actual, 'PythonScriptToRun.txt');

    % Saves it as a .txt first
    writetable(table(MethodString_edited), TextFile,'WriteVariableNames',0,'WriteRowNames',0,'QuoteStrings',0);

    % Credit to the following URL for inspiring me.
    % This creates a copy of the .txt file but changes the extension to ".py".
    % https://uk.mathworks.com/matlabcentral/answers/514865-how-to-change-file-extension-via-matlab
    [tempDir, tempFile] = fileparts(TextFile);
    editedMethodFullFile = fullfile(tempDir, [tempFile, '.py']); % This is the name for which the edited file will be saved under.
%     fprintf('Length of TextFile = %d, and length of new file = %d\n',length(TextFile),length(editedMethodFullFile));
    copyfile(TextFile, editedMethodFullFile);  % This copies that '.txt' file but resaves it as a '.py' file.
    fclose('all'); % Closes all potentially open txt/py files.
    delete(string(TextFile)); % Deletes that txt file that it copied from.
    
    
    fprintf('%s: Saved as %s.py\n',mfilename,tempFile)
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