import image, game

class Player:
    moveRight = False
    moveLeft = False
    moveUp = False
    moveDown = False
    def __init__(self, x, y, speed, health, sprite):
        #Initialising object variables
        #x, y used for player postiion, velx, vely will be used for player velocity
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.sprite = image.getImage(sprite)
        
    def render(self, screen):
        screen.blit(self.sprite, (self.x,self.y))
        
    def tick(self):
        if(self.moveRight):
            self.x += self.speed
        if(self.moveDown):
            self.y += self.speed
        if(self.moveLeft):
            self.x -= self.speed
        if(self.moveUp):
            self.y -= self.speed
        if (self.x < 0):
            self.x = 0
        if (self.y < 0):
            self.y = 0
        if (self.y > (game.height - self.sprite.get_height())):
            self.y = game.height - self.sprite.get_height()
        if (self.x > (game.width - self.sprite.get_width())):
            self.x = game.width - self.sprite.get_width()
    
    def checkCollision(self, map, mapTiles):
        #TODO write some long ugly code checking the x / y coordinate for every side of the 
        #sprite to check for collision and change movemen based on that because I am out of ideas 
        #As the x and y coordinates default to the top left of the sprite which is impractical 
        #and inside of the object that I want to prevent it getting inside of and I don't want to make
        #this easy and limit to only tile based movement 
        colliding = False
        playerGridX = int(self.x / 64)
        playerGridY = int(self.y / 64)
        if map[playerGridX][playerGridY] == (100,100,100):
            colliding = True
        print(playerGridX, playerGridY)
        if colliding:
            print('colliding')