
VPATH := $(ProjectVPATH):$(CurInt)

object: $(objects)

.PHONY : object

#将生成的.d文件包含在内
include $(depends:%=$(CurInt)/%)

