cd Z:\RR\Meso-scale-Cantilevers-Abaqus-Automation
dos('abaqus cae script=Method_StandardStatic_franken.py')
% JobName = 'nanoindent'
% pop = helpdlg('click')
% waitfor(pop)
% cd C:\Users\trin3150\Documents\Abaqus\liltemp
% !abaqus job=nanoindent input=nanoindent.inp
% dos('abaqus job=nanoindent input=nanoindent.inp interactive')
% cmd_str = ['abaqus job=', 'nanoindent', ' input=', 'nanoindent', '.inp interactive'];
% disp(cmd_str);
% system(cmd_str)