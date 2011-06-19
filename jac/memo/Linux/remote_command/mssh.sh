#!/usr/bin/expect -f

#auto ssh login
set timeout 30
set sshhost [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
set sshcommand [lindex $argv 3]
spawn ssh -l$username $sshhost $sshcommand
expect "password:"
send "$password\r"

interact
