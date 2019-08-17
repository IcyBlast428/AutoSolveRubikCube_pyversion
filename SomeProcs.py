def resetAll(grp, jobNumber):
    cmds.scriptJob(kill = jobNumber, force = True)
    cmds.currentTime(0)
    rootGrp = grp
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                cmds.parent(cmds.parent(("_" + str(i) + str(j) + str(k)), relative = True, world = True), rootGrp, relative = True)
    cmds.delete(rootGrp + "|group*")
    cmds.select(cl = True)
    cmds.playbackOptions(animationStartTime = 0, minTime = 0, maxTime = 6, animationEndTime = 6)
    # rubik = initializeRubik()
    # rubikRotation = initializeRotation()
    return initializeRubik(), initializeRotation()

def doGrp(cube):
    fullpath = cmds.listRelatives(cube, fullPath = True)
    topGroup = re.compile(r'[^|Rubiks|][^|]*').search(fullpath[0]).group()
    return cmds.group(topGroup)


def mvGrpPiv(grpName, cubePiv):
    grpPivot = cmds.xform(grpName, query = True, piv = True, ws = True)
    cmds.move((cubePiv[0]-grpPivot[0]), (cubePiv[1]-grpPivot[1]), (cubePiv[2]-grpPivot[2]), (str(grpName) + ".scalePivot"), (str(grpName) + ".rotatePivot"), relative = True)

def setKeyFrm(grpName, currentFrm, x, y, z):
    cmds.setKeyframe(grpName, at = ['rotateX', 'rotateY', 'rotateZ'], t = currentFrm)
    cmds.rotate(x, y, z, grpName, r = True)
    cmds.setKeyframe(grpName, at = ['rotateX', 'rotateY', 'rotateZ'], t = (currentFrm + 6))

def mvTimelinePointer(currentFrm):
    currentFrm += 6
    cmds.playbackOptions(animationStartTime = 0, minTime = 0, maxTime = currentFrm, animationEndTime = currentFrm)
    cmds.play(forward = True)
    return currentFrm




