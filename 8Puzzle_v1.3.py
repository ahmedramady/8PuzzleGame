import ctypes
import random
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from copy import deepcopy
from threading import Thread
from PyQt5 import QtWidgets, QtCore, QtGui
import time
import math


hManhattan = [0, 0, 0, 0, 0, 0, 0, 0, 0]
hEuclidean = [0, 0, 0, 0, 0, 0, 0, 0, 0]
#from PyQt5.uic.properties import QtGui
images = ["tile0.jpg", "tile1.jpg", "tile2.jpg", "tile3.jpg", "tile4.jpg", "tile5.jpg", "tile6.jpg", "tile7.jpg", "tile8.jpg"]
actions = ["Right", "Left", "Up", "Down"]
input_array = [1, 2, 5, 3, 4, 0, 6, 7, 8]
goal_array = [0, 1, 2, 3, 4, 5, 6, 7, 8]
start_time = 0

class Node:
    def __init__(self, data, parent, cost):
        self.data = data
        self.parent = parent
        self.cost = cost

node = Node(input_array, None, 1)
delay = 0.2
textfont = QFont("Verdana", 12, QFont.Bold)


shuffle_arrays =[ [1, 4, 2, 3, 7, 5, 6, 0, 8],
                  [1, 4, 2, 3, 0, 5, 6, 7, 8],
                  [1, 2, 0, 3, 4, 5, 6, 7, 8],
                  [1, 2, 3, 0, 4, 5, 6, 7, 8],
                  [1, 2, 5, 3, 4, 0, 6, 7, 8],
                  [8, 0, 7, 1, 2, 3, 4, 6, 5]]

class gui(QDialog):
    def __init__(self):
        super(gui, self).__init__()
        loadUi('8PuzzleGame.ui',self)
        global images
        #global input_array
        global node
        global delay
        global textFont
        global shuffle_arrays
	self.shuffled_array = []
        self.mode = 1
        #self.numbersradiolineedit.setChecked(True)

        self.tiles = [self.tile0lineedit, self.tile1lineedit, self.tile2lineedit, self.tile3lineedit,
                      self.tile4lineedit, self.tile5lineedit, self.tile6lineedit, self.tile7lineedit,
                      self.tile8lineedit]
        self.image = [QtGui.QImage(images[0]), QtGui.QImage(images[1]), QtGui.QImage(images[2]),
                      QtGui.QImage(images[3]), QtGui.QImage(images[4]), QtGui.QImage(images[5]),
                      QtGui.QImage(images[6]), QtGui.QImage(images[7]), QtGui.QImage(images[8])]
        self.pixmap = [QtGui.QPixmap.fromImage(self.image[0]), QtGui.QPixmap.fromImage(self.image[1]),
                       QtGui.QPixmap.fromImage(self.image[2]), QtGui.QPixmap.fromImage(self.image[3]),
                       QtGui.QPixmap.fromImage(self.image[4]), QtGui.QPixmap.fromImage(self.image[5]),
                       QtGui.QPixmap.fromImage(self.image[6]), QtGui.QPixmap.fromImage(self.image[7]),
                       QtGui.QPixmap.fromImage(self.image[8])]


        self.assignTiles(input_array)
        #self.shuffle()
        self.numbersradiolineedit.toggled.connect(self.setMode1)
        self.tilesradiolineedit.toggled.connect(self.setMode2)
        self.shufflelineedit.clicked.connect(self.shuffle)
        self.startlineedit.clicked.connect(self.start)
	self.shuffle()
        # self.positions = [ [ 10, 20 ]
        #                    [ 80, 20 ]
        #                    [ 150, 20 ]        ]
        # self.tile0lineedit.setGeometry(10,20,71,71)

    def start(self, choice):
        global start_time
        start_time = time.time()
        choice = self.comboboxlineedit.currentIndex()
        if choice == 0:
            self.setStatusText('Please select an algorithm')
            return
        elif choice == 1:
            self.statuslineedit.setText('')
            self.shufflelineedit.setEnabled(False)
            self.startlineedit.setEnabled(False)
            self.tilesradiolineedit.setEnabled(False)
            self.numbersradiolineedit.setEnabled(False)
            time.sleep(0.85)
            self.startBFSThread()

        elif choice == 2:
            self.statuslineedit.setText('')
            self.shufflelineedit.setEnabled(False)
            self.startlineedit.setEnabled(False)
            self.tilesradiolineedit.setEnabled(False)
            self.numbersradiolineedit.setEnabled(False)
            time.sleep(0.85)
            self.startDFSThread()

        elif choice == 3:
            self.statuslineedit.setText('')
            self.shufflelineedit.setEnabled(False)
            self.startlineedit.setEnabled(False)
            self.tilesradiolineedit.setEnabled(False)
            self.numbersradiolineedit.setEnabled(False)
            time.sleep(0.85)
            self.startAStarThread()



    def setMode1(self):
        global input_array
        self.assignTileNumbers(input_array)

    def setMode2(self):
        global input_array
        self.assignTileImages(input_array)

    def startAStarThread(self):
        self.astarthread = Thread(target=self.buildAStarTree)
        self.astarthread.start()
        #self.buildAStarTree()

    def startBFSThread(self):
        self.bfsThread = Thread(target= self.buildBFSTree)
        self.bfsThread.start()
        #self.buildBFSTree()
        #self.statuslineedit.setText('')

    def startDFSThread(self):
        self.dfsThread = Thread(target= self.buildDFSTree)
        #self.dfsThread.start()
        self.buildDFSTree()

    def shuffle(self):
        global input_array, node
        oneeightarr = deepcopy(goal_array)
        randelement = random.randint(0,5)

        input_array = deepcopy(shuffle_arrays[randelement])
	self.shuffled_array = deepcopy(input_array)
        self.assignTiles(self.shuffled_array)
	node = Node(self.shuffled_array, None, 1)


    def setStatusText(self,str):
        self.statuslineedit.setText(str)
        self.statuslineedit.setFont(textfont)

    def assignTileNumbers(self,array):
        self.mode = 1
        font = QFont("Verdana", 35, QFont.Bold)
        self.tile0lineedit.setText(str(array[0]))
        self.tile0lineedit.setFont(font)
        self.tile1lineedit.setText(str(array[1]))
        self.tile1lineedit.setFont(font)
        self.tile2lineedit.setText(str(array[2]))
        self.tile2lineedit.setFont(font)
        self.tile3lineedit.setText(str(array[3]))
        self.tile3lineedit.setFont(font)
        self.tile4lineedit.setText(str(array[4]))
        self.tile4lineedit.setFont(font)
        self.tile5lineedit.setText(str(array[5]))
        self.tile5lineedit.setFont(font)
        self.tile6lineedit.setText(str(array[6]))
        self.tile6lineedit.setFont(font)
        self.tile7lineedit.setText(str(array[7]))
        self.tile7lineedit.setFont(font)
        self.tile8lineedit.setText(str(array[8]))
        self.tile8lineedit.setFont(font)

    def assignTileImages(self, array):
        self.mode = 2
        for element in range(len(array)):
            self.tiles[element].setPixmap(self.pixmap[array[element]])
            self.tiles[element].setScaledContents(True)

    def assignTiles(self,array):
        if self.mode == 1:
            self.assignTileNumbers(array)
        elif self.mode == 2:
            self.assignTileImages(array)

    def move_tiles(self, data):
        pass

    def findIndex(self, array, element):
        for i in range(len(array)):
            if (array[i] == element):
                index = i
        return index

    def displayPuzzle(self, array):
        print("---------")
        print(array[0:3])
        print(array[3:6])
        print(array[6:9])
        print("---------")

    def move_down(self, array):
        arr = deepcopy(array)
        i = self.findIndex(arr, 0)
        down_index = i + 3
        if (down_index > 8):
            return
        else:
            temp = arr[i]
            arr[i] = arr[down_index]
            arr[down_index] = temp
            return arr

    def move_left(self, array):
        arr = deepcopy(array)
        i = self.findIndex(arr, 0)
        left_index = i - 1
        if (left_index == 5 or left_index == 2 or left_index == -1):
            return
        else:
            temp = arr[i]
            arr[i] = arr[left_index]
            arr[left_index] = temp
            return arr

    def move_right(self, array):
        arr = deepcopy(array)
        i = self.findIndex(arr, 0)
        right_index = i + 1
        if (right_index == 3 or right_index == 6 or right_index == 9):
            return
        else:
            temp = arr[i]
            arr[i] = arr[right_index]
            arr[right_index] = temp
            return arr

    def move_up(self, array):
        arr = deepcopy(array)
        i = self.findIndex(arr, 0)
        up_index = i - 3
        if (up_index < 0):
            return
        else:
            temp = arr[i]
            arr[i] = arr[up_index]
            arr[up_index] = temp
            return arr

    def findArrayOrg(self, input_array):
        if (input_array[4] == 0):
            case = 3
        elif (input_array[0] == 0 or input_array[2] == 0 or input_array[6] == 0 or input_array[8] == 0):
            case = 2
        elif (input_array[1] == 0 or input_array[3] == 0 or input_array[5] == 0 or input_array[7] == 0):
            case = 1
        return case

    def movePosition(self, array, action):
        if action == "Left":
            return self.move_left(array)
        elif action == "Right":
            return self.move_right(array)
        elif action == "Up":
            return self.move_up(array)
        elif action == "Down":
            return self.move_down(array)
        else:
            return

    depth_limit = 1000

    def buildBFSTree(self):
	global input_array
        global start_time
        if (node.data == goal_array):
            self.setStatusText("Goal already reached")
            return
        iteration = 0
        explored = []
	input_array = deepcopy(self.shuffled_array)
	print("Shuffled input array is {}".format(input_array))
        explored.append(deepcopy(input_array))
        self.current_node = [node]
        currentIteration = 0
        tempArray = deepcopy(input_array)
        while self.current_node:
            current_root = deepcopy(self.current_node.pop(0))

            for move in range(4):
                tempArray = self.movePosition(current_root.data, actions[move])
                if tempArray is not None:
                    self.child_Node = Node(tempArray, current_root, 0)
                    if self.child_Node.data not in explored:
                        if tempArray is not None:
                            print("Parent Node")
                            self.setStatusText('Parent Node')
                            self.assignTiles((current_root.data))
                            self.displayPuzzle(current_root.data)
                            time.sleep(delay)
                            time.sleep(delay)
                            print("Child Node")
                            self.setStatusText('Child Node')
                            #self.displayPuzzle(current_root.data)
                            #print("Child Nodes")
                            #print("--------")
                        self.current_node.append(self.child_Node)
                        explored.append(deepcopy(self.child_Node.data))
                        self.statuslineedit.setText("Moving " + actions[move])
                        #self.displayPuzzle(child_Node.data)
                        self.assignTiles((self.child_Node.data))
                        self.displayPuzzle((self.child_Node.data))
                        time.sleep(delay)
                        time.sleep(delay)

                        currentIteration += 1
                        if self.child_Node.data == goal_array:
                            #self.assignTiles(deepcopy(self.child_Node.data))
                            self.setStatusText('Successfully completed!')
                            self.shufflelineedit.setEnabled(True)
                            self.startlineedit.setEnabled(True)
                            self.tilesradiolineedit.setEnabled(True)
                            self.numbersradiolineedit.setEnabled(True)
                            print("Cost to goal is: {}".format(len(explored)))
                            self.current_node = []
                            self.child_Node = []
                            end_time = time.time()
                            print("Running time = {}".format(end_time - start_time))
			    print("Depth of tree is {}".format(currentIteration))
                            #print("GOAL REACHED")
                            return
            if (currentIteration > 5000):
                self.shufflelineedit.setEnabled(True)
                self.startlineedit.setEnabled(True)
                self.tilesradiolineedit.setEnabled(True)
                self.numbersradiolineedit.setEnabled(True)
                self.setStatusText('Exceeded maximum number of iterations')
                self.current_node = []
                self.child_Node = []
                return
                currentIteration = 0

    def buildDFSTree(self):
	global input_array
	depth = 0
	depthArray = []
        global start_time
        nodeCost = []
        rootCost = []

        if (node.data == goal_array):
            self.setStatusText("Goal already reached")
            return
        iteration = 0
        explored = []
        explored.append(deepcopy(input_array))
        self.current_node = [node]
        currentIteration = 0
        while self.current_node:
            current_root = [self.current_node.pop(0)]
            rootCost.append(current_root)
            #print(current_root)
            while current_root:
		#depth = 0
                current_ext_node = current_root.pop(0)
                #print(current_ext_node.data)
                for move in range(4):
                    if deepcopy(current_ext_node.data) is not None:
                        self.setStatusText('Parent Node')
                        print("Parent Node")
                        self.assignTiles(current_ext_node.data)
                        self.displayPuzzle(current_ext_node.data)
                        time.sleep(delay)
                        print('Child Node')
                        self.setStatusText('Child Node')
                    tempArray = deepcopy(current_ext_node.data)
                    tempArray = self.movePosition(deepcopy(tempArray), actions[move])
                    if tempArray is not None:
                        if tempArray not in explored:
                            #current_ext_node.data = deepcopy(tempArray)
                            # tempArray = deepcopy(current_ext_node.data)
                            self.child_Node = Node(tempArray, current_ext_node, 0)
                            nodeCost.append(current_ext_node)
                            # self.displayPuzzle(current_root.data)
                                # print("Child Nodes")
                                # print("--------")
                            #current_ext_node.append(self.child_Node)
                            current_root.append(self.child_Node)
                            explored.append(deepcopy(self.child_Node.data))
                            self.statuslineedit.setText("Moving " + actions[move])
                            self.displayPuzzle(self.child_Node.data)
                            self.assignTiles(deepcopy(self.child_Node.data))
                            time.sleep(delay)
                            if self.child_Node.data == goal_array:
                                # self.assignTiles(deepcopy(self.child_Node.data))
                                self.setStatusText('Successfully completed!')
                                self.startlineedit.setEnabled(True)
                                self.shufflelineedit.setEnabled(True)
                                self.tilesradiolineedit.setEnabled(True)
                                self.numbersradiolineedit.setEnabled(True)
                                self.current_node = []
                                self.child_Node = []
                                current_root = []
                                # print("GOAL REACHED")
                                print("Cost to goal is: {}".format(len(rootCost) + len(nodeCost)))
                                end_time = time.time()
                                print("Running time = {}".format(end_time - start_time))
				print("Depth of tree is {}".format(currentIteration))
                                rootCost = []
                                nodeCost = []
                                return
	        depth+=1
                currentIteration += 1
                self.current_node.append(current_ext_node)
                if currentIteration > 6000:
                    currentIteration = 0
                    self.setStatusText('Exceeded maximum number of levels')
                    self.startlineedit.setEnabled(True)
                    self.shufflelineedit.setEnabled(True)
                    self.tilesradiolineedit.setEnabled(True)
                    self.numbersradiolineedit.setEnabled(True)
                    self.current_node = []
                    self.child_Node = []
                    return

	    depthArray.append(deepcopy(depth))
	    depth=0


    def get_cost(self, input_array, goal_array):
        for i in range(0, 9):

            if i % 3 == 0:
                cCol = 0

            elif (i - 1) % 3 == 0:
                cCol = 1

            else:
                cCol = 2

            if i < 3:
                cRow = 0
            elif i < 6:
                cRow = 1
            else:
                cRow = 2

            if goal_array[input_array[i]] % 3 == 0 and (input_array[i] - 1) > -1:
                Gcol = 0
            elif (goal_array[input_array[i]] - 1) % 3 == 0 and (input_array[i] - 1) > -1:
                Gcol = 1
            else:
                Gcol = 2

            if goal_array[input_array[i]] < 3 and (input_array[i] - 1) > -1:
                GRow = 0
            elif goal_array[input_array[i]] < 6 and (input_array[i] - 1) > -1:
                GRow = 1
            # elif Goal[Current[i]-1] < 9 and (Current[i]-1) > -1:
            else:
                GRow = 2

            # print(cRow, GRow, cCol, Gcol)
            hEuclidean[i] = math.sqrt((cRow - GRow) ** 2 + (cCol - Gcol) ** 2)
            hManhattan[i] = abs(cRow - GRow) + abs(cCol - Gcol)
            if input_array[i] == 0:
                hEuclidean[i] = 0
                hManhattan[i] = 0
        # print("Manhattan distance", hManhattan)
        # print("Euclidean distance", hEuclidean)
        # print(sum(hManhattan))
        # print(sum(hEuclidean))

        return sum(hManhattan)

    def pop_all(self, l):
        r, l[:] = l[:], []
        return r

    def find_node(self, level_nodes, minCost):
        for i in range(len(level_nodes)):
            if level_nodes[i].cost == minCost:
                return level_nodes[i]

    def buildAStarTree(self):
	global input_array
        global start_time
        if(node.data == goal_array):
            self.setStatusText("Goal already reached")
            return
        explored = []
        node.cost = 0
        path_to_goal = []
        cost = 0
        cost_arr = []
        level_nodes = []
        explored.append(input_array)
        current_node = [node]
        currentIteration = 0
        tempArray = deepcopy(input_array)
        while current_node:
            path_to_goal.append(current_node)

            current_root = (deepcopy(current_node.pop(0)))

            for move in range(4):
                tempArray = self.movePosition(current_root.data, actions[move])
                if tempArray is not None:
                    child_Node = Node(tempArray, current_root, cost)
                    if child_Node.data not in explored:
                        if tempArray is not None:
                            print("Parent Node")
                            self.setStatusText('Parent Node')
                            self.assignTiles(current_root.data)
                            self.displayPuzzle(current_root.data)
                            time.sleep(delay)
                            print("Child Node")
                            self.setStatusText('Child Node')
                            print("--------")

                        explored.append(deepcopy(child_Node.data))
                        #print("Moving " + actions[move])
                        cost = self.get_cost(child_Node.data, goal_array)
                        print("Cost of node is {}".format(cost))
                        child_Node.cost = cost
                        #print("Cost of node")
                        #print(child_Node.cost)
                        cost_arr.append(child_Node.cost)
                        #print("Cost array ", cost_arr)
                        min_child_Node = child_Node.cost
                        #print(child_Node.cost)
                        #print("the minimum node of all nodes     ", child_Node.data)
                        self.assignTiles(child_Node.data)
                        self.displayPuzzle(child_Node.data)
                        time.sleep(delay)
                        currentIteration += 1
                        if child_Node.data == goal_array:
                            print("GOAL REACHED")
                            self.setStatusText('Successfully completed!')
                            self.startlineedit.setEnabled(True)
                            self.shufflelineedit.setEnabled(True)
                            self.tilesradiolineedit.setEnabled(True)
                            self.numbersradiolineedit.setEnabled(True)
                            print("Cost to path is {}".format(len(path_to_goal)))
                            self.current_node = []
                            self.child_Node = []
                            explored = []
                            end_time = time.time()
                            print("Running time = {}".format(end_time - start_time))
			    print("Depth of tree is {}".format(currentIteration))
                            return
                        level_nodes.append(child_Node)
            if len(cost_arr) > 0:
                minCost_ele = min(cost_arr)
                #print("the minimium node is     ", minCost_ele)
                tempNode = self.find_node(level_nodes, minCost_ele)
                current_node.append(tempNode)
                self.pop_all(level_nodes)
                self.pop_all(cost_arr)

            if (currentIteration > 3):
                pass
                # currentIteration = 0


def main():
    main_app=QApplication(sys.argv)
    window=gui()
    window.setWindowTitle('8 Puzzle Game')
    window.show()
    #buildDFSTree(node)
    sys.exit(main_app.exec_())
if __name__ == '__main__':
    main()
