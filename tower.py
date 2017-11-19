class tower:
    range = 10
    power = 1
    health = 1
    
    def __init__(self, xloc, yloc):
        self.xloc = xloc
        self.yloc = yloc
    
    def shoot(self, targets):
        import math
        targ_return = []
        for choice in targets:
            if math.sqrt((choice.xloc - self.xloc)**2  + (choice.yloc - self.yloc)**2) <= self.range:
                choice.health = choice.health - self.power
                if choice.health > 0:
                    targ_return.append(choice)
        targ_return            
    

