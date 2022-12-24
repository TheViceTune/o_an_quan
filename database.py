import codecs
from random import shuffle, randint
import sys, json, datetime

# Load the data from file
def loadData(locationString):
    with codecs.open(locationString, encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

# Writes data to file
def writeData(locationString, data):
    with codecs.open(locationString, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)

