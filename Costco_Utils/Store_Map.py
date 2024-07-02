# This class corresponds to an aisle object
class Aisle:
    def __init__(self,Number,Length, Width, PlaceX,PlaceY):
        self.Number = Number
        self.Length = Length
        self.Width = Width
        self.Placement = [PlaceX,PlaceY]
        self.Type = "None"
        
            

# This class corresponds to a particular item in the store
class Item:
    def __init__(self,Name,Aisle, RelPlace, PlaceX, PlaceY):
        self.Name = Name # Name of an Item
        self.Aisle  = [Aisle] # What Aisle is the Item On
        self.AislePlacement = [RelPlace] # Above, Below, Left Right?
        self.WorldPlacement = [PlaceX,PlaceY] # Above, Below, Left Right?

# This class is the super class for the entire store
class StoreDefine:
    def __init__(self):
        self.Aisles = []
        self.Items = []