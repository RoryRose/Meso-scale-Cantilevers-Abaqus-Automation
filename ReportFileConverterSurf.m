
% function outputmatrix = ReportFileConverterSurf

    [file, path] = uigetfile('Select the report file:');
    filename = fullfile(path,file);
    Lines_1 = py2string(filename,'r');
    Lines_2a = Lines_1(24:end);
    Lines_2 = replace(Lines_2a,'No Value','NaN');
    endline = find((Lines_2 == ''), 1, 'first');

    for i = 1:endline-1
        disp(i)
        current_row = Lines_2(i);
%         disp(current_row);
        Lines_3 = split(current_row,' ',2);
        curr_num = 1;
        for j = 1:length(Lines_3)
    %         disp(j);
            curr_Val = Lines_3(j); 
            if strcmp(curr_Val,"") == false
%                 disp(curr_Val)
                if curr_num == 1
                    curr_line = string(curr_Val);
                else
                    curr_line = horzcat(curr_line,curr_Val);
                end
                curr_num = curr_num+1;
            end
%             disp(curr_line)
        end

        if i == 1
            Lines_4 = join(curr_line);
        else
            Lines_4 = vertcat(Lines_4,join(curr_line));
        end

        Lines_5 = split(Lines_4,' ',2);
        Lines_6 = double(Lines_5);
    end

%% PostProcessing

clc
clearvars -except Lines_6
close all

Lines_7pre = Lines_6(~isnan(Lines_6(:,2)),:);
MissingData = Lines_7pre(isnan(Lines_7pre(:,6)),:);
% Lines_7 = Lines_7pre;
Lines_7 = Lines_7pre(~isnan(Lines_7pre(:,6)),:);


shp = alphaShape(Lines_7(:,3),Lines_7(:,4));
shp.Alpha = 1.50*10^-5;
inmask1 = inpolygon(Lines_7(:,3),Lines_7(:,4),shp.Points(:,1),shp.Points(:,2));


COOR1 = Lines_7(:,3);
COOR2 = Lines_7(:,4);
COOR3 = Lines_7(:,5);
SMises = Lines_7(:,6);
S11 = Lines_7(:,7);
S22 = Lines_7(:,8);
S33 = Lines_7(:,9);
S12 = Lines_7(:,10);
S13 = Lines_7(:,11);
S23 = Lines_7(:,12);

Quantity2Plot = S11;

MinXY = min(min(COOR1),min(COOR2));
MaxXY = max(max(COOR1),max(COOR2));


x = COOR1;
y = COOR2;
v = Quantity2Plot;

npts = length(x); % Number of points
% round((length(x)^0.5))

[~,IndXMax] = max(x);

ScatterORInt = 'Int'; % 'Int'

switch ScatterORInt
    case 'Int'
        % [xg,yg] = meshgrid(linspace(MinXY,MaxXY,100));
        [xg,yg] = meshgrid(linspace(min(x),max(x),600),linspace(min(y),max(y),600));
        F = scatteredInterpolant(x,y,v);
        vg = F(xg,yg);

        b = boundary(x,y);
        inmask = inpolygon(xg(:),yg(:), x(b),y(b));
        vg(~inmask) = nan;
        xg_new = xg(~inmask);
        yg_new = yg(~inmask);
        % MinXY = min(min(x),min(y));
        % MaxXY = max(max(x),max(y));
        % [xg,yg] = meshgrid(linspace(MinXY,MaxXY,300));
        % F = scatteredInterpolant(x,y,v);
        % vg = F(xg,yg);
        h = pcolor(xg,yg,vg);
        h.EdgeColor = 'none';
        c = colorbar;
        xlimvec = [min(xg(inmask)),max(xg(inmask))];
        ylimvec = [min(yg(inmask)),max(yg(inmask))];
        xlim(xlimvec);
        ylim(ylimvec);


        % dt = delaunayTriangulation(x,y);
        % [K,v] = convexHull(dt);
        % xp = x(K);
        % yp = y(K);
        % inmask = inpolygon(x(:),y(:), xp,yp);
        % v(~inmask) = nan;
        % % h = trisurf(dt.ConnectivityList,x,y,zeros(length(v),1),v);
        % h = trisurf(K,x,y,zeros(length(v),1),v);
        % h.FaceColor = 'interp';
        % % h.EdgeColor = 'none';
        % view(2)
        % colorbar
        hold on
        % plot(shp);
    otherwise
%         scatter(x,y,36,v,'filled');
        scatter(x,y,36,[0,0,0],'x');
        c = colorbar;
end

% c.Ticks = [linspace(round(min(v)),round(max(v)),10),0];

% plot(xg(1,:),vg(300,:));

caxis([round(min(vg(300,:))) round(max(vg(300,:)))])

% A = min(vg(300,:));
% B = min(v);

% end
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

%     Lines_4 = erase(Lines_3,"");
% %     Lines_4 = Lines_3(find(~isspace(Lines_3)));
%     Lines_4 = Lines_3;
% %     Lines_4(strcmp(Lines_3, ' ')) = [];
%     Lines_4(all(strcmp(Lines_4,""),2),:) = [];
%     Lines_4 = rmmissing(Lines_4, 'MinNumMissing', size(Lines_4,2));
%     Lines_5(i) = Lines_3;