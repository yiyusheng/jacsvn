
#当前目录
CurDir := $(shell pwd)
#相对项目的路径
RefPath := $(subst $(ProjectDir),,$(CurDir))
#当前中间目录
CurInt := $(IntDir)/$(RefPath)
#当前目录下的所有子目录
SubDirs := $(shell ls -p | grep -o -P ".+(?=/)")

#源文件
sources := $(wildcard *.cpp) $(wildcard *.cxx) $(wildcard *.cc) $(wildcard *.C) $(wildcard *.c)
basenames := $(basename $(sources))
#二进制目标文件
objects := $(addsuffix .o,$(basenames))
#依赖项文件
depends := $(addsuffix .d,$(basenames))

#需要创建的文件夹
Folders := $(CurInt)

VPATH := $(CurInt):$(ProjectVPATH)

ObjectDepend := $(Folders) depend object $(SubDirs)

objectsAll: $(ObjectDepend)

$(Folders):
	-mkdir $@

#根据.cpp文件自动生成依赖项.d文件
depend: $(depends)
$(depends):
	@set -e; rm -f $(CurInt)/$@; \
	$(CXX) -MM $(CPPFLAGS) $(shell find . ! -name "." -type d -prune -o \( -name "$(basename $@).cpp" -o -name "$(basename $@).cxx" -o -name "$(basename $@).cc" -o -name "$(basename $@).C" -o -name "$(basename $@).c" \) -print) > $(CurInt)/$@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $(CurInt)/$@.$$$$ > $(CurInt)/$@; \
	rm -f $(CurInt)/$@.$$$$

#生成二进制目标文件
object: $(objects)
$(objects):
	@echo Project:$(ProjectName) create object $(RefPath)/$@;
	$(CXX) -c $(CPPFLAGS) $(shell find . ! -name "." -type d -prune -o \( -name "$(basename $@).cpp" -o -name "$(basename $@).cxx" -o -name "$(basename $@).cc" -o -name "$(basename $@).C" -o -name "$(basename $@).c" \) -print) -o $(CurInt)/$@

#将生成的.d文件包含在内
-include $(depends:%=$(CurInt)/%)

$(SubDirs):
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectObject.mak -C $@

.PHONY : objectsAll depend object $(SubDirs)

