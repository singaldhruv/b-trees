#Code for the second assignment of CS315
#Dhruv Singal 12243
import os

fileCounter = 0

class Node:
    keys = []
    children = []
    parent = 0

    def __init__(self,nodeNo):
        if not os.path.isfile("./data/"+str(nodeNo)+".dat"):
            error("ERROR, node %d data not found"%nodeNo)
        
        with open("data/"+str(nodeNo) + ".dat") as nodeFile:
            lines = nodeFile.readlines()
            if lines[0] != 'node\n':
                error("ERROR, file %d.dat is not a tree node"%nodeNo)
            for line in lines[1:]:
                s = line.split()
                if s[0]=='keys':
                    self.keys = s[1:]
                elif s[0]=='children':
                    self.children=s[1:]
                elif s[0]=='parent':
                    self.parent=s[1]

            print self.keys, self.children, self.parent
        

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

def createDataNode(keys,data,parent):
    if len(keys) != len(data):
        error("Wrong keys/data set provided for the data node by %d"%parent)
    global fileCounter
    fileCounter += 1
    dataNodeNo = fileCounter
    dataNodeName = str(dataNodeNo) + ".dat"
    with open("data/"+dataNodeName,'w+') as dataFile:
        dataFile.write("data\n")
        for i in 1..len(keys):
            dataFile.write(str(keys[i]) + " " + str(data[i])+"\n")
        dataFile.write("parent " + str(nodeNo)+"\n")
    return dataNodeNo
    
def createTree(key,data):
    tree = createTreeNode([key],[data],0)
    createDataNode([

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
        currline = datafile.readline()
        currkey = currline.split()[0]
        currdata = currline.split()[1]
        tree = createTree(currkey,currdata)
    node = Node(tree)
    exit()

    firstLineFlag = True
    with open("sampledata.txt") as datafile:
        for currline in datafile:
            #currline = datafile.readline()
            currkey = currline.split()[0]
            currdata = currline.split()[1]
            if firstLineFlag:
                tree = createTree(currkey)
                firstLineFlag = False
            else:
                addKeyToTree(tree,currkey)
                
    print "Hello World"
