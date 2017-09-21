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
    
    def checkCollision(self, map, mapTiles, tileSize):
        colliding = False
        playerGridX = int(self.x / tileSize[0])
        playerGridY = int(self.y / tileSize[1])
        collisionCheckOffset = 5
        #Check collisions on topLeft and bottomLeft for collisions on the left
        if mapTiles[map[playerGridY][int((self.x - collisionCheckOffset)/ tileSize[0])]].collision:
            self.moveLeft = False
        elif mapTiles[map[int((self.y + self.sprite.get_height()) / tileSize[1])][int((self.x - collisionCheckOffset)/ tileSize[0])]].collision:
            self.moveLeft = False
        #Check collisions on topRight and bottomRight for collisions on the right
        if mapTiles[map[playerGridY][int((self.x + self.sprite.get_width() + collisionCheckOffset)/ tileSize[0])]].collision:
            self.moveRight = False
        elif mapTiles[map[int((self.y + self.sprite.get_height()) / tileSize[1])][int((self.x + self.sprite.get_width() + collisionCheckOffset)/ tileSize[0])]].collision:
            self.moveRight = False
        #Check collisions for above
        if mapTiles[map[int((self.y - collisionCheckOffset)/ tileSize[1])][playerGridX]].collision:
            self.moveUp = False
        elif mapTiles[map[int((self.y - collisionCheckOffset)/ tileSize[1])][int((self.x + self.sprite.get_width())/ tileSize[0])]].collision:
            self.moveUp = False
        #Check collisions for below
        if mapTiles[map[int((self.y + self.sprite.get_height() + collisionCheckOffset)/ tileSize[1])][playerGridX]].collision:
            self.moveDown = False
        elif mapTiles[map[int((self.y + self.sprite.get_height() + collisionCheckOffset)/ tileSize[1])][int((self.x + self.sprite.get_width())/ tileSize[0])]].collision:
            self.moveDown = False