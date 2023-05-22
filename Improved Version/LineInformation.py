import collections
import pandas as pd
class StationInfo:
    def __init__(self, data):
        self.data = data
        self.stations = collections.defaultdict(list)
        self.lines = collections.defaultdict(list)

        for index, row in self.data.iterrows():
            self.stations[row[1]].append(row[0])
            self.lines[row[0]].append(row[1])
    
    # Input station name to return station line info
    def getStation(self, station):
        return self.stations[station]

    # Input Line name to return stations on the line network
    def getLine(self, line):
        return self.lines[line]

    # Return all stations with their respective lines
    def getAllStations(self):
        return self.stations
    
    # Return all Lines with their respective stations
    def getAllLines(self):
        return self.lines
