import image
class Tile:
    x = 0
    y = 0
    def __init__(self, sprite, collision):
        self.sprite = image.getImage(sprite)
        self.height = self.sprite.get_height()
        self.width = self.sprite.get_width()
        ##Boolean value
        self.collision = collision
    def render(self, screen,pos):
        
        screen.blit(self.sprite, (pos[0]*self.sprite.get_width(), pos[1]*self.sprite.get_height()))
   