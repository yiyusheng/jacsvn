expect -c "
spawn -noecho scp $1 $3@$5:$2
    expect {
        \"*assword\" {set timeout 300; send \"$4\r\";}
        \"yes/no\" {send \"yes\r\"; exp_continue;}
        }
        expect eof"