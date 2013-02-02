#!/bin/bash
auto_smart_ssh () {
    expect -c "
        spawn -noecho scp $1 $3@$5:$2
            expect {
                \"Connection refused\" {exit 4;}
                \"*assword\" {send \"$4\r\";
					expect { 
                        *denied* {exit 2;}
						*100%* {;}
                        eof {exit 3;}
                    }
				}
                \"yes/no\" {send \"yes\r\"; exp_continue;}
                eof {exit 1;}
            }
			expect eof 
    "
    return $?
}

auto_smart_ssh $1 $2 $3 $4 $5
if [ $? -eq 0 ];
	then
    cp -f $6 $7
fi
