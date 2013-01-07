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

#当前目录
CurDir := $(shell pwd)
#相对项目的路径
RefPath := $(subst $(ProjectDir),,$(CurDir))
#当前中间目录
CurInt := $(IntDir)/$(RefPath)
#当前目录下的所有子目录
SubDirs := $(shell ls -p | grep -o -P ".+(?=/)")

#需要创建的文件夹
Folders := $(CurInt)

VPATH := $(CurInt):$(ProjectVPATH)

FolderDepend := $(Folders) $(SubDirs)

foldersAll: $(FolderDepend)

$(Folders):
	-mkdir $@

$(SubDirs):
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectFolders.mak -C $@

.PHONY : foldersAll $(SubDirs)

