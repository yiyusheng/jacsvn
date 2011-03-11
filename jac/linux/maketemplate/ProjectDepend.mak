#当前目录
export CurDir := $(shell pwd)
#相对项目的路径
export RefPath := $(subst $(ProjectDir),,$(CurDir))
#当前中间目录
export CurInt := $(IntDir)/$(RefPath)
#当前目录下的所有子目录
SubDirs := $(patsubst %/,%,$(shell ls -d */))

#源文件
export sources := $(wildcard *.cpp)
#二进制目标文件
export objects := $(sources:.cpp=.o)
#信赖项文件
export depends := $(sources:.cpp=.d)
#需要创建的文件夹
Folders := $(CurInt)

ObjectDepend := $(Folders) depend SubObjects $(SubDirs)

objects: $(ObjectDepend)
	@echo Project:$(ProjectName) create depends success! Path:$(RefPath)

$(Folders):
	-mkdir $@

#根据.c文件自动生成依赖项.d文件
depend: $(depends)
$(depends):%.d: %.cpp
	@set -e; rm -f $@; \
	$(CXX) -MM $(CPPFLAGS) $< >> $(CurInt)/$@; \
	echo "	$(CXX) -c $(CPPFLAGS) $< -o $(CurInt)/$*.o" >> $(CurInt)/$@;


SubObjects:
	$(Make) -f $(MakeInc)/ProjectObject.mak

$(SubDirs):
	$(Make) -f $(MakeInc)/ProjectDepend.mak -C $@

.PHONY : objects depend SubObjects $(SubDirs)
