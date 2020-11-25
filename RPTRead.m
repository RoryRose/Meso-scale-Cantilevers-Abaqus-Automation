function [d,t,dline,tline]=RPTRead(fname)
% FUNCTION:
% %         Read data from *.rpt file which includes text and data
% %         information.Content example is listed as following:
% % **********************************************************************
% % *                            NODE LOCATION REPORT                    *
% % **********************************************************************
% % Node Locations
% % Node ID   Coord 1 Value   Coord 2 Value   Coord 3 Value          Reference CID
% %       3        0.000000        0.000000        0.000000   (Global) Rectangular
% %       4       -0.621540       24.922939       -0.000000   (Global) Rectangular
% %       .....
% % Node Locations
% % Node ID           Analysis CID
% %       3   (Global) Rectangular
% %       4   (Global) Rectangular
% %      .....
% INPUT:
%       fname--File name
% OUTPUT:
%            d:nX4 sized data array:
%              1st col stores node id;
%              2nd col stores x coordination; 
%              3rd col stores y coordination; 
%              4th col stores z coordination;
%           t:Text cell array which stores header information and comment
%             information line by line;
%       dline: records data line number of the file;
%       tline: records line number of text array.
% USEAGE:
%       [d,t,dline,tline]=RPTRead('x0.rpt')
% Author: Li Haixing; Email:windchaser_lhx@163.com
% check number and type of arguments
if nargin < 1
    error('Function requires one input argument');
elseif ~ischar(fname)
    error('Input argument must be a string representing a filename');
end

% Open file
fid = fopen(fname);
if fid==-1
    error('File not found or permission denied.');
end
% 

%Initialize data array, text array, dline and tline
d = [];
t = { };
dline=0;
tline=0;
% 

% Process
while ~feof(fid)
    s=fgets(fid);
    [data, ncols, errmsg, nxtindex]= sscanf(s, '%f');
    if ~isempty(data)
        dline = dline+1;
        eval(['d','(:,',num2str(dline),')','=data']);
        sx = fgets(fid);
        [data2, ncols, errmsg, nxtindex]= sscanf(sx, '%f');
        if ~isempty(data2)
           off=-1*length(sx);
           fseek(fid,off,'cof');
        else
                while ~feof(fid)
                       s=fgets(fid);  
                       tline=tline+1;
                       eval(['t','{',num2str(tline),'}','=s']);                       
                end
                break;
        end
    else
        tline=tline+1;
        eval(['t','{',num2str(tline),'}','=s']);
    end
end

d=d';
t=t';
fclose(fid);
end
