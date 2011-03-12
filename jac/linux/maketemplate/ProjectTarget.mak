
#目标文件
export TargetPath := $(OutDir)/$(TargetName)

#make的文件搜寻目录
export ProjectVPATH := $(subst $(space),:,$(patsubst -I%,%,$(AttachInc))):$(patsubst -L%,%,$(subst $(space),:,$(AttachDllDir))):$(OutDir)
VPATH := $(ProjectVPATH)

#终级目标信赖项
TargetDepend := $(ProjectDependList) $(ProjectFolders) $(notdir $(GCH)) objects $(TargetName)

#默认目标
all: $(TargetDepend)

#编译依赖的项目
$(ProjectDependList):
	@$(Make) $(MGLAGS) -C $(SolutionSrc)/$@

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

#生成预编译头
$(GCHFile): $(GCHHead)
	@echo Project:$(ProjectName) create GCHHead $(GCHFile)
	$(CXX) $(CPPFLAGS) $(ProjectInc)/$(GCHHead) -o $(GCH)

#生成所有obj文件
objects:
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectDepend.mak

#根据配置类型选择终极目标的生成命令
ifeq ($(ConfigurationType),lib)
CreateTargetCmd := $(AR) $(ARFLAGS) $(TargetPath) $(AllObjects) $(AttachLib)
else
CreateTargetCmd := $(CXX) $(CPPFLAGS) $(LDFLAGS) -o $(TargetPath) $(AllObjects) $(AttachLib)
endif
$(TargetName): $(AllObjects)
	@echo Project:$(ProjectName) create target $(TargetName)
	$(CreateTargetCmd)

.PHONY : all clean debug release $(ProjectDependList) objects

clean :
	@echo Project:$(ProjectName) clean
	-rm -f $(AllObjects) $(AllDepends) $(TargetPath) $(GCH)

