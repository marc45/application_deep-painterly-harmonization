

import subprocess


#This command could have multiple commands separated by a new line \n
#some_command = "export PATH=$PATH://server.sample.mo/app/bin \n customupload abc.txt"
some_command = "   th daemon_gram.lua 2>&1 >a1.log "

while True:
    p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate()  

    #This makes the wait possible
    p_status = p.wait()

    #This will give you the output of the command being executed
    #print "Command output: " + output


