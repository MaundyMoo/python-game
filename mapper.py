#This class will handle opening and scanning an img to get the values of each pixel to assign a tile to
from PIL import Image
class readMapTiles:
    def __init__(self, path):
        #Opens the image
        self.map = Image.open(path)
        #Gets a list of all the pixel data in the img in a 1 dimensional list
        pixels = list(self.map.getdata())
        #Sets the size so that the pixel list can be turned into a 2 dimensional array like a grid
        width, height = self.map.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        self.pixels = pixels
    
    def returnMap(self):
        print(self.pixels)
        return self.pixels