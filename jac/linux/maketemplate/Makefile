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

