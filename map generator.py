import json
import math
import time
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter

 


def color(x):

    if (x < 33):
        r = x*3
        g = 0
        b = 0
    elif (x < 66):
        r = 1
        g = x*3 - 33
        b = 0
    else:
        r = 1
        g = 1
        b = x*3 - 66
    
    return (round(r), round(g), round(b))

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

print(stepsizelong)
print(stepsizelat)

coords_to_use = []

for coords in pairs:
    if lat1 <= coords[0] <=lat2:
        if long1 <= coords[1] <= long2:
            coords_to_use.append(coords)
            
    
#coords_to_use = [(45, -80), (46, -81.7777)]

#print(coords_to_use[0][0])
#print(coords_to_use[0][1])
#print(coords_to_use[1][0])
#print(coords_to_use[1][1])

img = Image.new('RGB', (resolution[0], resolution[1]), 'black')



draw = ImageDraw.Draw(img)
for i in range(len(coords_to_use)):
    #coords_to_use[i][0] = abs(90-coords_to_use[i][0])
    #coords_to_use[i][0] = abs(180-coords_to_use[i][0])

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

            #print((coords_to_use[i][1]-p1_long)+(resolution[0]/2))
            #print((coords_to_use[i][0]-p1_lat)+(resolution[1]/2))

            #print(((coords_to_use[i][1]-p1_long)/stepsizelong)+(resolution[0]/2))
            #print(((coords_to_use[i][0]-p1_lat)/stepsizelat)+(resolution[1]/2))
            #print(((coords_to_use[i+1][1]-p1_long)/stepsizelong)+(resolution[0]/2))
            #print(((coords_to_use[i+1][0]-p1_lat)/stepsizelat)+(resolution[1]/2))
    




img.save("single_output 500m.png")

#time.sleep(5)

'''
txt = input("Input height, latitude range, longitude range, inital latitude, and inital longitude: ")
txt = txt.split()
height = int(txt[0])
rectheight = float(txt[1])
rectwidth = float(txt[2])
inital_lat = float(txt[3])
inital_long = float(txt[4])


txt = input("Select mode; Center or Corner: ")
mode = txt
print(type(mode))

if mode == "corner":
    lat1 = inital_lat
    lat2 = lat1 + rectheight
    long1 = inital_long
    long2 = long1 + rectwidth
    print("mode is corner")
elif mode == "center":
    lat1 = inital_lat - rectheight/2
    lat2 = inital_lat + rectheight/2
    long1 = inital_long - rectwidth/2
    long2 = inital_long + rectwidth/2
    print("mode is center")
'''



'''
y_list = [[0] * width for i in range(height)]

maxvalue = 0


for i in pairs:
    index_x = math.floor((i[1]-long1)/stepsizelong)
    index_y = math.floor((i[0]-lat1)/stepsizelat)
    if index_x > 0 and index_x < width and index_y > 0 and index_y < height:
        if (y_list[index_y][index_x] > maxvalue):
            maxvalue = y_list[index_y][index_x]
        for k in [-1, 0 , 1]:
            for l in [-1, 0, 1]:
                if k == 0 and l == 0:
                    y_list[index_y + k][index_x + l] += 1  
                else:
                    y_list[index_y + k][index_x + l] += 0.5  


img = Image.new('RGB', (width, height), 'black')

maxvalue = math.log(maxvalue,10)
'''






'''
for j, xlist in enumerate(y_list):
    for i, x in enumerate(xlist):
        intensity = round(100*math.log(x+1)/maxvalue)
        pixels[i,height - j - 1] = color(intensity)
'''
 

