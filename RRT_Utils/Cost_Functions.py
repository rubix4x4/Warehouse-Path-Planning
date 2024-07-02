def CostToRoot(NodeL,NodeParent,FullTree):
    # Initialize NodeCost with cost to go to immediate parent
    NodeCost = DistCost(NodeL, NodeParent.Location)
    
    # If Node's parent is not root, keep going down the chain
    while NodeParent.Parent != "Root":       
        NodeL = NodeParent.Location
        NodeParent = FullTree[NodeParent.Parent]
        CostToParent = DistCost(NodeL, NodeParent.Location)
        NodeCost = NodeCost + CostToParent
    return NodeCost

def DistCost (NodeL, ParentL):
    return ((NodeL[0]-ParentL[0])**2 +  (NodeL[1]-ParentL[1])**2)**(1/2)