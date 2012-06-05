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

#解决方案目录
SolutionDir := ../..
#makefile包含目录
MakeInc := $(SolutionDir)/include/makeinclude

#项目列表
ProjectList := $(patsubst $(SolutionDir)/src/%/,%,$(shell ls -d $(SolutionDir)/src/*/))

#需要创建的文件夹
Folders := $(MakeInc) $(SolutionDir)/bin $(SolutionDir)/bin/debug $(SolutionDir)/bin/release $(SolutionDir)/doc $(SolutionDir)/lib $(SolutionDir)/src $(SolutionDir)/tmp

help:
	@echo 请输入具体的命令

solution:
	cp Makefile.solution $(SolutionDir)/Makefile

makeinclude:
	cp ProjectObject.mak $(MakeInc)/ProjectObject.mak;\
	cp ProjectTarget.mak $(MakeInc)/ProjectTarget.mak;\
	cp ProjectToSolution.def $(MakeInc)/ProjectToSolution.def;\
	cp ProjectVar.def $(MakeInc)/ProjectVar.def;\
	cp SolutionVar.def $(MakeInc)/SolutionVar.def

makeinclude.clean:
	-rm -f $(MakeInc)/ProjectObject.mak;\
	rm -f $(MakeInc)/ProjectTarget.mak;\
	rm -f $(MakeInc)/ProjectToSolution.def;\
	rm -f $(MakeInc)/ProjectVar.def;\
	rm -f $(MakeInc)/SolutionVar.def

solution.clean:
	-rm -f $(SolutionDir)/Makefile

$(ProjectList):
	cp Makefile.project $(SolutionDir)/src/$@/Makefile

$(Folders):
	-mkdir $@

all: $(Folders) solution $(ProjectList) makeinclude

.PHONY: help solution $(ProjectList) clean solution.clean $(ProjectList:%=%.clean)

$(ProjectList:%=%.clean):
	-rm -f $(SolutionDir)/src/$(basename $@)/Makefile

clean: solution.clean $(ProjectList:%=%.clean) makeinclude.clean

