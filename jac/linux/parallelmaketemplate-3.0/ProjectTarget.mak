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

#目标文件
export TargetPath := $(OutDir)/$(TargetName)

#make的文件搜寻目录
export ProjectVPATH := $(OutDir):$(patsubst -L%,%,$(subst $(space),:,$(AttachDllDir))):$(subst $(space),:,$(patsubst -I%,%,$(AttachInc)))
VPATH := $(ProjectVPATH)

#二进制目标文件按文件名排序
sortedObjects := $(sort $(AllObjects))

#临时变量
tmpObjects := 
partObjects :=

#本结点负责编译的object文件 
export allResponsibleObjects :=
#本结点正在编译的object文件
export workingObjects :=

define SetOtherResponsibleObjects
export $(1).ResponsibleObjects := $$($(1).ResponsibleObjects) $$(word $($(1).NodeIndex),$(partObjects))
endef

define SetResponsibleObjects
allResponsibleObjects := $(allResponsibleObjects) $(word $(NodeIndex),$(partObjects))
$(foreach n,$(OtherNodesIPList),$(eval $(call SetOtherResponsibleObjects,$(n))))
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

allResponsibleObjects := $(allResponsibleObjects) $(word $(NodeIndex),$(tmpObjects))

define SetOtherFinalResponsibleObject
$(1).ResponsibleObjects := $$($(1).ResponsibleObjects) $$(word $($(1).NodeIndex),$(tmpObjects))
endef
$(foreach n,$(OtherNodesIPList),$(eval $(call SetOtherFinalResponsibleObject,$(n))))

#终级目标依赖项
TargetDepend := $(ProjectDependList) folders chmods $(notdir $(GCHDepend)) $(notdir $(GCH)) objects $(patsubst %,%.wait,$(AllObjects)) $(TargetPath) $(AllTokenFiles) $(TargetName)

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

#根据.h文件自动生成GCH依赖项.d文件
$(GCHDependFile):
	@set -e; rm -f $(GCHDir)/$@; \
	$(CXX) -MM $(CPPFLAGS) $(ProjectInc)/$(GCHHead) > $(GCHDir)/$@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.h.gch $@ : ,g' < $(GCHDir)/$@.$$$$ > $(GCHDir)/$@; \
	rm -f $(GCHDir)/$@.$$$$

#生成预编译头
$(GCHFile): $(GCHHead)
	@echo Project:$(ProjectName) create GCHHead $(GCHFile)
	$(CXX) $(CPPFLAGS) $(ProjectInc)/$(GCHHead) -o $(GCH)

#将生成的.d文件包含在内
-include $(GCHDepend)

#创建所有的需要的文件夹
folders: $(ProjectFolders)
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectFolders.mak

#改变sh文件的权限
chmods:
	chmod +x $(MakeInc)/autoscp.sh
	chmod +x $(MakeInc)/batscp.sh

#生成所有depends文件
depends:
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectDepend.mak

#生成所有obj文件
objects:
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectObject.mak

#根据配置类型选择终极目标的生成命令
ifeq ($(ConfigurationType),lib)
CreateTargetCmd := $(AR) $(ARFLAGS) $(TargetPath) $(AllObjects) $(AttachLib)
else
CreateTargetCmd := $(CXX) $(CPPFLAGS) $(LDFLAGS) -o $(TargetPath) $(AllObjects) $(AttachLib)
endif
$(TargetName): $(AllObjects) $(AttachLib)
	@echo Project:$(ProjectName) create target $(TargetName)
	$(CreateTargetCmd)

$(patsubst %,%.wait,$(AllObjects)):
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectWaitSCPObject.mak -C $(dir $(patsubst $(IntDir)%,$(ProjectDir)%,$@)) $(basename $(notdir $@))

.PHONY : all clean debug release $(ProjectDependList) folders chmods depends objects $(patsubst %,%.wait,$(AllObjects)) $(AllTokenFiles)

clean:
	@echo Project:$(ProjectName) clean
	-rm -f $(AllObjects) $(patsubst %,%.*,$(AllObjects)) $(AllDepends) $(patsubst %,%.*,$(AllDepends)) $(TargetPath) $(GCH) $(GCHDepend) $(IntDir)/*.TokenFile

$(TargetPath): $(AllObjects)
	$(MakeInc)/batscp.sh $(ProjectDir)/$(TokenFile) $(IntDir)/$(NodeIP).TokenFile $(SCPUsername) $(SCPPassword) $(MakeInc) $(OtherNodesIPList)

$(AllTokenFiles):
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectWaitTokenFile.mak $(IntDir)/$@
