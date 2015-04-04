#Code for the second assignment of CS315
#Dhruv Singal 12243
import os

fileCounter = 0

class Node:
    nodeNo = 0
    keys = []
    children = []
    parent = 0
    next = 0
    prev = 0
    leaf = False

    #Create a node object by reading from the file
    def __init__(self,nodeNo):
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
        print self.keys, self.children, self.parent, self.next, self.prev, self.leaf

    #Returns the number of keys in the tree node
    def numKeys(self):
        return len(self.keys)

    def isLeaf(self):
        return self.leaf

    def isRoot(self):
        return self.parent == 0

    #Add a key/data pair to a leaf of the tree
    def addDataToLeaf(self,key,data):
        if not self.isLeaf():
            error("Can't add data to a non-leaf node %d"%self.nodeNo)
        
        global blockSize
        newDataNode = createDataNode([key],[data],self.nodeNo)
        for i in range(0,self.numKeys()):
            if self.keys[i]>key:
                break
        self.keys.insert(i,key)
        self.children.insert(i,newDataNode)

        if self.numKeys() < blockSize:
            self.writeToDisk()

        else:
            #split the node and add key to parent and so on
            a = 1
    #
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
                    

def createTreeNode(keys,children,parent):
    if len(keys) != len(children):
        error("Wrong keys/children set provided for the data node by %d"%parent)
    global fileCounter
    fileCounter += 1
    nodeNo = fileCounter
    nodeName = str(nodeNo) + ".dat"

    with open("data/"+nodeName,'w+') as nodeFile:
        nodeFile.write("node\n")
        nodeFile.write("keys")
        for key in keys:
            nodeFile.write(" "+str(key))
        nodeFile.write("\nchildren")
        for child in children:
            nodeFile.write(" "+str(child))
        nodeFile.write("\nparent "+str(parent)+"\n")
    return nodeNo


#Create a data node with a root node of the tree as the parent
def createDataNode(keys,data,parent):
    if len(keys) != len(data):
        error("Wrong keys/data set provided for the data node by %d"%parent)
    global fileCounter
    fileCounter += 1
    dataNodeNo = fileCounter
    dataNodeName = str(dataNodeNo) + ".dat"
    with open("data/"+dataNodeName,'w+') as dataFile:
        dataFile.write("data\n")
        for i in range(0,len(keys)):
            dataFile.write(str(keys[i]) + " " + str(data[i])+"\n")
        dataFile.write("parent " + str(parent)+"\n")
    return dataNodeNo
    



#Create a new B-plus tree with the first pair of key and data
def createTree(key,data):
    global fileCounter
    fileCounter += 1
    nodeNo = fileCounter
    nodeName = str(nodeNo) + ".dat"
    fileCounter += 1
    dataNodeNo = fileCounter
    dataNodeName = str(dataNodeNo) + ".dat"

    with open("data/"+nodeName,'w+') as nodeFile:
        nodeFile.write("node\n")
        nodeFile.write("keys")
        nodeFile.write(" "+str(key))
        nodeFile.write("\nchildren")
        nodeFile.write(" "+str(dataNodeNo))
        nodeFile.write("\nparent 0")
        nodeFile.write("\nnext 0")
        nodeFile.write("\nprev 0")
        nodeFile.write("\nleaf 1")

    with open("data/"+dataNodeName,'w+') as dataFile:
        dataFile.write("data\n")
        dataFile.write(str(key) + " " + str(data)+"\n")
        dataFile.write("parent " + str(nodeNo)+"\n")
    
    return nodeNo
    





#Print the error message and exit
def error(errorString):
    print errorString
    exit()






if __name__ == "__main__":
    if not os.path.exists("./data"):
        os.makedirs("./data")

    with open("bplustree.config") as config:
        global blockSize
        blockSize = int(config.readline())        

    with open("sampledata.txt") as datafile:
        lines = datafile.readlines()
        currline = lines[0]
        currkey = currline.split()[0]
        currdata = currline.split()[1]
        tree = createTree(currkey,currdata)
        node = Node(tree)
        for currline in lines[1:]:
            currkey = currline.split()[0]
            currdata = currline.split()[1]
            node.addDataToLeaf(float(currkey),currdata)
    
        node.printValues()
