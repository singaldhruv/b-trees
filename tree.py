#Code for the second assignment of CS315
#Dhruv Singal 12243
import os

fileCounter = 0

class Node:

    #Create a node object by reading from the file
    def __init__(self,nodeNo):
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
        print "nodeNo: ",self.nodeNo
        print "keys: ",self.keys
        print "children: ", self.children
        print "parent: ",self.parent
        print "next: ",self.next
        print "prev: ",self.prev
        print "isLeaf: ",self.isLeaf()
        print "isRoot: ",self.isRoot()
        print "\n",

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
            #split the key and children lists
            keys1 = self.keys[0:blockSize/2]
            keys2 = self.keys[blockSize/2+1:(self.numKeys())]
            children1 = self.children[0:blockSize/2]
            children2 = self.children[blockSize/2+1:(self.numKeys())]
            #create a new tree node and set the referees accordingly
            newNode = createTreeNode(keys2,children2,self.parent,self.next,self.nodeNo,self.isLeaf())
            for child in children2:
                updateDataNodeParent(child,newNode)

            self.keys = keys1
            self.children = children1
            if self.next!=0:
                updatePrev(self.next,newNode)
            self.next = newNode
            self.writeToDisk()
            #update the parent recursively
            splitRec(self.parent,self.nodeNo,newNode)

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
    if len(keys) != len(data):
        error("Wrong keys/data set provided for the data node by %d"%parent)
    global fileCounter
    fileCounter += 1
    dataNodeNo = fileCounter
    with open("data/%d.dat"%dataNodeNo,'w+') as dataFile:
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

#Set parent parameter of the given node
def updateParent(nodeNo,parent):
    node = Node(nodeNo)
    node.parent = parent
    node.writeToDisk()
    return

def updateDataNodeParent(nodeNo,parent):
    if not os.path.isfile("./data/%d.dat"%nodeNo):
        error("ERROR, node %d data not found"%nodeNo)
        
    lines = open("data/%d.dat"%nodeNo).readlines()
    if lines[0].split()[0] != 'data':
        error("ERROR, file %d.dat is not a data node"%nodeNo) 

    for line in lines:
        if line.split()[0]=='parent':
            lines[lines.index(line)]="parent %d"%parent

    open("data/%d.dat"%nodeNo,'w').writelines(lines)


#Update the key for the nodes recursively
def updateRec(parent,node):
    if parent == 0:
        return
    par = Node(parent)
    nod = Node(parent)
    i = par.children.index(node)
    for i in range(0,par.numKeys()):
        if par.children[i]==node:
            break
        
    par.updateKey(i,nod.maxKey())
    par.writeToDisk()

    if i == (par.numKeys()-1):
        updateRec(par.parent,parent,key)



#Split the node recursively to the top
def splitRec(parent,node1,node2):

    if parent==0:
        #Base case, completed processing the top
        #Create a new root adding the node addresses of the two new nodes and update the parent pointers of node1 and node2s
        nodeObject1 = Node(node1)
        nodeObject2 = Node(node2)
        key1 = nodeObject1.maxKey()
        key2 = nodeObject2.maxKey()

        global tree
        tree = createTreeNode([key1,key2],[node1,node2],0,0,0,False)
        updateParent(node1,tree)
        updateParent(node2,tree)

    else:
        #On a tree node (maybe root)
        #Check if the node has enough space, if yes, just add the new node
        #If not, split the node and call this function recursively
        par = Node(parent)
        nodeObject1 = Node(node1)
        nodeObject2 = Node(node2)
        key1 = nodeObject1.maxKey()
        key2 = nodeObject2.maxKey()
        
        global blockSize
        i = 0
        i = par.children.index(node1)
        for i in range(0,par.numKeys()):
            if par.children[i]==node1:
                break

        par.keys.insert(i+1,key2)
        par.children.insert(i+1,node2)

        if par.numKeys() <= blockSize:
            par.writeToDisk()
            #Update the key in the path from root to this leaf
            #updateRec(par.parent,par.nodeNo,par.maxKey())

        else:
            #Split the parent too, and call this routine recursively
            keys1 = par.keys[0:blockSize/2]
            keys2 = par.keys[blockSize/2+1:(par.numKeys())]
            children1 = par.children[0:blockSize/2]
            children2 = par.children[blockSize/2+1:(par.numKeys())]
            #create a new tree node and set the referees accordingly
            newNode = createTreeNode(keys2,children2,par.parent,par.next,par.nodeNo,par.isLeaf())
            par.keys = keys1
            par.children = children1
            if par.next!=0:
                updatePrev(par.next,newNode)
            par.next = newNode
            par.writeToDisk()
            #update the parent recursively
            splitRec(par.parent,par.nodeNo,newNode)

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
        global tree
        tree = createTree(currkey,currdata)

        for currline in lines[1:]:
            currkey = currline.split()[0]
            currdata = currline.split()[1]
            currNode = Node(findLeaf(currkey))
            currNode.addDataToLeaf(float(currkey),currdata)
    
        Node(tree).printValues()
        Node(36).printValues()
