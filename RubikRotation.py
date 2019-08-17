def RubikRotation(face, cw):
    global rubik
    #global rubikRotation
    cmds.currentTime(numberOfRotation(rubikRotation) * 6)
    curFrame = cmds.currentTime(query = True)
    cubePivot = cmds.xform('_222', query = True, piv = True, ws = True)
    clockwise = cw
    print(face, cw)
    if face == 'white':
        sel = selection(face)
        for i in range(len(sel)):
            grp = doGrp(sel[i])
            cmds.select(cl = True)
            mvGrpPiv(grp, cubePivot)
            setKeyFrm(grp, curFrame, 0, (math.pow(-1, clockwise)*90), 0)
        curFrame = mvTimelinePointer(curFrame)
        #rubik = rotateFace(rubik, face = face, cw = clockwise)
        rubik = rotateFace(rubik, face = face, cw = clockwise)
    elif face == 'orange':
        sel = selection(face)
        print(sel)
        for i in range(len(sel)):
            grp = doGrp(sel[i])
            cmds.select(cl = True)
            mvGrpPiv(grp, cubePivot)
            setKeyFrm(grp, curFrame, (math.pow(-1, clockwise)*(-90)), 0, 0)
        curFrame = mvTimelinePointer(curFrame)
        #global rubik = rotateFace(rubik, face = face, cw = clockwise)
        #global rubik
        rubik = rotateFace(rubik, face = face, cw = clockwise)
    elif face == 'blue':
        sel = selection(face)
        for i in range(len(sel)):
            grp = doGrp(sel[i])
            cmds.select(cl = True)
            mvGrpPiv(grp, cubePivot)
            setKeyFrm(grp, curFrame, 0, 0, (math.pow(-1, clockwise)*90))
        curFrame = mvTimelinePointer(curFrame)
        #global rubik = rotateFace(rubik, face = face, cw = clockwise)
        #global rubik
        rubik = rotateFace(rubik, face = face, cw = clockwise)
    elif face == 'red':
        sel = selection(face)
        for i in range(len(sel)):
            grp = doGrp(sel[i])
            cmds.select(cl = True)
            mvGrpPiv(grp, cubePivot)
            setKeyFrm(grp, curFrame, (math.pow(-1, clockwise)*90), 0, 0)
        curFrame = mvTimelinePointer(curFrame)
        #global rubik = rotateFace(rubik, face = face, cw = clockwise)
        #global rubik
        rubik = rotateFace(rubik, face = face, cw = clockwise)
    elif face == 'green':
        sel = selection(face)
        for i in range(len(sel)):
            grp = doGrp(sel[i])
            cmds.select(cl = True)
            mvGrpPiv(grp, cubePivot)
            setKeyFrm(grp, curFrame, 0, 0, (math.pow(-1, clockwise)*(-90)))
        curFrame = mvTimelinePointer(curFrame)
        #global rubik = rotateFace(rubik, face = face, cw = clockwise)
        #global rubik
        rubik = rotateFace(rubik, face = face, cw = clockwise)
    elif face == 'yellow':
        sel = selection(face)
        for i in range(len(sel)):
            grp = doGrp(sel[i])
            cmds.select(cl = True)
            mvGrpPiv(grp, cubePivot)
            setKeyFrm(grp, curFrame, 0, (math.pow(-1, clockwise)*90), 0)
        curFrame = mvTimelinePointer(curFrame)
        #global rubik = rotateFace(rubik, face = face, cw = clockwise)
        #global rubik
        rubik = rotateFace(rubik, face = face, cw = clockwise)
