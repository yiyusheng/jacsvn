#!/bin/bash
expect -c "
spawn -noecho scp $1 $3@$5:$2
    expect {
        \"*assword\" {send \"$4\r\";}
        \"yes/no\" {send \"yes\r\"; exp_continue;}
        }
        expect eof"
$6/autossh.sh $3 $4 $5 mv -f $2 $1
