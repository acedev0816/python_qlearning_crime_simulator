from Common import *
class Park:
    """Station class is ..."""
    
    def __init__(self, lat, lon, radius, name):
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.name = name

    def getPosition(self):
        return self.lat, self.lon

    def getRadius(self):
        return self.radius
    
    def getName(self):
        return self.name

    def printPosition(self):
        print("Lat: ", self.lat)
        print("Lon: ", self.lon)

    def printRadius(self):
        print("effective: ", self.radius )

    def printName(self):
        print("Name: ", self.name)