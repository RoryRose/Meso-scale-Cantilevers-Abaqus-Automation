filename = 'nanoindent_calib';
pathname = 'C:\Users\trin3150\Documents\Abaqus\liltemp';
Create_inp_file
%% Rory's Functions
function Create_inp_file()
%This is a hack of the Abaqus2Matlab GUI code for creating .inp files for
%analysis which bypasses the GUI and just creates a copied .inp file with
%updated format to be run by abaqus
Load_input_button_Callback
Button_write_input_Callback
end
%% Abaqus2Matlab functions (some small changes made)

%%load input%%
function Load_input_button_Callback()
% hObject    handle to Load_input_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global pathname filename all_elset all_nset Selected_vars clear_lines all_STEP
%open window to select input file
%[filename, pathname] = uigetfile({'*.inp'}, 'Select Abaqus Input File');
if ~filename
    warning('Please load an input file')
    return
end
%read input file
[all_elset,all_nset,all_STEP,StdExp,Selected_vars,clear_lines]=...
    read_input([pathname filename]);
all_elset=['ALL', all_elset];
all_nset=['ALL', all_nset];
end

% Executes if the button WRITE TO INPUT is pressed.
function Button_write_input_Callback()
% hObject    handle to Button_write_input (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global pathname filename clear_lines current_folder Selected_vars

current_directory=pwd;
h = waitbar(0,'Please wait...');

try
    if strcmp(current_directory(end-13:end),'A2M_GUI_Output')
        cd ('..')
    end
catch
end

input_file=[pathname filename];
if isempty(pathname)
    warning('Please select an input file')
    return
end
cd(pathname(1:end-1))
mkdir A2M_GUI_Output
fileattrib A2M_GUI_Output -w
current_folder=pwd;

filename_new=regexprep(filename(1:end-4),'_','');
filename_new=regexprep(filename_new,'\W','');
filename_new=regexprep(filename_new,'(','');
filename_new=regexprep(filename_new,')','');
FID = fopen([pathname filename],'r');
if FID<0
    error('Cannot open file')
end
Data = textscan(FID, '%s', 'delimiter', '\n', 'whitespace', '');
CStr = Data{1};
fclose(FID);
% Delete comments
IndexC = strfind(CStr,'**');
if ~isempty(IndexC)
    CStr(~cellfun('isempty', IndexC))=[];
end
% Delete empty lines
CStr(cellfun('isempty', CStr))=[];
% Delete output options
CStr(clear_lines)=[];
[ NEW_Index_steps ] = Obtain_Index_step( CStr );
waitbar(10/100);

DATA_Input=CStr(~cellfun('isempty',CStr));
FID = fopen([current_folder '\A2M_GUI_Output\' filename_new '_A2M.inp'],'w');
if FID<0
    error('Cannot open file')
end


[num_steps,~]=size(NEW_Index_steps);
for a=(num_steps:-1:1)
    DATA_Input=[DATA_Input(1:NEW_Index_steps(a,2)-1); Selected_vars{a}(:); DATA_Input(NEW_Index_steps(a,2):end)];
end
waitbar(20/100);
fprintf(FID,'%s \r\n',DATA_Input{:,1});
waitbar(1);
try
    close(h)
catch
end
fclose(FID);
end
function [all_elset,all_nset,all_steps,StdExp,previous_vars,clear_lines]=read_input(input)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

h = waitbar(0,'Please wait...');


%% Load the contents of the Abaqus input file
FID = fopen(input,'r');
if FID<0
    error('Cannot open Abaqus input file')
end
Data = textscan(FID,'%s','delimiter','\n','whitespace','');
fclose(FID);
waitbar(10 / 100)
%% Preprocess the Data cell
CStr_ = Data{1};
% Delete whitespaces
CStr_ = regexprep(CStr_,'\s','');
% Delete tabs
CStr_ = regexprep(CStr_,'\t','');
% Delete formfeeds
CStr_ = regexprep(CStr_,'\f','');
% Delete linefeeds
CStr_ = regexprep(CStr_,'\n','');
% Delete carriage returns
CStr_ = regexprep(CStr_,'\r','');
% Delete vertical tabs
CStr_ = regexprep(CStr_,'\v','');
% Delete comments
IndexC = strfind(CStr_,'**');
CStr_(~cellfun('isempty', IndexC))=[];
% Delete empty lines
CStr_(cellfun('isempty', CStr_))=[];
% Convert to lowercase characters
CStr = lower(CStr_);

%% Find PART definitions
IndexC = strfind(CStr,'*part');
IndexS = find(~cellfun('isempty', IndexC));
IndexC = strfind(CStr,'*endpart');
IndexE = find(~cellfun('isempty', IndexC));
partdef=false;
if ~isempty(IndexS)
    if numel(IndexS) ~= numel(IndexE) || ~all(IndexS<IndexE)
        error('Not properly specified *PART and *END PART options')
    end
    all_parts=cell(3,length(IndexS));
    for a=1:length(IndexS)
        str_line=CStr(IndexS(a));
        start_=strfind(str_line{1},'name=')+5;
        % If the NAME parameter is not specified, the part is not properly
        % defined
        if isempty(start_)
            error('Part does not have a name')
        end
        end_=strfind(str_line{1},',');
        if any(end_>start_)
            % If additional parameter(s) are specified after NAME
            end_=min(end_(end_>start_))-1;
        else
            % If the NAME parameter is the last in the option definition
            end_=length(str_line{1});
        end
        all_parts{1,a}=IndexS(a);
        all_parts{2,a}=IndexE(a);
        CStrPart=CStr_(IndexS(a));
        all_parts{3,a}=CStrPart{1}(start_:end_);
    end
    partdef=true;
end
waitbar(20 / 100)
%% Find INSTANCE definitions
IndexC = strfind(CStr,'*instance');
IndexS = find(~cellfun('isempty', IndexC));
IndexC = strfind(CStr,'*endinstance');
IndexE = find(~cellfun('isempty', IndexC));
instdef=false;
anal_import=false;
if ~isempty(IndexS)
    if numel(IndexS) ~= numel(IndexE) || ~all(IndexS<IndexE)
        error('Not properly specified *INSTANCE and *END INSTANCE options')
    end
    all_instances=cell(4,length(IndexS));
    for a=1:length(IndexS)
        str_line=CStr(IndexS(a));
        % NAME and PART are required parameters if instance is not imported
        % from a previous analysis
        start_1=strfind(str_line{1},'name=')+5;
        start_2=strfind(str_line{1},'part=')+5;
        % if NAME parameter not specified, check if instance is imported
        % from a previous analysis
        if isempty(start_1) || isempty(start_2)
            start_1=strfind(str_line{1},'instance=')+9;
            anal_import=true;
        end
        % If none of NAME or INSTANCE parameters are specified, the
        % instance is not properly defined
        if isempty(start_1)
            error('Instance improperly defined in the Abaqus input file')
        end
        end_=strfind(str_line{1},',');
        if any(end_>start_1)
            % If additional parameter(s) are specified after NAME
            end_=min(end_(end_>start_1))-1;
        else
            % If the NAME parameter is the last in the option definition
            end_=length(str_line{1});
        end
        end_1=end_;
        end_=strfind(str_line{1},',');
        if any(end_>start_2)
            % If additional parameter(s) are specified after PART
            end_=min(end_(end_>start_2))-1;
        else
            % If the PART parameter is the last in the option definition
            end_=length(str_line{1});
        end
        end_2=end_;
        all_instances{1,a}=IndexS(a);
        all_instances{2,a}=IndexE(a);
        CStrInstance=CStr_(IndexS(a));
        all_instances{3,a}=CStrInstance{1}(start_2:end_2);
        all_instances{4,a}=CStrInstance{1}(start_1:end_1);
    end
    instdef=true;
end
waitbar(30 / 100)
%% Find ASSEMBLY definitions
IndexC = strfind(CStr,'*assembly');
IndexS = find(~cellfun('isempty', IndexC));
IndexC = strfind(CStr,'*endassembly');
IndexE = find(~cellfun('isempty', IndexC));
if ~isempty(IndexS)
    if numel(IndexS)>1 || numel(IndexE)>1 || (IndexS>IndexE)
        error('Assembly improperly defined')
    end
    all_assemblies=cell(3,length(IndexS));
    % Only one assembly definition can be contained in the Abaqus input file
    if length(IndexS)>1
        error('More than one assemblies defined in the Abaqus input file')
    end
    str_line=CStr(IndexS);
    start_=strfind(str_line{1},'name=')+5;
    end_=strfind(str_line{1},',');
    if any(end_>start_)
        % If additional parameter(s) are specified after NAME
        end_=min(end_(end_>start_))-1;
    else
        % If the NAME parameter is the last in the option definition
        end_=length(str_line{1});
    end
    all_assemblies{1,1}=IndexS;
    all_assemblies{2,1}=IndexE;
    CStrAssembly=CStr_(IndexS);
    all_assemblies{3,1}=CStrAssembly{1}(start_:end_);
end
%% Find NSET definitions
IndexC = strfind(CStr,'nset=');
Index = find(~cellfun('isempty', IndexC));
all_nset=cell(2,length(Index));
for a=1:length(Index)
    str_line=CStr(Index(a));
    start_=strfind(str_line{1},'nset=')+5;
    end_=strfind(str_line{1},',');
    if any(end_>start_)
        % If additional parameter(s) are specified after NSET
        end_=min(end_(end_>start_))-1;
    else
        % If the NSET parameter is the last in the option definition
        end_=length(str_line{1});
    end
    all_nset{1,a}=Index(a);
    CStrNode=CStr_(Index(a));
    all_nset{2,a}=CStrNode{1}(start_:end_);
end

%% Find ELSET definitions
IndexC = strfind(CStr,'elset=');
Index = find(~cellfun('isempty', IndexC));
all_elset=cell(2,length(Index));
for a=1:length(Index)
    str_line=CStr(Index(a));
    start_=strfind(str_line{1},'elset=')+6;
    end_=strfind(str_line{1},',');
    if any(end_>start_)
        % If additional parameter(s) are specified after ELSET
        end_=min(end_(end_>start_))-1;
    else
        % If the ELSET parameter is the last in the option definition
        end_=length(str_line{1});
    end
    all_elset{1,a}=Index(a);
    CStrEle=CStr_(Index(a));
    all_elset{2,a}=CStrEle{1}(start_:end_);
end
waitbar(40 / 100)
%% Definitions of node sets within part/instance/assembly level
% part-level definitions inherited by instances
if partdef
    for i=1:size(all_parts,2)
        b2=all([cell2mat(all_parts(1,i))<cell2mat(all_nset(1,:))',...
            cell2mat(all_parts(2,i))>cell2mat(all_nset(1,:))'],2);
        if any(b2)
            ind=find(b2);
            for j=1:numel(ind)
                if strcmpi(all_instances{3,i},all_parts{3,i})
                    all_nset{2,ind(j)}=[all_instances{4,i},'.',all_nset{2,ind(j)}];
                end
            end
        end
    end
end
% instance-level definitions
if instdef
    for i=1:size(all_instances,2)
        b2=all([cell2mat(all_instances(1,i))<cell2mat(all_nset(1,:))',...
            cell2mat(all_instances(2,i))>cell2mat(all_nset(1,:))'],2);
        if any(b2)
            ind=find(b2);
            for j=1:numel(ind)
                all_nset{2,ind(j)}=[all_instances{4,i},'.',all_nset{2,ind(j)}];
            end
        end
    end
end

%% Definitions of element sets within part/instance/assembly level
% part-level definitions inherited by instances
if partdef
    for i=1:size(all_parts,2)
        b2=all([cell2mat(all_parts(1,i))<cell2mat(all_elset(1,:))',...
            cell2mat(all_parts(2,i))>cell2mat(all_elset(1,:))'],2);
        if any(b2)
            ind=find(b2);
            for j=1:numel(ind)
                if strcmpi(all_instances{3,i},all_parts{3,i})
                    all_elset{2,ind(j)}=[all_instances{4,i},'.',all_elset{2,ind(j)}];
                end
            end
        end
    end
end
% instance-level definitions
if instdef
    for i=1:size(all_instances,2)
        b2=all([cell2mat(all_instances(1,i))<cell2mat(all_elset(1,:))',...
            cell2mat(all_instances(2,i))>cell2mat(all_elset(1,:))'],2);
        if any(b2)
            ind=find(b2);
            for j=1:numel(ind)
                all_elset{2,ind(j)}=[all_instances{4,i},'.',all_elset{2,ind(j)}];
            end
        end
    end
end
waitbar(50 / 100)
%% Remove duplicate set definitions
% Remove duplicate NSET definitions
all_nset=unique(all_nset(2,:));
% Remove duplicate ELSET definitions
all_elset=unique(all_elset(2,:));

%% Find STEP definitions
IndexC = strfind(CStr,'*step');
IndexS = find(~cellfun('isempty', IndexC));
if isempty(IndexS)
    error('No *STEP option defined')
end
IndexC = strfind(CStr,'*endstep');
IndexE = find(~cellfun('isempty', IndexC));
if numel(IndexS) ~= numel(IndexE) || ~all(IndexS<IndexE)
    error('Not properly specified *STEP and *END STEP options')
end
if ~isempty(IndexS)
    k=1;
    all_steps=cell(4,length(IndexS));
    for a=1:length(IndexS)
        str_line=CStr(IndexS(a));
        % NAME and PART are required parameters if instance is not imported
        % from a previous analysis
        start_1=strfind(str_line{1},'name=')+5;
        % if NAME parameter not specified, check if instance is imported
        % from a previous analysis
        if isempty(start_1)
            all_steps{1,a}=IndexS(a);
            all_steps{2,a}=IndexE(a);
            all_steps{3,a}=['Unnamed',num2str(k)];
            k=k+1;
        else
            end_=strfind(str_line{1},',');
            if any(end_>start_1)
                % If additional parameter(s) are specified after NAME
                end_=min(end_(end_>start_1))-1;
            else
                % If the NAME parameter is the last in the option definition
                end_=length(str_line{1});
            end
            all_steps{1,a}=IndexS(a);
            all_steps{2,a}=IndexE(a);
            CStrStep=CStr_(IndexS(a));
            all_steps{3,a}=CStrStep{1}(start_1:end_);
        end
        % query for analysis type
        str_line=CStr(IndexS(a)+1);
        if ~isempty(cell2mat(strfind(str_line,'*dynamic'))) && ...
                ~isempty(cell2mat(strfind(str_line,'explicit')))
            % *dynamic, explicit analysis
            all_steps{4,a}='Exp';
        elseif ~isempty(cell2mat(strfind(str_line,'*dynamictemperature-displacement')))
            % *dynamic temperature-displacement analysis
            all_steps{4,a}='Exp';
        elseif ~isempty(cell2mat(strfind(str_line,'*anneal')))
            % *anneal analysis
            all_steps{4,a}='Exp';
        else
            % Abaqus/Standard for all other types of analysis
            all_steps{4,a}='Std';
        end
    end
end
% standard and explicit steps are not permitted in the same input file
StdExp=unique(all_steps(4,:));
if numel(StdExp)>1
    error('Abaqus/Standard and Abaqus/Explicit definitions in the Abaqus input file')
end
StdExp=StdExp{1};
waitbar(60 / 100)
%% Options in Abaqus/Standard for printing in the results file (fil)
StdOutOpts={'*fileformat';
    '*contactfile';
    '*elfile';
    '*energyfile';
    '*modalfile';
    '*nodefile';
    '*sectionfile'};
IndexStd=[];
fileformat=false;
for a=1:length(StdOutOpts)
    IndexC0=strfind(CStr, StdOutOpts{a});
    IndexC0 = find(~cellfun('isempty', IndexC0));
    if ~isempty(IndexC0)
        if a<=1
            if length(IndexC0)>1
                error('Option *FILE FORMAT more than one times defined')
            end
            % The option *fileformat is contained in the input file
            IndexStd=[IndexStd;IndexC0];
            fileformat=true;
        else
            for b=1:length(IndexC0)
                n=0;
                while ~strcmp(CStr{IndexC0(b)+1+n}(1),'*')
                    n=n+1;
                end
                IndexStd=[IndexStd;(IndexC0(b):(IndexC0(b)+n))'];
            end
        end
    end
end
% sort indices
IndexStd=sort(IndexStd);
waitbar(70 / 100)
%% Options in Abaqus/Explicit for printing in the results file (sel or fil)
ExplOutOpts={'*fileoutput';
    '*elfile';
    '*energyfile';
    '*nodefile'};
IndexExpl=[];
fileoutput=false;
for a=1:length(ExplOutOpts)
    IndexC0=strfind(CStr, ExplOutOpts{a});
    IndexC0 = find(~cellfun('isempty', IndexC0));
    if ~isempty(IndexC0)
        if a<=1
            if length(IndexC0)>1
                error('Option *FILE OUTPUT more than one times defined')
            end
            % The option *fileoutput is contained in the input file
            IndexExpl=[IndexExpl;IndexC0];
            fileoutput=true;
        else
            for b=1:length(IndexC0)
                n=0;
                while ~strcmp(CStr{IndexC0(b)+1+n}(1),'*')
                    n=n+1;
                end
                IndexExpl=[IndexExpl;(IndexC0(b):(IndexC0(b)+n))'];
            end
        end
    end
end
% sort indices
IndexExpl=sort(IndexExpl);
waitbar(90 / 100)
%% Options in Abaqus for printing in the odb file
OdbOutOpts={'*output';
    '*elementoutput';
    '*nodeoutput';
    '*contactoutput';
    '*modaloutput';
    '*integratedoutput';
    '*incrementationoutput';
    '*radiationoutput';
    '*surfaceoutput';
    '*energyoutput'};
IndexOdb=[];
for a=1:length(OdbOutOpts)
    IndexC0=strfind(CStr, OdbOutOpts{a});
    IndexC0 = find(~cellfun('isempty', IndexC0));
    if ~isempty(IndexC0)
        if a<=1
            % The option *output is contained in the input file
            IndexOdb=[IndexOdb;IndexC0];
        else
            for b=1:length(IndexC0)
                n=0;
                %if ~isempty(CStr{IndexC0(b)+1+n})
                while ~strcmp(CStr{IndexC0(b)+1+n}(1),'*')
                    n=n+1;
                end
                IndexOdb=[IndexOdb;(IndexC0(b):(IndexC0(b)+n))'];
            end
        end
    end
end
% sort indices
IndexOdb=sort(IndexOdb);

%% Checks for output options for fil and odb files
% check results file requests for Abaqus/Standard
if ~isempty(IndexStd)
    % check if results file requests are within a step definition
    deterr1=false(size(IndexStd,1),1);
    for i=1:size(all_steps,2)
        S_=all_steps{1,i};
        E_=all_steps{2,i};
        deterr1=deterr1 | ((IndexStd>S_) & (IndexStd<E_));
        deterr2=IndexStd(((IndexStd>S_) & (IndexStd<E_)));
        if ~isempty(deterr2)
            if (1+deterr2(end)-deterr2(1))~=numel(deterr2)
                warning('Results file requests not in correct order')
            end
        end
    end
    if ~all(deterr1)
        error('At least one results file request outside a step definition')
    end
end
% check results file requests for Abaqus/Explicit
if ~isempty(IndexExpl)
    % check if results file requests are within a step definition
    deterr1=false(size(IndexExpl,1),1);
    for i=1:size(all_steps,2)
        S_=all_steps{1,i};
        E_=all_steps{2,i};
        deterr1=deterr1 | ((IndexExpl>S_) & (IndexExpl<E_));
        deterr2=IndexExpl(((IndexExpl>S_) & (IndexExpl<E_)));
        if ~isempty(deterr2)
            if (1+deterr2(end)-deterr2(1))~=numel(deterr2)
                warning('Results file requests not in correct order')
            end
        end
    end
    if ~all(deterr1)
        error('At least one results file request outside a step definition')
    end
end
% check results file requests for odb
if ~isempty(IndexOdb)
    % check if results file requests are within a step definition
    deterr1=false(size(IndexOdb,1),1);
    for i=1:size(all_steps,2)
        S_=all_steps{1,i};
        E_=all_steps{2,i};
        deterr1=deterr1 | ((IndexOdb>S_) & (IndexOdb<E_));
        deterr2=IndexOdb(((IndexOdb>S_) & (IndexOdb<E_)));
        if ~isempty(deterr2)
            if (1+deterr2(end)-deterr2(1))~=numel(deterr2)
                warning('Output data base file requests not in correct order')
            end
        end
    end
    if ~all(deterr1)
        error('At least one output data base file request outside a step definition')
    end
end

%% Function output to GUI
noFilOpt=false;
if (~fileoutput) && (~fileformat)
    noFilOpt=true;
    warning('No options related to results file (*.fil)');
    if strcmp(StdExp,'Std')
        Index=IndexStd;
    elseif strcmp(StdExp,'Exp')
        Index=IndexExpl;
    end
elseif (~fileoutput) && (fileformat)
    Index=IndexStd;
elseif (fileoutput) && (~fileformat)
    Index=IndexExpl;
else
    error('Both *FILE FORMAT and *FILE OUTPUT options specified.');
end

Index=sort([Index;IndexOdb]);
for a=1:size(all_steps,2)
    previous_vars{a}=CStr_(Index((Index>all_steps{1,a} & Index<all_steps{2,a})));
end
waitbar(100 / 100)
if noFilOpt
    if strcmp(StdExp,'Std')
        previous_vars{1}=['*FILE FORMAT, ASCII';previous_vars{1}];
    elseif strcmp(StdExp,'Exp')
        previous_vars{1}=['*FILE OUTPUT';previous_vars{1}];
    end
end
all_steps=all_steps(3,:);
clear_lines=Index;
try
    close(h)
catch
end
end
function [ NEW_Index_steps ] = Obtain_Index_step( CStr_ )
% Delete whitespaces
CStr_ = regexprep(CStr_,'\s','');
% Delete tabs
CStr_ = regexprep(CStr_,'\t','');
% Delete formfeeds
CStr_ = regexprep(CStr_,'\f','');
% Delete linefeeds
CStr_ = regexprep(CStr_,'\n','');
% Delete carriage returns
CStr_ = regexprep(CStr_,'\r','');
% Delete vertical tabs
CStr_ = regexprep(CStr_,'\v','');
% Delete comments
IndexC = strfind(CStr_,'**');
CStr_(~cellfun('isempty', IndexC))=[];
% Delete empty lines
CStr_(cellfun('isempty', CStr_))=[];
% Convert to lowercase characters
CStr = lower(CStr_);

IndexC = strfind(CStr,'*step');
Index_start_step = find(~cellfun('isempty', IndexC));
IndexC = strfind(CStr,'*endstep');
Index_end_step = find(~cellfun('isempty', IndexC));
NEW_Index_steps=([Index_start_step,Index_end_step]);
end
function [ CStr ] = PostProcessDataCell( CStr_ )
%% Preprocess the Data cell
if ~isempty(CStr_)
    % Delete whitespaces
    CStr_ = regexprep(CStr_,'\s','');
    % Delete tabs
    CStr_ = regexprep(CStr_,'\t','');
    % Delete formfeeds
    CStr_ = regexprep(CStr_,'\f','');
    % Delete linefeeds
    CStr_ = regexprep(CStr_,'\n','');
    % Delete carriage returns
    CStr_ = regexprep(CStr_,'\r','');
    % Delete vertical tabs
    CStr_ = regexprep(CStr_,'\v','');
    % Delete comments
    IndexC = strfind(CStr_,'**');
    if isempty(IndexC)
        CStr_(~isempty(IndexC))=[];
    end
    % Delete empty lines
    CStr_(isempty(CStr_))=[];
    % Convert to lowercase characters
    CStr = lower(CStr_);
else
    CStr=CStr_;
end
end
function [text_to_input]=include_node_variable(text_to_input,set,variable)
%% Preprocess the Data cell
CStr_=text_to_input;
% Delete whitespaces
CStr_ = regexprep(CStr_,'\s','');
% Delete tabs
CStr_ = regexprep(CStr_,'\t','');
% Delete formfeeds
CStr_ = regexprep(CStr_,'\f','');
% Delete linefeeds
CStr_ = regexprep(CStr_,'\n','');
% Delete carriage returns
CStr_ = regexprep(CStr_,'\r','');
% Delete vertical tabs
CStr_ = regexprep(CStr_,'\v','');
% Delete comments
IndexC = strfind(CStr_,'**');
if isempty(IndexC)
    CStr_(~cellfun('isempty', IndexC))=[];
end
% Delete empty lines
CStr_(cellfun('isempty', CStr_))=[];
% Convert to lowercase characters
CStr = lower(CStr_);

% *NODE FILE
IndexC5 = strfind(CStr, '*nodefile');
IndexC5 = find(~cellfun('isempty', IndexC5));
if isempty(IndexC5) %NO Exist nodefile
    
    flaged=1;
    
else %Exist nodefile
    
    for p=1:length(IndexC5)
        [ Options_nset ]=extract_info_comma( CStr_{IndexC5(p)} );
        IS_set(p)=sum(strcmpi(Options_nset,['nset=' set]));
    end
    position=find(IS_set);
    
    if sum(IS_set)>0%Exist nset
        [ variables_previously_selected ]=extract_info_comma( CStr_{IndexC5(position)+1} );
        IS_var=strcmpi(variables_previously_selected,variable);
        
        if sum(IS_var)>0 %Exist var
            flaged=3;
        else
            flaged=2;
            position=IndexC5(position)+1;
        end
        
    else %NO Exist nset
        if strcmpi(set,'ALL')
            for p=1:length(IndexC5)
                IS_set(p)=isempty(strfind(CStr{IndexC5(p)},'nset='));
            end
            position=sum(IS_set);
            if position>0%Exist ALL
                [ variables_previously_selected ]=extract_info_comma( CStr_{IndexC5(position)+1} );
                IS_var=strcmpi(variables_previously_selected,variable);
                
                if sum(IS_var)>0 %Exist var
                    flaged=3;
                else
                    flaged=2;
                    position=IndexC5(position)+1;
                end
            else
                flaged=1;
            end
        else
            flaged=1;
        end
    end
end

switch flaged
    case 1
        if strcmpi(set,'ALL')
            text_to_input{end+1}=['*NODE FILE'];
            text_to_input{end+1}=[variable];
        else
            text_to_input{end+1}=['*NODE FILE, NSET=' set];
            text_to_input{end+1}=[variable];
        end
    case 2
        text_to_input{position}=[text_to_input{position} ',' variable];
    case 3
        disp('This variable is already included in this nset and step');
end
end
function [text_to_input]=include_element_variable(text_to_input,set,variable)
%% Preprocess the Data cell
CStr_=text_to_input;
% Delete whitespaces
CStr_ = regexprep(CStr_,'\s','');
% Delete tabs
CStr_ = regexprep(CStr_,'\t','');
% Delete formfeeds
CStr_ = regexprep(CStr_,'\f','');
% Delete linefeeds
CStr_ = regexprep(CStr_,'\n','');
% Delete carriage returns
CStr_ = regexprep(CStr_,'\r','');
% Delete vertical tabs
CStr_ = regexprep(CStr_,'\v','');
% Delete comments
IndexC = strfind(CStr_,'**');
CStr_(~cellfun('isempty', IndexC))=[];
% Delete empty lines
CStr_(cellfun('isempty', CStr_))=[];
% Convert to lowercase characters
CStr = lower(CStr_);

% *NODE FILE
IndexC5 = strfind(CStr, '*elfile');
IndexC5 = find(~cellfun('isempty', IndexC5));
if isempty(IndexC5) %NO Exist nodefile
    
    flaged=1;
    
else %Exist nodefile
    
    for p=1:length(IndexC5)
        [ Options_nset ]=extract_info_comma( CStr_{IndexC5(p)} );
        IS_set(p)=sum(strcmpi(lower(Options_nset),['elset=' lower(set)]));
    end
    position=find(IS_set);
    
    if sum(IS_set)>0%Exist nset
        [ variables_previously_selected ]=extract_info_comma( CStr_{IndexC5(position)+1} );
        IS_var=strcmpi(variables_previously_selected,variable);
        
        if sum(IS_var)>0 %Exist var
            flaged=3;
        else
            flaged=2;
            position=IndexC5(position)+1;
        end
        
    else %NO Exist nset
        if strcmpi(set,'ALL')
            for p=1:length(IndexC5)
                IS_set(p)=isempty(strfind(CStr{IndexC5(p)},'elset='));
            end
            position=sum(IS_set);
            if position>0%Exist ALL
                [ variables_previously_selected ]=extract_info_comma( CStr_{IndexC5(position)+1} );
                IS_var=strcmpi(variables_previously_selected,variable);
                
                if sum(IS_var)>0 %Exist var
                    flaged=3;
                else
                    flaged=2;
                    position=IndexC5(position)+1;
                end
            else
                flaged=1;
            end
        else
            flaged=1;
        end
    end
end

switch flaged
    case 1
        if strcmpi(set,'ALL')
            text_to_input{end+1}=['*EL FILE'];
            text_to_input{end+1}=[variable];
        else
            text_to_input{end+1}=['*EL FILE, ELSET=' set];
            text_to_input{end+1}=[variable];
        end
    case 2
        text_to_input{position}=[text_to_input{position} ',' variable];
    case 3
        disp('This variable is already included in this nset and step');
end
end
function [ variables_previously_selected ] = extract_info_comma( cell_text_var )
b=1;
cell_text_var=regexprep(cell_text_var,'\s','');
pos=strfind( cell_text_var,',');
if isempty(pos)
    variables_previously_selected{b}= cell_text_var;
    b=b+1;
else
    if pos(end)~=length( cell_text_var)
        pos(length(pos)+1)=length( cell_text_var)+1;
    end
    variables_previously_selected{b}= cell_text_var(1:pos(1)-1);
    b=b+1;
    for ii=1:(length(pos)-1)
        variables_previously_selected{b}= cell_text_var(pos(ii)+1:pos(ii+1)-1);
        b=b+1;
    end
end
end

%% FUNCTIONS FOR STORAGE OF VARIABLES

function [OUTPUTVARIABLEIDENTIFIER_nodes, OUTPUTVARIABLEIDENTIFIER_elements,...
    NODALRECORDTYPE, FUNCTION_nodes, FUNCTION_elements, ELEMENTRECORDTYPE]=...
    load_Variables()

NODALRECORDTYPE = {
    
'Concentrated Electrical Nodal Charge(CECHG)'
'Concentrated Electrical Nodal Current(CECUR)'
'Concentrated Flux(CFL)'
'Electrical Potential(EPOT)'
'Electrical Reaction Charge(RCHG)'
'Electrical Reaction Current(RECUR)'
'Fluid Cavity Pressure(PCAV)'
'Fluid Cavity Volume(CVOL)'
'Internal Flux(RFLE)'
'Motions (in Cavity Radiation Analysis)(MOT)'
'Nodal Acceleration(A)'
'Nodal Coordinate(COORD)'
'Nodal Displacement(U)'
'Nodal Point Load(CF)'
'Nodal Reaction Force(RF)'
'Nodal Velocity(V)'
'Normalized Concentration (Mass Diffusion Analysis)(NNC)'
'Pore or Acoustic Pressure(POR)'
'Reactive Fluid Total Volume(RVT)'
'Reactive Fluid Volume Flux(RVF)'
'Residual Flux(RFL)'
'Temperature(NT)'
'Total Force(TF)'
'Viscous Forces Due to Static Stabilization(VF)'};

ELEMENTRECORDTYPE ={
    
'Average Shell Section Stress(SSAVG)'
'Concrete Failure(CONF)'
'Coordinates(COORD)'
'Creep Strain (Including Swelling)(CE)'
'Element Status(STATUS)'
'Energy (Summed over Element)(ELEN)'
'Energy Density(ENER)'
'Equivalent plastic strain components(PEQC)'
'Film(FILM)'
'Gel (Pore Pressure Analysis)(GELVR)'
'Heat Flux Vector(HFL)'
'J-integral(JK)'
'Logarithmic Strain(LE)'
'Mass Concentration (Mass Diffusion Analysis)(CONC)'
'Mechanical Strain Rate(ER)'
'Nodal Flux Caused by Heat(NFLUX)'
'Nominal Strain(NE)'
'Plastic Strain(PE)'
'Pore Fluid Effective Velocity Vector(FLVEL)'
'Pore or Acoustic Pressure(POR)'
'Principal elastic strains(EEP)'
'Principal inelastic strains(IEP)'
'Principal logarithmic strains(LEP)'
'Principal mechanical strain rates(ERP)'
'Principal nominal strains(NEP)'
'Principal plastic strains(PEP)'
'Principal strains(EP)'
'Principal stresses(SP)'
'Principal thermal strains(THEP)'
'Principal values of backstress tensor for kinematic harden...'
'Principal values of deformation gradient(DGP)'
'Radiation(RAD)'
'Saturation (Pore Pressure Analysis)(SAT)'
'Section Force and Moment(SF)'
'Section Strain and Curvature(SE)'
'Section Thickness(STH)'
'Strain Jump at Nodes(SJP)'
'Stress(S)'
'Stress Invariant(SINV)'
'Thermal Strain(THE)'
'Total Elastic Strain(EE)'
'Total Fluid Volume Ratio(FLUVR)'
'Total Inelastic Strain(IE)'
'Total Strain(E)'
'Unit Normal to Crack in Concrete(CRACK)'
'Whole Element Volume(EVOL)'};

FUNCTION_nodes = {
    
'120'
'139'
'206'
'105'
'119'
'138'
'136'
'137'
'214'
'237'
'103'
'107'
'101'
'106'
'104'
'102'
'221'
'18'
'110'
'109'
'204'
'201'
'146'
'145'};

FUNCTION_elements = {
    
'83'
'31'
'8'
'23'
'61'
'19'
'14'
'45'
'33'
'40'
'28'
'1991'
'89'
'38'
'91'
'10'
'90'
'22'
'97'
'18'
'408'
'409'
'405'
'406'
'404'
'411'
'403'
'401'
'410'
'402'
'407'
'34'
'35'
'13'
'29'
'27'
'32'
'11'
'12'
'88'
'25'
'43'
'24'
'21'
'26'
'78'};

OUTPUTVARIABLEIDENTIFIER_elements = {
    
'SSAVG'
'CONF'
'COORD'
'CE'
'STATUS'
'ELEN'
'ENER'
'PEQC'
'FILM'
'GELVR'
'HFL'
'JK'
'LE'
'CONC'
'ER'
'NFLUX'
'NE'
'PE'
'FLVEL'
'POR'
'EEP'
'IEP'
'LEP'
'ERP'
'NEP'
'PEP'
'EP'
'SP'
'THEP'
'ALPHAP'
'DGP'
'RAD'
'SAT'
'SF'
'SE'
'STH'
'SJP'
'S'
'SINV'
'THE'
'EE'
'FLUVR'
'IE'
'E'
'CRACK'
'EVOL'};

OUTPUTVARIABLEIDENTIFIER_nodes = {
    
'CECHG'
'CECUR'
'CFL'
'EPOT'
'RCHG'
'RECUR'
'PCAV'
'CVOL'
'RFLE'
'MOT'
'A'
'COORD'
'U'
'CF'
'RF'
'V'
'NNC'
'POR'
'RVT'
'RVF'
'RFL'
'NT'
'TF'
'VF'};
end
function [CStr]=load_template_script()

CStr = {
    
'% If using this code for research or industrial purposes please cite:'
''
'% G. Papazafeiropoulos, M. Muniz-Calvente, E. Martinez-Paneda'
'% Abaqus2Matlab: a suitable tool for finite element post-processing.'
'% Advances in Engineering Software. Vol. 105, pp 9-16 (2017)'
'% DOI:10.1016/j.advengsoft.2017.01.006'
'% % G. Papazafeiropoulos, M. Muniz Calvente, E. Martinez-Paneda'
'% % % Abaqus2Matlab@gmail.com'
'% www.abaqus2matlab.com'
''
'%close all'
'clear'
'% Change the current directory'
'S = mfilename(''fullpath'');'
'f = filesep;'
'ind=strfind(S,f);'
'S1=S(1:ind(end)-1);'
'cd(S1) ;'
'%% 1st STEP - Run one FEM model'
''
'disp(''Simulation Started'')'
''
''
'% Run the input file with Abaqus'
'% Initialize sw (boolean switch) as true'
'system([''abaqus job='' Inp_file]);'
'    sw=true;'
'    tic;'
'    while sw'
'        % Pause Matlab execution in order for the lck file to be created'
'        pause(0.5);'
'        % While the lck file exists, pause Matlab execution. If it is'
'        % deleted, exit the while loop and proceed.'
'        while exist([Inp_file ''.lck''],''file'')==2'
'            pause(0.1)'
'            % the lck file has been created and Matlab halts in this loop.'
'            % Set sw to false to break the outer while loop and continue'
'            % the code execution.'
'            sw=false;'
'        end'
'        % In case that the lck file cannot be detected, then terminate'
'        % infinite execution of the outer while loop after a certain'
'        % execution time limit (5 sec)'
'        if sw && (toc>5)'
'            sw=false;'
'        end'
'    end'
'% NOTE: Alternatively, you can replace lines 27 to 49 by system([''abaqus job='' Inp_file '' interactive''])'
''
'disp(''Simulation Finished'')'
''
'%% 2st STEP - Postprocess Abaqus results file with Abaqu2Matlab'
'% Obtain the desired output data'
'disp(''Obtaining desired output data by Abaqus2Matlab'')'
'% NOTE: Some output variables are Matlab Cells, If you are not confortable working with Cells, you can use cell2mat()'
''};
end
