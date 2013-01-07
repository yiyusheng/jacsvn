#!/bin/bash
expect -c "
	spawn -noecho ssh -o StrictHostKeyChecking=no $1@$3 ${@:4};
	expect {
		*assword:* {send -- $2\r;
			expect { 
				*denied* {exit 2;}
				eof
			}
		}
		eof		{exit 1;}
	}
" 
