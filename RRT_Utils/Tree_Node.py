import numpy as np
from RRT_Utils.Cost_Functions import CostToRoot

class Node:
    def __init__(self, Location, Orientation, Cost, Parent, Number):
        self.Location = Location # XY Location
        self.Orientation = Orientation # Orientation Relative to True North
        self.Cost = Cost # Cost to get to Parent
        self.Parent = Parent # Parent Node
        self.Number = Number
        
def NearestNodeSort(val):
    return val[1]  

# Returns an array containing the N nearest points in a Tree to a given Node         
def NearestCostSet(Potential_Node, Tree, N):
    NodePosition = Potential_Node.Location
    TreeDistArray = [] # Create Array for Return
    for x in Tree:
        # Cost to Root
        Cost = CostToRoot(NodePosition,x,Tree)
        TreeDistArray.append([x.Number, Cost])
    TreeDistArray.sort(key=NearestNodeSort)
    TreeSubset = TreeDistArray[0:N]
    return TreeSubset

# Returns an array containing the N points in a Tree with minimum cost to return to root         
def NearestNodeSet(Potential_Node, Tree, N):
    NodePosition = Potential_Node.Location
    
    TreeCostArray = [] # Create Array for Return
    for x in Tree:
        NodeDist = ((NodePosition[0]-x.Location[0])**2 +  (NodePosition[1]-x.Location[1])**2)**(1/2)
        TreeCostArray.append([x.Number, NodeDist])
    TreeCostArray.sort(key=NearestNodeSort)
    TreeSubset = TreeCostArray[0:N]
    return TreeSubset

# Defines a Function that checks whether a location is inside a Store Object
def StoreObjectCollision (Spot, Store):
    for Aisle in Store.Aisles:
        # Location of the Spot
        SpotX = Spot[0]
        SpotY = Spot[1]
        
        # Range of the Aisle Object
        ShapeLocation = Aisle.Placement
        ShapeBounds = [Aisle.Width, Aisle.Length]
        
        if (SpotX >= ShapeLocation[0] and SpotX <= ShapeLocation[0]+ShapeBounds[0]) and \
        (SpotY >= ShapeLocation[1] and SpotY <= ShapeLocation[1]+ShapeBounds[1]):
            Check = 1
            break # Exit Loop, Path is Invalid
        else:
            Check = 0
            
    return Check    
        
def CheckPathToNode (Node, SortedTreeSubset, Tree, Store):
    ViableNodeArray = []
    for Point in SortedTreeSubset:
        Start = Node.Location
        Stop = Tree[Point[0]].Location
        PathArray = np.linspace(Start,Stop,100) # 100 point array making a line between points
        Check = 0 # Set to 0
        for Dot in PathArray: #If i make it through this array without flipping check to 1, then the Point is valid
            if StoreObjectCollision(Dot,Store) == 1: # If this switch activates, then the point along the path hit a store object
                Check = 1
                break
        if Check == 0:
            ViableNodeArray.append(Point[0])
            
    
    # if I made it here, then there were no viable paths
    
    if len(ViableNodeArray) !=0:
        return ViableNodeArray # Return the Indices of Closest Node on FullTree
    else:
        return "Collision"
                

            
    