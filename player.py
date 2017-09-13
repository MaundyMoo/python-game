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