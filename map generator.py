import json
import math
import time
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter



datasource = open("E:\Programming\Projects\maps\Records.json","r")

datadict = json.load(datasource)

locationlist = datadict["locations"]



pairs = [(int(i["latitudeE7"])/1e7,int(i["longitudeE7"])/1e7) for i in locationlist if "latitudeE7" in i.keys()]

# defined by center point and 2 distances
resolution = (1920*4, 1080*4)
p1_lat = 43.465
p1_long = -80.516
lat_height = 2.25
long_width = resolution[0]/resolution[1] * lat_height


lat1 = p1_lat - lat_height/2
lat2 = p1_lat + lat_height/2
long1 = p1_long - long_width/2
long2 = p1_long + long_width/2


stepsizelong = (long2 - long1)/resolution[0]
stepsizelat = (lat2 - lat1)/resolution[1]


coords_to_use = []

for coords in pairs:
    if lat1 <= coords[0] <=lat2:
        if long1 <= coords[1] <= long2:
            coords_to_use.append(coords)

img = Image.new('RGB', (resolution[0], resolution[1]), 'black')



draw = ImageDraw.Draw(img)
for i in range(len(coords_to_use)):
    if i < len(coords_to_use)-1:
        distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use[i][0] - coords_to_use[i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use[i][0])) * math.cos(math.radians(coords_to_use[i+1][0])) * (math.sin(math.radians(coords_to_use[i][1] - coords_to_use[i+1][1])/2)**2)))
    
        if distance < 500:
            draw.line(
            (
            ((coords_to_use[i][1]-p1_long)/stepsizelong)+(resolution[0]/2),
            (0-(coords_to_use[i][0]-p1_lat)/stepsizelat)+(resolution[1]/2), 
            ((coords_to_use[i+1][1]-p1_long)/stepsizelong)+(resolution[0]/2),
            (0-(coords_to_use[i+1][0]-p1_lat)/stepsizelat)+(resolution[1]/2)
            ), 
            fill=(255,255,255))

    




img.save("single_output 500m.png")
