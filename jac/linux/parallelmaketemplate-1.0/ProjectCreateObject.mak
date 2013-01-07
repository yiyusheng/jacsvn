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

#源文件
sources := $(wildcard *.cpp) $(wildcard *.cxx) $(wildcard *.cc) $(wildcard *.C) $(wildcard *.c)
basenames := $(basename $(sources))
#二进制目标文件
objects := $(addsuffix .o,$(basenames))
#依赖项文件
depends := $(addsuffix .d,$(basenames))
#二进制目标文件按文件名排序
sortedObjects := $(sort $(objects))

#临时变量
tmpObjects := 
partObjects :=

#本结点负责编译的object文件 
responsibleObjects :=

define SetResponsibleObjects
responsibleObjects := $(responsibleObjects) $(word $(NodeIndex),$(partObjects))
partObjects :=
endef

define SetPartObjects
partObjects := $(if $(word $(AllNodesNum),$(tmpObjects)),$(tmpObjects))
$$(eval $$(call SetResponsibleObjects))
tmpObjects := $(if $(word $(AllNodesNum),$(tmpObjects)),,$(tmpObjects))
endef

define FilterByNodeIndex
tmpObjects := $(tmpObjects) $(1)
$$(eval $$(call SetPartObjects))
endef

$(foreach n,$(sortedObjects),$(eval $(call FilterByNodeIndex,$(n))))

responsibleObjects := $(responsibleObjects) $(word $(NodeIndex),$(tmpObjects))

VPATH := $(CurInt):$(ProjectVPATH)

#生成二进制目标文件
$(responsibleObjects):
	@echo Project:$(ProjectName) create object $(RefPath)/$@;
	$(CXX) -c $(CPPFLAGS) $(shell find . ! -name "." -type d -prune -o \( -name "$(basename $@).cpp" -o -name "$(basename $@).cxx" -o -name "$(basename $@).cc" -o -name "$(basename $@).C" -o -name "$(basename $@).c" \) -print) -o $(CurInt)/$@;
	$(MakeInc)/batscp.sh $(CurInt)/$@ $(CurInt)/ $(SCPUsername) $(SCPPassword) $(MakeInc) $(OtherNodesIPList)
