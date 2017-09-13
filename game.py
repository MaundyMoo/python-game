##This is the main file that handles the game and scene logic
import pygame, random
##Import child modules
import player, tile
##Screen size
width = 540
height = 400
#Initialise pygame
pygame.init()
##The base scene that handles the framework logic
class SceneBase:
    def __init__(self):
        self.next = self  
    def ProcessInput(self, events, pressed_keys):
        print("ProcessInput not overwritten")
    def Update(self):
        print("Update not overwritten")
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
        # Event filtering - Handles closing the game
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
        pygame.display.update()
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
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(GameScene())
    
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((255, 0, 0))
        screen.blit(self.title, ((width / 2) - (self.title.get_width())/2, height / 2 - (self.title.get_height())))


class GameScene(SceneBase):
    char = None
    ##List of used tiles
    tiles = []
    grid = None
    tileSize = 64
    def __init__(self):
        SceneBase.__init__(self)
        self.char = player.Player(0, 0, 5, 5, 'res/Character.png')
        ##Tiles
        grassTile = tile.Tile('res/grass.png', False)
        self.tiles.append(grassTile)
        flowerTile = tile.Tile('res/grassFlower.png', False)        
        self.tiles.append(flowerTile)
        self.grid = self.getGrid()
    
    def getGrid(self):               
        x = 0
        y = 0
        grid = []
        ##TODO find a more optimized solution than rerendering every frame
        for x in range(0, int(width / self.tileSize) + 1):
            for y in range(0, int(height / self.tileSize) + 1):
                type = random.randint(0,1)
                grid.append((x,y, type))
            y += 1
        x += 1
        return grid
        
    def ProcessInput(self, events, pressed_keys):
        #Player movement
        for event in events:
            #TODO rework code to allow configuration
            ##Begin movement
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP):
                    self.char.moveUp = True
                if (event.key == pygame.K_DOWN):
                    self.char.moveDown = True
                if (event.key == pygame.K_LEFT):
                    self.char.moveLeft = True
                if (event.key == pygame.K_RIGHT):
                    self.char.moveRight = True
            ##Stop movement
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
    
    def Render(self, screen):
        for each in self.grid:
            self.tiles[each[3]].render(screen, each)
        self.char.render(screen)

if __name__ == "__main__":     
    run_game(width, height, 60, TitleScene())