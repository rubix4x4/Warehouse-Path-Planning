# This will serve as the baseline folder for the costco optimization
from RRT_Utils import RRT_Classes as RRT
from RRT_Utils import Tree_Node as Tree
from RRT_Utils import Cost_Functions as Cost
from RRT_Utils.Tree_Node import NearestCostSet, CheckPathToNode
from Costco_Utils import Store_Map as SM
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import random

np.set_printoptions(precision=5)

# region Create Map
Store = SM.StoreDefine()

# region Create Aisles
AisleNums = np.linspace(0, 24, 25)
Aisles = []
for i in range(0,len(AisleNums),1):
    Aisle = SM.Aisle(i,0,0,0,0)
    Aisles.append(Aisle)


AisleLength = len(Aisles)
for i in [0, 1, 2, 3, 4]:
    print(Aisles[i].Number)
    PlaceX = 5 + i*20
    PlaceY = 5 
    Aisles[i].Length = 10*4 #
    Aisles[i].Width = 10
    Aisles[i].Placement = [PlaceX, PlaceY]
    Aisles[i].Type = "Vertical"
    
for i in [5, 6, 7, 8, 9]:
    print(Aisles[i].Number)
    PlaceX = -15 + (i-5)*-20
    PlaceY = 5 
    Aisles[i].Length = 10*4 #
    Aisles[i].Width = 10    
    Aisles[i].Placement = [PlaceX, PlaceY]
    Aisles[i].Type = "Vertical"
    
for i in [10, 11, 12, 13, 14]:
    print(Aisles[i].Number)
    PlaceX = 5 + (i-10)*20
    PlaceY = 55 
    Aisles[i].Length = 10*4 #
    Aisles[i].Width = 10
    Aisles[i].Placement = [PlaceX, PlaceY]
    Aisles[i].Type = "Vertical"
    
for i in [15, 16, 17, 18, 19]:
    print(Aisles[i].Number)
    PlaceX = -15 + (i-15)*-20
    PlaceY = 55
    Aisles[i].Length = 10*4 #
    Aisles[i].Width = 10    
    Aisles[i].Placement = [PlaceX, PlaceY]
    Aisles[i].Type = "Vertical"   
     
for i in [20, 21, 22, 23, 24]:
    print(Aisles[i].Number)
    PlaceX = -45 + (i-20)*20
    PlaceY = 105
    Aisles[i].Length = 10 #
    Aisles[i].Width = 10    
    Aisles[i].Placement = [PlaceX, PlaceY]
    Aisles[i].Type = "Square"
    
Store.Aisles = Aisles #Rewrite Map to include updated Aisles    
# endregion

# region Create Items and Aisle Placements
ItemNum = 200
ItemDict = []
for i in range(0,ItemNum,1):
    ItemAisle = random.randrange(0,len(Store.Aisles))
    if Store.Aisles[ItemAisle].Type == "Vertical":
        RelativeLocation = random.choice(['left','right'])
        Location = Store.Aisles[ItemAisle].Placement
        ItemLoc = [0,0]
        if RelativeLocation == 'left':
            ItemLoc[0] = Location[0]-5
            ItemLoc[1] = Location[1]+ Store.Aisles[ItemAisle].Length*random.random()
        
        elif RelativeLocation == 'right':
            ItemLoc[0] = Location[0]+15
            ItemLoc[1] = Location[1]+ Store.Aisles[ItemAisle].Length*random.random()
        
    elif Store.Aisles[ItemAisle].Type == "Square":
        RelativeLocation = random.choice(['left','right','above','below'])
        Location = Store.Aisles[ItemAisle].Placement
        ItemLoc = [0,0]
        if RelativeLocation == 'left':
            ItemLoc[0] = Location[0]-5
            ItemLoc[1] = Location[1]+5
        
        elif RelativeLocation == 'right':
            ItemLoc[0] = Location[0]+15
            ItemLoc[1] = Location[1]+5
            
        elif RelativeLocation == 'above':
            ItemLoc[0] = Location[0]+5
            ItemLoc[1] = Location[1]+15            
            
        elif RelativeLocation == 'below':    
             ItemLoc[0] = Location[0]+5
             ItemLoc[1] = Location[1]-5       
 
    NewItem = SM.Item(i, ItemAisle, RelativeLocation, ItemLoc[0],ItemLoc[1])
    ItemDict.append(NewItem)

Store.Items = ItemDict
# endregion

# region Create Map
fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(0,len(Store.Aisles),1):
    XY = Store.Aisles[i].Placement
    Length = Store.Aisles[i].Length
    Width = Store.Aisles[i].Width
    ax.add_patch(Rectangle(XY,Width,Length, color = 'green'))
    
for i in range(0,len(Store.Items),1):
    XY = Store.Items[i].WorldPlacement
    ax.add_patch(Circle(XY,1, color = 'blue'))

# Create the Shoppers
Shoppers = []
NewCustomer = RRT.Agent()
ShoppingList = random.sample(sorted(np.linspace(0,len(ItemDict),len(ItemDict)+1)),5) # Assume each shopper is looking for about 5 items
NewCustomer.ShoppingList = ShoppingList
Shoppers.append(NewCustomer)
print(Shoppers[0].Position)
print(Shoppers[0].ShoppingList)

# Create Tree Structure
FullTree = []

StartLocation = [0,0]
NewNode = Tree.Node(StartLocation, 0, 0, "Root", 0)
FullTree.append(NewNode)

# Add Test 100 New Nodes
while(len(FullTree) < 750):
    # Check if Node is In Aisles
    Node_L = [(random.random()-0.5)*240, random.random()*120]
    Node_O = random.random()*360
    
    DummyNode = Tree.Node(Node_L, Node_O, 0, "Dummy", 0)
    # Find Closest N Node in Tree To Target Point
    N = 20
    TreeSubset = NearestCostSet(DummyNode, FullTree, N) 
    
    # Checks Path of all Candidate Nodes for Collisions 
    Check = CheckPathToNode(DummyNode,TreeSubset, FullTree, Store)

    if Check != "Collision":
        # Add Node to Tree
        ClosestTreeNode = Check[0]    
        NodeParent = FullTree[ClosestTreeNode]
        
        NodeCost = Cost.CostToRoot(Node_L, NodeParent, FullTree)
        NewNode = Tree.Node(Node_L, Node_O, NodeCost, ClosestTreeNode, len(FullTree))
        FullTree.append(NewNode)
        
        # Rewire
        TreeSubset = []
        ViableNodes = []
        RewiredNodes = []
        TreeSubset = NearestCostSet(DummyNode, FullTree[0:-1], N) #
        ViableNodes = CheckPathToNode(DummyNode,TreeSubset,FullTree[0:-1],Store)
        for Nodes in ViableNodes:
            CostOriginal = FullTree[Nodes].Cost
            NewCost = Cost.CostToRoot(FullTree[Nodes].Location, FullTree[len(FullTree)-1], FullTree[:-1])
            #print(CostOriginal, ' vs ', NewCost)
            if CostOriginal > NewCost:
                RewiredNodes.append([Nodes, NewCost])

        for Nodes in RewiredNodes:
            FullTree[Nodes[0]].Parent = len(FullTree)-1
            FullTree[Nodes[0]].Cost = Nodes[1]
            
        print(len(FullTree))  
            
for Node in FullTree:
    XY = Node.Location
    ax.add_patch(Circle(XY, .25, color = 'red'))
    Parent = Node.Parent
    if Parent != "Root":
        Start = FullTree[Parent].Location
        PathArray = np.linspace(Start,XY,100)
        ax.plot(PathArray[:,0],PathArray[:,1],'r', linewidth = .5)
plt.xlim([-110,110])            
plt.ylim([0,135])    
plt.show()
print(len(FullTree))  

print("Done")