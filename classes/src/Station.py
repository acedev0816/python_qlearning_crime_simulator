from Common import *
class Station:
    """Station class is ..."""
    
    def __init__(self, lat, lon, effective, name):
        self.lat = lat
        self.lon = lon
        self.effective = effective
        self.name = name

    def getPosition(self):
        return self.lat, self.lon

    def getEffective(self):
        return self.effective
    
    def getName(self):
        return self.name

    def printPosition(self):
        print("Lat: ", self.lat)
        print("Lon: ", self.lon)

    def printEffective(self):
        print("effective: ", self.effective )

    def printName(self):
        print("Name: ", self.name)

if __name__ == '__main__':
    lat, lon = generateRandomPosition()
    station = Station(lat, lon,500,"aaa")
    station.printPosition()
    station.printEffective()
    station.printName()