class Node :
    
    def __init__(self,value, id_node,children = [] ):
        self.value = value
        self.children = children
        self.id = id_node
        
    def setChildren(self,ch):
        self.children.append(ch)
        
    def getValue (self):
        return self.value
    
    def getID (self):
        return self.id
    
    def children (self):
        return self.children 

    def is_leaf(self):
        return self.children==[]
    
class Arc:
    def __init__(self,weight,father,son = None):
        self.weight = weight
        self.father = father
        self.son = son
        self.data = None
        
    def setSon(self,son):
        self.son = son
    
    def setData(self,data):
        self.data=data
        
    def getWeight(self):
        return self.weight
    
    def getFather (self):
        return self.father

    def getSon (self):
        return self.son
    
    def getData(self):
        return self.data
    
class Arbre_Desicion:
    def __init__(self,root):
        self.root = root
    