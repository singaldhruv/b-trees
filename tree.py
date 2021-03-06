#Code for the second assignment of CS315
#Dhruv Singal 12243
import os
import datetime
import math



class StatsAggregator:
    def __init__(self):
        self.max = 0
        self.min = 0
        self.num = 0
        self.sum = 0
        self.sumSquare = 0
    
    def average(self):
        if self.num == 0:
            return 0

        return float(float(self.sum)/float(self.num))

    def deviation(self):
        if self.num == 0:
            return 0

        return math.sqrt((float(self.sumSquare)/float(self.num)) - (self.average())*(self.average()))

    def update(self,value):
        self.num += 1
        self.sum+=value
        self.sumSquare+=value*value
    
        if self.num == 1:
            self.max = value
            self.min = value
            return

        if self.max < value:
            self.max = value

        if self.min > value:
            self.min = value

        return


    def printStats(self):
        print "Max: %d"%self.max
        print "Min: %d"%self.min
        print "Average: %f"%self.average()
        print "Standard Deviation: %f"%self.deviation()




class Node:

    #Create a node object by reading from the file
    def __init__(self,nodeNo):
        global currentAccessCounter
        currentAccessCounter += 1

        self.nodeNo = 0
        self.keys = []
        self.children = []
        self.parent = 0
        self.next = 0
        self.prev = 0
        self.leaf = False

        if not os.path.isfile("./data/"+str(nodeNo)+".dat"):
            error("ERROR, node %d data not found"%nodeNo)
        
        with open("data/"+str(nodeNo) + ".dat") as nodeFile:
            lines = nodeFile.readlines()
            if lines[0].split()[0] != 'node':
                error("ERROR, file %d.dat is not a tree node"%nodeNo)
            self.nodeNo = nodeNo
            for line in lines[1:]:
                s = line.split()
                if s[0]=='keys':
                    for key in s[1:]:
                        self.keys.append(float(key))
                elif s[0]=='children':
                    for child in s[1:]:
                        self.children.append(int(child))
                elif s[0]=='parent':
                    self.parent=int(s[1])
                elif s[0]=='leaf':
                    self.leaf = (s[1]!='0')
                elif s[0]=='next':
                    self.next = int(s[1])
                elif s[0]=='prev':
                    self.prev = int(s[1])

    #Prints all the values of the node
    def printValues(self):
        print "******NODE********"
        print "nodeNo: ",self.nodeNo
        print "keys: ",self.keys
        print "children: ", self.children
        print "parent: ",self.parent
        print "next: ",self.next
        print "prev: ",self.prev
        print "isLeaf: ",self.isLeaf()
        print "isRoot: ",
        print self.isRoot()

    #Returns the number of keys in the tree node
    def numKeys(self):
        return len(self.keys)

    def isLeaf(self):
        return self.leaf

    def isRoot(self):
        return self.parent == 0

    def maxKey(self):
        return self.keys[-1]

    def updateKey(self,index,newKey):
        self.keys[index]=newKey
        return

    #Add a key/data pair to a leaf of the tree
    def addDataToLeaf(self,key,data):
        if not self.isLeaf():
            error("Can't add data to a non-leaf node %d"%self.nodeNo)
        
        global blockSize
        newDataNode = createDataNode([key],[data],self.nodeNo)
        i = 0
        for i in range(0,self.numKeys()):
            if self.keys[i]>key:
                break
        if self.maxKey()<=key:
            i = self.numKeys()
        maxKey = self.maxKey()

        self.keys.insert(i,key)
        self.children.insert(i,newDataNode)

        if self.numKeys() <= blockSize:
            self.writeToDisk()
            #Update the key in the path from root to this leaf
            if i==self.numKeys():
                updateRec(self.parent,self.nodeNo)

        #split the node and add key to parent and so on
        else:
            splitRec(self.nodeNo)

    #Write back the node data to disk
    def writeToDisk(self):
        with open("data/"+str(self.nodeNo)+".dat",'w+') as nodeFile:
            nodeFile.write("node %d\n"%self.nodeNo)
            nodeFile.write("keys")
            for key in self.keys:
                nodeFile.write(" "+str(key))
            nodeFile.write("\nchildren")
            for child in self.children:
                nodeFile.write(" "+str(child))
            nodeFile.write("\nparent %d"%self.parent)
            nodeFile.write("\nnext %d"%self.next)
            nodeFile.write("\nprev %d"%self.prev)
            nodeFile.write("\nleaf ")
            if self.isLeaf():
                nodeFile.write("1")
            else:
                nodeFile.write("0")
                    

#Create a tree node with given values
def createTreeNode(keys,children,parent,next,prev,leaf):
    global currentAccessCounter
    currentAccessCounter += 1

    if len(keys) != len(children):
        error("Wrong keys/children set provided for the data node by %d"%parent)
    global fileCounter
    fileCounter += 1
    nodeNo = fileCounter
    nodeName = str(nodeNo) + ".dat"

    with open("data/"+nodeName,'w+') as nodeFile:
        nodeFile.write("node %d\n"%nodeNo)
        nodeFile.write("keys")
        for key in keys:
            nodeFile.write(" "+str(key))
        nodeFile.write("\nchildren")
        for child in children:
            nodeFile.write(" "+str(child))
        nodeFile.write("\nparent %d"%parent)
        nodeFile.write("\nnext %d"%next)
        nodeFile.write("\nprev %d"%prev)
        if leaf:
            nodeFile.write("\nleaf 1")
        else:
            nodeFile.write("\nleaf 0")
    return nodeNo


#Create a data node with a root node of the tree as the parent
def createDataNode(keys,data,parent):
    global currentAccessCounter
    currentAccessCounter += 1

    if len(keys) != len(data):
        error("Wrong keys/data set provided for the data node by %d"%parent)
    global fileCounter
    fileCounter += 1
    dataNodeNo = fileCounter
    with open("data/%d.dat"%dataNodeNo,'w+') as dataFile:
        dataFile.write("data %d\n"%dataNodeNo)
        for i in range(0,len(keys)):
            dataFile.write(str(keys[i]) + " " + str(data[i])+"\n")
        dataFile.write("parent " + str(parent)+"\n")
    return dataNodeNo
    

#Create a new B-plus tree with the first pair of key and data
def createTree(key,data):
    global currentAccessCounter
    currentAccessCounter += 1

    global fileCounter
    fileCounter += 1
    nodeNo = fileCounter
    fileCounter += 1
    dataNodeNo = fileCounter

    with open("data/%d.dat"%nodeNo,'w+') as nodeFile:
        nodeFile.write("node\n")
        nodeFile.write("keys")
        nodeFile.write(" "+str(key))
        nodeFile.write("\nchildren")
        nodeFile.write(" "+str(dataNodeNo))
        nodeFile.write("\nparent 0")
        nodeFile.write("\nnext 0")
        nodeFile.write("\nprev 0")
        nodeFile.write("\nleaf 1")

    with open("data/%d.dat"%dataNodeNo,'w+') as dataFile:
        dataFile.write("data\n")
        dataFile.write(str(key) + " " + str(data)+"\n")
        dataFile.write("parent " + str(nodeNo)+"\n")
    
    return nodeNo
    

#Set prev parameter of the given node
def updatePrev(nodeNo,prev):
    node = Node(nodeNo)
    node.prev = prev
    node.writeToDisk()
    return


#Update the parent of a node, generally after the old parent split
def updateParent(nodeNo,parent):
    if not os.path.isfile("./data/%d.dat"%nodeNo):
        error("ERROR, node %d data not found"%nodeNo)
        
    lines = open("data/%d.dat"%nodeNo).readlines()

    for line in lines:
        if line.split()[0]=='parent':
            lines[lines.index(line)]="parent %d\n"%parent

    open("data/%d.dat"%nodeNo,'w').writelines(lines)


#Update the key for the nodes in the tree recursively, till root
def updateRec(parent,node):
    if parent == 0:
        return
    par = Node(parent)
    nod = Node(parent)
    i = par.children.index(node)
        
    par.updateKey(i,nod.maxKey())
    par.writeToDisk()

    if i == (par.numKeys()-1):
        updateRec(par.parent,parent,key)


#Split the node with more keys than the allowed blockSize, and do so recursively till root is reached
def splitRec(node):
    global blockSize
    nod1 = Node(node)
    #split the key and children lists
    keys1 = nod1.keys[0:blockSize/2]
    keys2 = nod1.keys[blockSize/2+1:(nod1.numKeys())]
    children1 = nod1.children[0:blockSize/2]
    children2 = nod1.children[blockSize/2+1:(nod1.numKeys())]

    #create a new tree node and set the referees accordingly
    newNode = createTreeNode(keys2,children2,nod1.parent,nod1.next,nod1.nodeNo,nod1.isLeaf())
        
 
    for child in children2:
        updateParent(child,newNode)

    nod1.keys = keys1
    nod1.children = children1

    if nod1.next!=0:
        updatePrev(nod1.next,newNode)
    nod1.next = newNode
    nod1.writeToDisk()

    nod2 = Node(newNode)
    key1 = nod1.maxKey()
    key2 = nod2.maxKey()

    if nod1.isRoot():
        #This node is the root. Create a new root
        global tree
        tree = createTreeNode([key1,key2],[node,newNode],0,0,0,False)
        updateParent(node,tree)
        updateParent(newNode,tree)
        return

    else:
        par = Node(nod1.parent)
        i = par.children.index(node)
        par.updateKey(i,key1)
        par.keys.insert(i+1,key2)
        par.children.insert(i+1,newNode)

        if par.numKeys() <= blockSize:
            par.writeToDisk()
            #Update the key in the path from root to this leaf
            if i==(par.numKeys()-1):
                updateRec(par.parent,par.nodeNo)
            return
        #Split this node recursively too
        else:
            splitRec(nod1.parent)


#Find the leaf node at which insertion will take place
#IMPORTANT: The rule to use is that the child indexed by i, contains elements which have keys which are less than or equal to the key at i
def findLeaf(key):
    global tree
    curr = tree
    currNode = Node(curr)
    while not currNode.isLeaf():
        i = 0
        for i in range(0,currNode.numKeys()):
            if currNode.keys[i]>key:
                break
        
        curr = currNode.children[i]
        currNode = Node(curr)
    return curr


#Function to wrap around insertion operation
def insert(key,data):
    currNode = Node(findLeaf(key))
    currNode.addDataToLeaf(key,data)
    return


#Function for point query operation. 
def pointQuery(key):
    data = []
    #Get the first data node with its key greater than 'key'
    currNode = Node(findLeaf(key))
    i = 0
    for i in range(0,currNode.numKeys()):
        currKey = currNode.keys[i]
        if currKey > key:
            break
    
    currKey = currNode.keys[i]

    while not currKey < key:
        if currKey == key:
            #Get data from the data node and append it to the return list
            data.extend(getData(currNode.children[i]))

        if i != 0:
            i -= 1
            currKey = currNode.keys[i]
        else:
            if currNode.prev == 0:
                break
            else:
                currNode = Node(currNode.prev)
                i = currNode.numKeys()-1
                currKey = currNode.keys[i]

    return data


#Function for range query, similar to the point query function
def rangeQuery(center,limit):
    data = {}
    
    #Get the first data node with its key greater than 'key'
    currNode = Node(findLeaf(center+limit))
    i = 0
    for i in range(0,currNode.numKeys()):
        currKey = currNode.keys[i]
        if currKey > center+limit:
            break
    
    currKey = currNode.keys[i]

    while not currKey < center-limit:
        if currKey <= center+limit and currKey >= center-limit:
            #Get data from the data node and append it to the return list
            if currNode.keys[i] in data:
                data[currNode.keys[i]].extend(getData(currNode.children[i]))
            else:
                data[currNode.keys[i]] = []
                data[currNode.keys[i]].extend(getData(currNode.children[i]))

        if i != 0:
            i -= 1
            currKey = currNode.keys[i]
        else:
            if currNode.prev == 0:
                break
            else:
                currNode = Node(currNode.prev)
                i = currNode.numKeys()-1
                currKey = currNode.keys[i]

    return data
    

#Function to take a data node and return the data contained in it as a list
def getData(dataNodeNo):
    global currentAccessCounter
    currentAccessCounter += 1

    if not os.path.isfile("./data/%d.dat"%dataNodeNo):
        error("ERROR, node %d data not found"%dataNodeNo)
        
    lines = open("data/%d.dat"%dataNodeNo).readlines()
    
    if lines[0].split()[0]!='data':
        error("ERROR, node %d not a data node"%dataNodeNo)

    data = []
    for line in lines[1:]:
        if line.split()[0]!='parent':
            data.append(line.split()[1])
    
    return data

#Print the error message and exit
def error(errorString):
    print errorString
    exit()


if __name__ == "__main__":
    global fileCounter
    global currentAccessCounter

    fileCounter = 0
    currentAccessCounter = 0

    if not os.path.exists("./data"):
        os.makedirs("./data")

    with open("bplustree.config") as config:
        global blockSize
        blockSize = int(config.readline())        

    with open("assgn2_bplus_data.txt") as datafile:
#    with open("sampledata.txt") as datafile:
        lines = datafile.readlines()
        currline = lines[0]
        currkey = currline.split()[0]
        currdata = currline.split()[1]
        global tree
        tree = createTree(currkey,currdata)

        for currline in lines[1:]:
            currkey = float(currline.split()[0])
            currdata = currline.split()[1]
            insert(currkey,currdata)

    insertTimeStats = StatsAggregator()
    insertAccessStats = StatsAggregator()
    pointQueryTimeStats = StatsAggregator()
    pointQueryAccessStats = StatsAggregator()
    rangeQueryTimeStats = StatsAggregator()
    rangeQueryAccessStats = StatsAggregator()

    with open("querysample.txt") as queryfile:
        lines = queryfile.readlines()
        for line in lines:
            if line.split()[0] == '0':
                currentAccessCounter = 0
                before = datetime.datetime.now()
                insert(float(line.split()[1]),line.split()[2])
                after = datetime.datetime.now()
                insertTimeStats.update((after - before).microseconds)
                insertAccessStats.update(currentAccessCounter)
                
            elif line.split()[0] == '1':
                currentAccessCounter = 0
                before = datetime.datetime.now()
                pointQuery(float(line.split()[1]))
                after = datetime.datetime.now()
                pointQueryTimeStats.update((after - before).microseconds)
                pointQueryAccessStats.update(currentAccessCounter)

            elif line.split()[0] == '2':
                currentAccessCounter = 0
                before = datetime.datetime.now()
                rangeQuery(float(line.split()[1]),float(line.split()[2]))
                after = datetime.datetime.now()
                rangeQueryTimeStats.update((after - before).microseconds)
                rangeQueryAccessStats.update(currentAccessCounter)


    print "\n***************************"
    print "Stats for insert operation"
    print "TIME:"
    insertTimeStats.printStats()
    print "DISK ACCESS:"
    insertAccessStats.printStats()

    print "\n***************************"
    print "Stats for point query operation"
    print "TIME:"
    pointQueryTimeStats.printStats()
    print "DISK ACCESS:"
    pointQueryAccessStats.printStats()

    print "\n***************************"
    print "Stats for range query operation"
    print "TIME:"
    rangeQueryTimeStats.printStats()
    print "DISK ACCESS:"
    rangeQueryAccessStats.printStats()
