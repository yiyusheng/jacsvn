
#当前目录
CurDir := $(shell pwd)
#相对项目的路径
RefPath := $(subst $(ProjectDir),,$(CurDir))
#当前中间目录
CurInt := $(IntDir)/$(RefPath)
#当前目录下的所有子目录
SubDirs := $(shell ls -p | grep -o -P ".+(?=/)")

#源文件
sources := $(wildcard *.cpp)
#二进制目标文件
objects := $(sources:.cpp=.o)
#依赖项文件
depends := $(sources:.cpp=.d)

#需要创建的文件夹
Folders := $(CurInt)

VPATH := $(CurInt):$(ProjectVPATH)

ObjectDepend := $(Folders) depend object $(SubDirs)

objectsAll: $(ObjectDepend)

$(Folders):
	mkdir -p $@

#根据.c文件自动生成依赖项.d文件
depend: $(depends)
$(depends):
	@set -e; rm -f $(CurInt)/$@; \
	$(CXX) -MM $(CPPFLAGS) $(basename $@).cpp > $(CurInt)/$@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $(CurInt)/$@.$$$$ > $(CurInt)/$@; \
	rm -f $(CurInt)/$@.$$$$

#生成二进制目标文件
object: $(objects)
$(objects):
	@echo Project:$(ProjectName) create object $(RefPath)/$@;
	$(CXX) -c $(CPPFLAGS) $(basename $@).cpp -o $(CurInt)/$@

#将生成的.d文件包含在内
-include $(depends:%=$(CurInt)/%)

$(SubDirs):
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectObject.mak -C $@

.PHONY : objectsAll depend object $(SubDirs)

