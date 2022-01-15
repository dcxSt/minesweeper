class Cat:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.health = 10
        self.hunger = 5
        self.color = "blue"
    
    def __str__(self):
        return self.name + " is " + str(self.age) + " years old"

    def feed(self):
        self.hunger -= 1


"""

class Grid:
    # attributes
    list_of_blocks 
    current_shape

    # methods


class Shape:
    # attributes
    color 
    position

    # methods
    rotate_shape
    move_shape (left right)


class Block: # aka tile

"""
