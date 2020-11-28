%% MSCAA_method_editor
% By Robert J Scales

function editedMethodFullFile = MSCAA_method_editor(method_fullfile,WorkingDirectory_actual)
%%
    fprintf('%s: Started\n',mfilename)

    MethodString = py2string(method_fullfile,'r');
%     Row2ChangeA = strfind(MethodString,'AbqFDir'); % Shows what column position(s) that word appears in
    Row2ChangeB = contains(MethodString,'AbqFDir');
    
    Row2Change = find(Row2ChangeB,1,'first');
    
    ActualRow = MethodString(Row2Change,:);
    path2use = strip(WorkingDirectory_actual,'right','\');
    EditedRow = replace(ActualRow,'C:\Users\trin3150\Documents\Abaqus\liltemp',path2use);
    
    MethodString_edited = MethodString;
    MethodString_edited(Row2Change,:) = EditedRow;
    
    
    SaveName = 'PythonScriptToRun';
    
    SaveNameTXT = sprintf('%s.txt',SaveName);
    TextFile = fullfile(WorkingDirectory_actual, SaveNameTXT);

    % Writes it as a .txt first
    writetable(table(MethodString_edited), TextFile,'WriteVariableNames',0,'WriteRowNames',0,'QuoteStrings',0);

    % Credit to the following URL for inspiring me.
    % This creates a copy of the .txt file but changes the extension to ".py".
    % https://uk.mathworks.com/matlabcentral/answers/514865-how-to-change-file-extension-via-matlab
    [tempDir, tempFile] = fileparts(TextFile);
    editedMethodFullFile = fullfile(tempDir, [tempFile, '.py']);
%     fprintf('tempDir = %s\n',tempDir);
%     fprintf('Length of TextFile = %d, and length of new file = %d\n',length(TextFile),length(editedMethodFullFile));
    copyfile(TextFile, editedMethodFullFile); 
    fclose('all');
    delete(string(TextFile));
    
    
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