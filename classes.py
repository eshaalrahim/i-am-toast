class Player:
    def __init__(self):
        self.x = 594
        self.y = 450
        self.angle = 0
        self.speed = 30


    def move(self, direction):
        if direction == "right":
            self.angle += 30
        elif direction == "left":
            self.angle -= 30
    
    def jump(self):
        self.y -= self.speed
        
            
class Obstacle: 
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def collide(self, x, y):
        return self.x <= x <= (self.x + self.width//3)

class Edibility:
    def __init__(self):
        self.counter = 100
    
    def decrease(self):
        if self.counter > 0:
            self.counter -= 5


class Skateboard:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == "right":
            self.x -= 30
        elif direction == "left":
            self.x += 30

class Toaster:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def onTop(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height



class Surface:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def isOnSurface(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height