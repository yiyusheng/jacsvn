
#make的文件搜寻目录
export VPATH := $(subst $(space),:,$(patsubst -I%,%,$(AttachInc))):$(patsubst -L%,%,$(subst $(space),:,$(AttachDllDir))):$(IntDir):$(OutDir)

#终级目标信赖项
TargetDepend := $(ProjectDependList) $(ProjectFolders) $(notdir $(GCH)) objects target

#默认目标
all $(ProjectName): $(TargetDepend)
	@echo Project:$(ProjectName) success complete! Target:$@

#编译依赖的项目
$(ProjectDependList):
	$(Make) -r -C $(SolutionSrc)/$@

#创建需要的文件夹
$(ProjectFolders):
	-mkdir $@

#确保在只有debug和release一个参数时，make能够正常执行
SingleConfigurationDepend :=
ifeq ($(MAKECMDGOALS),debug)
SingleConfigurationDepend := $(TargetDepend)
else
ifeq ($(MAKECMDGOALS),release)
SingleConfigurationDepend := $(TargetDepend)
endif
endif

debug release: $(SingleConfigurationDepend)
	@echo Project:$(ProjectName) success complete! Target:$@

#生成预编译头
$(GCHFile): $(GCHHead)
	$(CXX) $(CPPFLAGS) $(ProjectInc)/$(GCHHead) -o $(IntDir)/$(GCHFile)

#生成所有obj文件
objects:
	$(Make) -f $(MakeInc)/ProjectDepend.mak

#根据配置类型选择终极目标的生成命令
ifeq ($(ConfigurationType),lib)
CreateTargetCmd := $(AR) $(ARFLAGS) $(TargetPath) $(AllObjects) $(AttachLib)
else
CreateTargetCmd := $(CXX) $(CPPFLAGS) $(LDFLAGS) -o $(TargetPath) $(AllObjects) $(AttachLib)
endif
target:
	$(CreateTargetCmd)


.PHONY : all $(ProjectName) clean debug release $(ProjectDependList) objects target

clean :
	-rm -f $(AllObjects) $(AllDepends) $(TargetPath) $(GCH)

