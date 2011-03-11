
VPATH := $(VPATH):$(CurInt)

object: $(objects)
	@echo Project:$(ProjectName) create objects success! Path:$(RefPath)

.PHONY : object

#将生成的.d文件包含在内
include $(depends:%=$(CurInt)/%)

