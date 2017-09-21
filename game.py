#The base scene that handles the framework logic
class SceneBase:
    def __init__(self):
        self.next = self  
    def ProcessInput(self, events, pressed_keys):
        print("ProcessInput not overwritten")
    def Update(self):
        print("Update not overwritten")
    def initialRender(self, screen):
        print("initialRender not overwritten")
    def Render(self, screen):
        print("Render not overwritten")
    
    def SwitchToScene(self, next_scene):
        self.next = next_scene    
    def Terminate(self):
        self.SwitchToScene(None)

def run_game(width, height, fps, starting_scene):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("MoundyMoo")
    pygame.display.set_icon(image.getImage('C:/Dev/git/python-game.git/res/Moo.ico'))
    clock = pygame.time.Clock()
    active_scene = starting_scene
    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()       
        #Event filtering - Detects if user wants to close the game, otherwise sends inputs to be handled by scene
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            #Checks if window is being closed or if alt-f4 is pressed (pygame doesn't close on alt-f4 by default)
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True           
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        #Call the methods in the active scene
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        
        #Check if scene needs to be changed
        active_scene = active_scene.next
        #Update the buffer and tick to the next frame
        pygame.display.flip()
        clock.tick(fps)
        #print ("fps:", clock.get_fps())
        
class TitleScene(SceneBase):
    font = None
    title = None
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 64)
        self.title = self.font.render("MoundyMoo", True, (0, 128, 128))
        SceneBase.__init__(self)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                #Move to the next scene when the user pressed Enter
                self.SwitchToScene(GameScene())
    
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((255, 0, 0))
        screen.blit(self.title, ((width / 2) - (self.title.get_width())/2, height / 2 - (self.title.get_height())))


class GameScene(SceneBase):
    backgroundRendered = False
    #List of used tiles
    tileSize = [0, 0]
    def __init__(self):
        SceneBase.__init__(self)
        self.char = player.Player(0, 0, 5, 5, 'C:/Dev/git/python-game.git/res/Character.png')
        #TODO change map from a string of the path to the actual image
        self.map = mapper.readMapTiles('C:/Dev/git/python-game.git/res/map.png')
        self.map = self.map.returnMap()
        #Tiles
        #TODO replace with tiles based on colours (dictionary perhaps?)
        grassTile = tile.Tile('C:/Dev/git/python-game.git/res/grass.png', False)
        flowerTile = tile.Tile('C:/Dev/git/python-game.git/res/grassFlower.png', False)
        rockTile = tile.Tile('C:/Dev/git/python-game.git/res/rockWall.png', True)
        #Dictionary to correspond each tile type to an rgb value on the map
        self.maptiles = {
            (0,255,0) : grassTile,
            (255,255,0) : flowerTile,
            (100,100,100) : rockTile
        }
        self.tileSize[0] = grassTile.sprite.get_width()
        self.tileSize[1] = grassTile.sprite.get_height()  
        
    def ProcessInput(self, events, pressed_keys):
        #Player movement
        for event in events:
            #TODO rework code to allow configuration
            #Begin movement
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    self.char.moveUp = True
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    self.char.moveDown = True
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    self.char.moveLeft = True
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    self.char.moveRight = True
            #Stop movement
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    self.char.moveUp = False
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    self.char.moveDown = False
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    self.char.moveLeft = False
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    self.char.moveRight = False
            
    def Update(self):
        self.char.checkCollision(self.map, self.maptiles, self.tileSize)
        self.char.tick()

    
    def initialRender(self, screen):
        #Render all the tiles at the beginning
        for row in range(0, len(self.map)):
            for column in range (0, len(self.map[0])):
                screen.blit(self.maptiles[self.map[row][column]].sprite, (column * self.tileSize[0], row * self.tileSize[1]))
        self.backgroundRendered = True
        
    def Render(self, screen):
        #render the background on the first frame
        if not self.backgroundRendered:
            self.initialRender(screen)

        #Render tiles around player 
        #Could possibly rework logic into player class if need to reuse multiple times, not sure on feasbility though
        for row in range(0, len(self.map)):
            for column in range (0, len(self.map[0])):
                if int(self.char.x / self.tileSize[0]) == column and int(self.char.y / self.tileSize[1]) == row:
                    offsetX = -1
                    offsetY = -1
                    for offsetX in range(-1,2):
                        for offsetY in range(-1,2):
                            screen.blit(self.maptiles[self.map[row + offsetX][column + offsetY]].sprite, ((column + offsetY) * self.tileSize[0], (row + offsetX) * self.tileSize[1]))
                
        #Render character
        self.char.render(screen)

width = 580
height = 500        
if __name__ == "__main__":     
    #This is the main file that handles the game and scene logic
    import pygame
    #Import child modules
    import player, tile, mapper, image
    #Screen size
    pygame.init()

    run_game(width, height, 60, TitleScene())