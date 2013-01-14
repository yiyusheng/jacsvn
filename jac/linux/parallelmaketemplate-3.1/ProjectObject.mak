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

ObjectDepend := wait object next

waitObjects := $(workingObjects)
workingObjects := $(wordlist 1,$(ConcurrentJobs),$(allResponsibleObjects))
allResponsibleObjects := $(filter-out $(workingObjects),$(allResponsibleObjects))

objectsAll: $(ObjectDepend)

wait: $(waitObjects)

$(waitObjects):
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectWaitCreateObject.mak -C $(dir $(patsubst $(IntDir)%,$(ProjectDir)%,$@)) $(notdir $@)

object: $(workingObjects)

$(workingObjects):
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectCreateObject.mak -C $(dir $(patsubst $(IntDir)%,$(ProjectDir)%,$@)) $(notdir $@).create &

nextTarget := $(if $(firstword $(workingObjects)),nextTarget)

next: $(nextTarget)

nextTarget:
	@$(Make) $(MGLAGS) -f $(MakeInc)/ProjectObject.mak

.PHONY : objectsAll wait object $(waitObjects) $(workingObjects) next nextTarget

