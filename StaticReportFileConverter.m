% function outputmatrix = ReportFileConverterSurf

%% Settings
% clc
% clear
% close all
ScatterORInt = 'Int'; % 'Int'
PlotTF = true;

%% Reading Data
[file, path] = uigetfile('Select the report file:','MultiSelect','on');
%%
thickness = [];
if isa(file,'char') == true
    file = cellstr(file);
end
data=[];
outPutArray = nan(length(file),1);
NameArray = transpose(string(file));
filestotest={'B10-S1','B10-S2','B4-S1 ','B4-S2 ','C7-S1 ','C7-S2 '};
FileNumidx=ismember(extractBetween(file,"Model-","-t"),filestotest{1},'rows')';

for FileNum = 1:length(file)

    filename = fullfile(path,file{FileNum});
    Lines_1 = py2string(filename,'r');
    Lines_2a = Lines_1(24:end);
    Lines_2 = replace(Lines_2a,'No Value','NaN');
    endline = find((Lines_2 == ''), 1, 'last');

    for i = 1:endline-1
        current_row = Lines_2(i);
        Lines_3 = split(current_row,' ',2);
        curr_num = 1;
        for j = 1:length(Lines_3)
            curr_Val = Lines_3(j); 
            if strcmp(curr_Val,"") == false
                if curr_num == 1
                    curr_line = string(curr_Val);
                else
                    curr_line = horzcat(curr_line,curr_Val);
                end
                curr_num = curr_num+1;
            end
        end

        if i == 1
            Lines_4 = join(curr_line);
        else
            Lines_4 = vertcat(Lines_4,join(curr_line));
        end
        try
            Lines_5 = split(Lines_4(3),' ',2);
            Lines_6 = double(Lines_5(2));
        catch
            Lines_5 = [];
            Lines_6 = [];
            warning('error');
        end
    end
    data(FileNum,2)=1/Lines_6;
    fprintf('%d Done!\n',FileNum);
    data(FileNum,1)=FileNum;
    thickness(FileNum) = str2double(cell2mat(extractBetween(file{FileNum},"t-",".rpt")));
end
%%

%data = sortrows(data,1);
figure
subplot(1,2,1);
scatter(data(:,1),data(:,2),'r')
hold on
yline(mean(data(:,2)),'b')
xlabel('sample number')
ylabel('beam modulus(N/m)')
subplot(1,2,2);
hist(data(:,2))
xlabel('beam modulus(N/m)');
ylabel('counts');
figure
scatter(thickness,data(:,2));
xlabel('thickness(m)')
ylabel('beam modulus(N/m)')



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