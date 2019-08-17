def FaceController():
    sel = cmds.ls(sl = True)
    color = re.compile(r'^[^_]+').search(sel[0]).group()
    direction = re.compile(r'[^_]+$').search(sel[0]).group()
    print(color, direction)
    if color == "blue":
        if direction == "clockwise":
            #mel.eval('rubikRotation("blue", 1)')
            RubikRotation("blue", 1)
        else:
            #mel.eval('rubikRotation("blue", 0)')
            RubikRotation("blue", 0)
    elif color == "orange":
        if direction == "clockwise":
            #mel.eval('rubikRotation("orange", 1)')
            RubikRotation("orange", 1)
        else:
            #mel.eval('rubikRotation("orange", 0)')
            RubikRotation("orange", 0)
    elif color == "green":
        if direction == "clockwise":
            #mel.eval('rubikRotation("green", 1)')
            RubikRotation("green", 1)
        else:
            #mel.eval('rubikRotation("green", 0)')
            RubikRotation("green", 0)
    elif color == "red":
        if direction == "clockwise":
            #mel.eval('rubikRotation("red", 1)')
            RubikRotation("red", 1)
        else:
            #mel.eval('rubikRotation("red", 0)')
            RubikRotation("red", 0)
    elif color == "yellow":
        if direction == "clockwise":
            #mel.eval('rubikRotation("yellow", 1)')
            RubikRotation("yellow", 1)
        else:
            #mel.eval('rubikRotation("yellow", 0)')
            RubikRotation("yellow", 0)
    elif color == "white":
        if direction == "clockwise":
            #mel.eval('rubikRotation("white", 1)')
            RubikRotation("white", 1)
        else:
            #mel.eval('rubikRotation("white", 0)')
            RubikRotation("white", 0)
