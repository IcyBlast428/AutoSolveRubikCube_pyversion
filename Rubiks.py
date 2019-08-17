from pymel.core import *
import maya.cmds as cmds
import maya.mel as mel
import re
import math

# Initialize Rubik's cube
def initializeRubik():
    
    # Each face is represented as a two-dimensional list
    # 1st value is the absolutely position of each face
    # 2nd value is the absolutely position that the first value position face moves to
    # 3rd value is the current absolutely position occupied by which first value position face
    white  = [ ['w_o_b_111', None, None], ['w_b_112', None, None], ['w_b_r_113', None, None],
               ['w_o_121', None, None], ['w_122', None, None], ['w_r_123', None, None],
               ['w_g_o_131', None, None], ['w_g_132', None, None], ['w_r_g_133', None, None] ]
               
    orange = [ ['o_w_g_131', None, None], ['o_w_121', None, None], ['o_b_w_111', None, None],
               ['o_g_231', None, None], ['o_221', None, None], ['o_b_211', None, None],
               ['o_g_y_331', None, None], ['o_y_321', None, None], ['o_y_b_311', None, None] ]
               
    blue   = [ ['b_w_o_111', None, None], ['b_w_112', None, None], ['b_r_w_113', None, None],
               ['b_o_211', None, None], ['b_212', None, None], ['b_r_213', None, None],
               ['b_o_y_311', None, None], ['b_y_312', None, None], ['b_y_r_313', None, None] ]
               
    red    = [ ['r_w_b_113', None, None], ['r_w_123', None, None], ['r_g_w_133', None, None],
               ['r_b_213', None, None], ['r_223', None, None], ['r_g_233', None, None],
               ['r_b_y_313', None, None], ['r_y_323', None, None], ['r_y_g_333', None, None] ]
               
    green  = [ ['g_w_r_133', None, None], ['g_w_132', None, None], ['g_o_w_131', None, None],
               ['g_r_233', None, None], ['g_232', None, None], ['g_o_231', None, None],
               ['g_r_y_333', None, None], ['g_y_332', None, None], ['g_y_o_331', None, None] ]
               
    yellow = [ ['y_b_o_311', None, None], ['y_b_312', None, None], ['y_r_b_313', None, None],
               ['y_o_321', None, None], ['y_322', None, None], ['y_r_323', None, None],
               ['y_o_g_331', None, None], ['y_g_332', None, None], ['y_g_r_333', None, None] ]

    # 'rubik' is a dictionary with face color key and face status value
    rubik = {"white" : white,
             "orange": orange,
             "blue"  : blue,
             "red"   : red,
             "green" : green,
             "yellow": yellow}
    
    # Initialize the last two values as same as the first value
    for colour in rubik.values():
        for i in range(len(colour)):
            colour[i][1] = colour[i][0]
            colour[i][2] = colour[i][0]
    
    # Retuen rubik's
    return rubik

# Record the count of clockwise or anticlockwise rotation for each face,
# The first value represents clockwise rotation, the second value represents anticlockwise rotation.
def initializeRotation():
    white  = [0, 0]
    orange = [0, 0]
    blue   = [0, 0]
    red    = [0, 0]
    green  = [0, 0]
    yellow = [0, 0]
    rubikRotation = {'white' : white,
                     'orange': orange,
                     'blue'  : blue,
                     'red'   : red,
                     'green' : green,
                     'yellow': yellow}
    return rubikRotation

# What other faces will be affected when rotating a face.
# Dictionary: key -> rotating face
#             value -> associated faces list
def associatedRotationFace():
    associatedRotation = {
        'white' :['green' ,'blue' ,'orange','red'],
        'blue'  :['yellow','white','orange','red'],
        'orange':['yellow','white','green' ,'blue'],
        'green' :['yellow','white','red'   ,'orange'],
        'red'   :['yellow','white','blue'  ,'green'],
        'yellow':['green' ,'blue' ,'orange','red'] }
    return associatedRotation

def transpose(det):
    newDet = []
    for i in range(len(det[0])):
        newDet.append([row[i] for row in det])
    return newDet

# Show the current state of rubik
def displayRubik(rubik):
    for colour in rubik.keys(): # scan each face
        print(colour, ':')   # show face name
        for value in rubik[colour]: # scan each tile in the face
            print(value)    # print each tile's value
    print('\n\n')   #

# set the 2nd value for all cubes
def setSecondValue(rubik):
    newRubik = rubik   # get the rubik object
    for outerIterationFace in newRubik.keys(): # iterate all the face color
        for outerIterationCube in newRubik[outerIterationFace]: # iterate all the cubes in one face
            for innerIterationFace in newRubik.keys():  # iterate all the face color
                for innerIterationCube in newRubik[innerIterationFace]: # iterate all the cubes in one face
                    # if the 3rd value of outer iteration cube equals to the 1st value of inner iteration cube
                    if newRubik[innerIterationFace][newRubik[innerIterationFace].index(innerIterationCube)][0] == newRubik[outerIterationFace][newRubik[outerIterationFace].index(outerIterationCube)][2]:
                        # set the 2nd value of inner iteration cube to the 1st value of outer iteration cube
                        newRubik[innerIterationFace][newRubik[innerIterationFace].index(innerIterationCube)][1] = newRubik[outerIterationFace][newRubik[outerIterationFace].index(outerIterationCube)][0]
    return newRubik

# Rotate face
# arguments:
#   rubik: rubik object
#   face:  rotate face color, Data type: string, values: ('white', 'orange', 'blue', 'red', 'green', 'yellow')
#   cw:    rotate direction, Data type: boolean, values: (True, False), True: clockwise, False: anticlockwise
def rotateFace(rubik, face, cw):
    rotateFaceColor = face  # rotateFaceColor:string
    clockwise = cw  # clockwise:boolean
    needRotateFaceCubes = []    # 1D vector which saves faces need to be rotated
    beforeRotationWithoutAssociatedFace = [[], [], []] # 3 by 3 matrix
    beforeRotationWithAssociatedFace = [[],[],[],[],[]] # 5 by 5 matrix

    # set the rotate cube with 3rd value
    # [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in rubik[rotateFaceColor]:
        needRotateFaceCubes.append(i[2])

    # convert 1D vector to 2D matrix
    #                                  [ [1, 2, 3]
    # [1, 2, 3, 4, 5, 6, 7, 8, 9]   =>   [4, 5, 6]
    #                                    [7, 8, 9] ]
    for i in range(3):
        for j in range(3):
            beforeRotationWithoutAssociatedFace[i].append(needRotateFaceCubes[i * 3 + j])

    # reverse 2D matrix
    # [ [7, 8, 9]
    #   [4, 5, 6]
    #   [1, 2, 3] ]
    #beforeRotationWithoutAssociatedFace = np.array(beforeRotationWithoutAssociatedFace)[::-1]
    beforeRotationWithoutAssociatedFace = beforeRotationWithoutAssociatedFace[::-1]

    # make a 5 by 5 matrix with all '-----' elements
    # [ ['-----', '-----', '-----', '-----', '-----']
    #   ['-----', '-----', '-----', '-----', '-----']
    #   ['-----', '-----', '-----', '-----', '-----']
    #   ['-----', '-----', '-----', '-----', '-----']
    #   ['-----', '-----', '-----', '-----', '-----'] ]
    for i in range(5):
        for _ in range(5):
            beforeRotationWithAssociatedFace[i].append('-----')
    
    # insert 3 by 3 matrix into 5 by 5 matrix in the center
    # [ ['-', '-', '-', '-', '-']
    #   ['-', '7', '8', '9', '-']
    #   ['-', '4', '5', '6', '-']
    #   ['-', '1', '2', '3', '-']
    #   ['-', '-', '-', '-', '-'] ]
    for i in range(1, 4): # from the row of second
        for j in range(1, 4): # from the column of second
            beforeRotationWithAssociatedFace[i][j] = beforeRotationWithoutAssociatedFace[i - 1][j - 1]

    # create associated cubes list which links to the cubes that in the rotating face
    # according to the associatedRotation list
    # the first value in each element is the rotating face cube
    # the second value in each elemtnt is the associated cube in other face
    # [ [w_1, b_1]
    #   [w_2, b_4]
    #   [w_3, b_3]
    #   [w_7, g_7]
    #      ....    ]  
    # 12 elements (3 cubes/side * 4 sides) for a 3-level rubik 
    associatedCubes = []
    for color in associatedRotation[rotateFaceColor]: # get all associated faces
        for i in rubik[color]: # scan all associated faces in rubik object
            for j in needRotateFaceCubes: # scan all cubes in the rorating face
                if re.split(r"_",i[2])[-1] == re.split(r"_",j)[-1]: # if the cube index number are same
                    associatedCubes.append([j, i[2]]) # make them as a list and insert
    
    # insert the associated cubes into the beforeRotationWithAssociatedFace list
    # [ ['---', 'g_7', 'g_8', 'g_9', '---']
    #   ['o_7', 'w_7', 'w_8', 'w_9', 'r_9']
    #   ['o_4', 'w_4', 'w_5', 'w_6', 'r_6']
    #   ['o_1', 'w_1', 'w_2', 'w_3', 'r_3']
    #   ['---', 'b_1', 'b_2', 'b_3', '---'] ]
    for i in range(12): # scan all elements in the associatedCubes list
        for j in range(1,4): # from the second row to the last but one row
            for k in range(1,4): # from the second column to the last but one column
                if beforeRotationWithAssociatedFace[j][k] == associatedCubes[i][0]: 
                    if i in range(3): # 3 top elements
                        beforeRotationWithAssociatedFace[j - 1][k] = associatedCubes[i][1]
                    if i in range(3, 6): # 3 bottom elements
                        beforeRotationWithAssociatedFace[j + 1][k] = associatedCubes[i][1]
                    if i in range(6, 9): # 3 left elements
                        beforeRotationWithAssociatedFace[j][k - 1] = associatedCubes[i][1]
                    if i in range(9, 12): # 3 right elements
                        beforeRotationWithAssociatedFace[j][k + 1] = associatedCubes[i][1]
    
    # determine whether clockwise or anticlockwise
    # clockwise:                                 anticlockwise:
    # [ ['---', 'o_1', 'o_4', 'o_7', '---']      [ ['---', 'r_9', 'r_6', 'r_3', '---']
    #   ['b_1', 'w_1', 'w_4', 'w_7', 'g_7']        ['g_9', 'w_9', 'w_6', 'w_3', 'b_3']
    #   ['b_2', 'w_2', 'w_5', 'w_8', 'g_8']        ['g_8', 'w_8', 'w_5', 'w_2', 'b_2']
    #   ['b_3', 'w_3', 'w_6', 'w_9', 'g_9']        ['g_7', 'w_7', 'w_4', 'w_1', 'b_1']
    #   ['---', 'r_3', 'r_6', 'r_9', '---'] ]      ['---', 'o_7', 'o_4', 'o_1', '---'] ]
    if clockwise:
        #afterRotationWithAssociatedFace = np.array(beforeRotationWithAssociatedFace)[::-1].T  # 3 by 3 matrix rotate in clockwise, reverse matrix first, then transpose
        afterRotationWithAssociatedFace = transpose(beforeRotationWithAssociatedFace[::-1])
        rubikRotation[rotateFaceColor][0] += 1  # clockwise counter increase
    else:
        #afterRotationWithAssociatedFace = np.array(beforeRotationWithAssociatedFace).T[::-1]  # 3 by 3 matrix rotate in anticlockwise, transpose matrix first, then reverse
        afterRotationWithAssociatedFace = transpose(beforeRotationWithAssociatedFace)[::-1]
        rubikRotation[rotateFaceColor][1] += 1  # anticlockwise counter increase
    
    # mapping list is a list that contains 25 elements (includes 4 ['-----', ['-----'] pairs),
    # 21 elements are valid, 9 of 21 elements are the rotating face information, 12 of 21 are associated face information
    # mapping list is used to set the 3rd value in the rubik
    #
    # beforeRotationWithAssociatedFace:          afterRotationWithAssociatedFace:
    # [ ['---', 'g_7', 'g_8', 'g_9', '---']      [ ['---', 'o_1', 'o_4', 'o_7', '---']
    #   ['o_7', 'w_7', 'w_8', 'w_9', 'r_9']        ['b_1', 'w_1', 'w_4', 'w_7', 'g_7']
    #   ['o_4', 'w_4', 'w_5', 'w_6', 'r_6']        ['b_2', 'w_2', 'w_5', 'w_8', 'g_8']
    #   ['o_1', 'w_1', 'w_2', 'w_3', 'r_3']        ['b_3', 'w_3', 'w_6', 'w_9', 'g_9']
    #   ['---', 'b_1', 'b_2', 'b_3', '---'] ]      ['---', 'r_3', 'r_6', 'r_9', '---'] ]
    #             ↑------------------------------------------↑
    # mapping:
    # [ ['---', '---'],
    #   ['g_7', 'o_1'],
    #   ['g_8', 'o_4'],
    #   ['g_9', 'o_7'],
    #     ..........
    #   ['b_3', 'r_9'],
    #   ['---', '---'] ]
    mapping = []
    for i in range(5):
        for j in range(5):
            mapping.append([beforeRotationWithAssociatedFace[i][j], afterRotationWithAssociatedFace[i][j]])
    
    # set new values to the 3rd value in rubik
    excludeList = [] # scaned cubes list, no longer to consider
    for i in range(len(mapping)): # scan all elements in the mapping list
        for color in rubik.keys(): # scan all faces
            for cube in rubik[color]: # scan all cubes in the face
                excludeItem = color + '_' + str(rubik[color].index(cube)) # record the scaned cube
                if cube[2] == mapping[i][0] and excludeItem not in excludeList: # if find the cube and it is not in excludeList
                    rubik[color][rubik[color].index(cube)][2] = mapping[i][1] # set the new value
                    excludeList.append(excludeItem) # add to excludeList

    rubik = setSecondValue(rubik)  # set the 2nd value for all faces
    return rubik    # return the latest rubik object

# number of rotation
def numberOfRotation(obj):
    number = 0
    for color in obj.keys():
        for value in obj[color]:
            number += value
    return number


# SELECT CUBES THAT NEED TO ROTATE
def selection(face):
    #select(cl = True) # clear all selections
    selectedCube = []
    for cube in rubik[face]: # iterate all cubes in one face
        #select(re.search(r".\d+", cube[2]).group(), add = True) # select 3rd value faces
        #print(cube)
        selectedCube.append(re.search(r".\d+", cube[2]).group())
    #return ls(sl=1) # return selections
    return selectedCube

# instantiate a rubik's cube and related rotation information
rubik = initializeRubik()
rubikRotation = initializeRotation()
associatedRotation = associatedRotationFace()

