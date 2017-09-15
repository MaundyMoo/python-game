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
    pygame.display.set_caption("Moundy's Moo")
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
        print ("fps:", clock.get_fps())
        
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
    tiles = []
    tileSize = [0, 0]
    def __init__(self):
        SceneBase.__init__(self)
        self.char = player.Player(0, 0, 5, 5, 'C:/Dev/git/python-game.git/res/Character.png')
        #TODO change map from a string of the path to the actual image
        self.map = ('C:/Dev/git/python-game.git/res/map.png')
        #Tiles
        
        grassTile = tile.Tile('C:/Dev/git/python-game.git/res/grass.png', False)
        flowerTile = tile.Tile('C:/Dev/git/python-game.git/res/grassFlower.png', False)
        
        self.tiles.append(grassTile)
        self.tiles.append(flowerTile)
        
        self.tileSize[0] = grassTile.sprite.get_width()
        self.tileSize[1] = grassTile.sprite.get_height()

        self.tileGrid = self.getGrid()
    
    #TODO replace with map reading
    def getGrid(self):               
        x = 0
        y = 0
        tileGrid = []
        for x in range(0, int(width / self.tileSize[0]) + 1):
            for y in range(0, int(height / self.tileSize[1]) + 1):
                type = random.randint(0,1)
                tileGrid.append((x,y, type))
            y += 1
        x += 1
        return tileGrid
        
    def ProcessInput(self, events, pressed_keys):
        #Player movement
        for event in events:
            #TODO rework code to allow configuration
            #Begin movement
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP):
                    self.char.moveUp = True
                if (event.key == pygame.K_DOWN):
                    self.char.moveDown = True
                if (event.key == pygame.K_LEFT):
                    self.char.moveLeft = True
                if (event.key == pygame.K_RIGHT):
                    self.char.moveRight = True
            #Stop movement
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP):
                    self.char.moveUp = False
                if (event.key == pygame.K_DOWN):
                    self.char.moveDown = False
                if (event.key == pygame.K_LEFT):
                    self.char.moveLeft = False
                if (event.key == pygame.K_RIGHT):
                    self.char.moveRight = False
            
    def Update(self):
        self.char.tick()
    
    def initialRender(self, screen):
        #Render all the tiles at the beginning
        for each in self.tileGrid:
            self.tiles[each[2]].render(screen, each, 0, 0)
        self.backgroundRendered = True
    def Render(self, screen):
        #Render tiles around player 
        if not self.backgroundRendered:
            self.initialRender(screen)
        #Could possibly rework logic into player class if need to reuse multiple times, not sure on feasbility though
        for each in self.tileGrid:
            if int(self.char.x / self.tileSize[0]) == each[0] and int(self.char.y / self.tileSize[1]) == each[1]:
                offsetX = -1
                offsetY = -1
                for offsetX in range(-1,2):
                    for offsetY in range(-1,2):                       
                        #TODO get the tile type from the grid here for each offset
                        self.tiles[each[2]].render(screen, each, offsetX, offsetY)
        #Render character
        self.char.render(screen)

width = 540
height = 400        
if __name__ == "__main__":     
    #This is the main file that handles the game and scene logic
    import pygame, random
    #Import child modules
    import player, tile
    #Screen size
    pygame.init()

    run_game(width, height, 60, TitleScene())