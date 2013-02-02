#################################################################################
#    asyframe for asyframe@gmail.com											#
#																				#
#    Copyright (C) 2011, asyframe@gmail.com, http://asyframe.googlecode.com/	#
#																				#
#    This program is free software: you can redistribute it and/or modify		#
#    it under the terms of the GNU General Public License as published by		#
#    the Free Software Foundation, either version 3 of the License, or			#
#	(at your option) any later version.											#
#																				#
#    This program is distributed in the hope that it will be useful,			#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of				#
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the				#
#    GNU General Public License for more details.								#
#																				#
#    You should have received a copy of the GNU General Public License			#
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.		#
#################################################################################

ifeq ($(MAXSCPTRYMAKELEVEL),$(MAKELEVEL))
$(error Exceed max make level! CURDIR=$(CURDIR) MAKECMDGOALS=$(MAKECMDGOALS))
endif

target := $(firstword $(MAKECMDGOALS))
OtherNodeIP := $(basename $(notdir $(target)))

#生成二进制目标文件
$(target): $(AllObjects)
	$(MakeInc)/autoscp.sh $(ProjectDir)/$(TokenFile) $(IntDir)/$(NodeIP).TokenFile $(SCPUsername) $(SCPPassword) $(OtherNodeIP) $(ProjectDir)/$(TokenFile) $@ 1>/dev/null
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectCreateSCPFinishFile.mak $(target)
