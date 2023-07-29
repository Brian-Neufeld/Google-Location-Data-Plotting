import json
import math
import time
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter
import scipy
from scipy import interpolate
import numpy as np


# Settings #################################
Line_distance = 500 # Metres
Start_datetime = [2017,1,1,0,0,0] # Y,M,D,H,M,S
End_datetime = [2023,7,28,23,59,59] # Y,M,D,H,M,S
Draw_line = True
Animated = True
Frames = 300


datasource = open("e:\Programming\Projects\maps\Location History 28-07-2023.json","r")

datadict = json.load(datasource)

locationlist = datadict["locations"]


pairs = [(int(i["latitudeE7"])/1e7,     # Latitude
          int(i["longitudeE7"])/1e7,    # Longitude
          int((i["timestamp"][0:4])),   # Year
          int((i["timestamp"][5:7])),   # Month
          int((i["timestamp"][8:10])),  # Day
          int((i["timestamp"][11:13])), # Hour
          int((i["timestamp"][14:16])), # Minute
          int((i["timestamp"][17:19]))) # Second
          for i in locationlist if "latitudeE7" in i.keys()]



Frames = 300

lat_height_points = [180, 20, 10, 1, 0.5, 0.01]
lat_height_frames = [0, 75, 125, 225, 250, 299]

cs_lat_height = interpolate.CubicSpline(lat_height_frames, lat_height_points)

xs = np.arange(0, Frames, 1)

plt.plot(xs, cs_lat_height(xs))
plt.show()

for k in range(0, 1, 1):
    print(k)
    resolution = (1080*4, 1080*4)
    if k < 200:
        p1_lat = 43.467034 #* k / 200
        p1_long = -80.518941 #* k / 200
    else:
        p1_lat = 43.467034 
        p1_long = -80.518941 

    lat_height = 5 #cs_lat_height(k)
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


    
    for i in range(-180, 180, 5):
        coords_to_use.append((5*i,0))

    for i in range(-180, 180, 5):
        coords_to_use.append((5*i,90))

    for i in range(-180, 180, 5):
        coords_to_use.append((0,5*i))
    

    draw = ImageDraw.Draw(img)
    for i in range(len(coords_to_use)):
        if i < len(coords_to_use)-1:
            distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use[i][0] - coords_to_use[i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use[i][0])) * math.cos(math.radians(coords_to_use[i+1][0])) * (math.sin(math.radians(coords_to_use[i][1] - coords_to_use[i+1][1])/2)**2)))
        
            '''if distance < 500000:
                draw.line(
                (
                ((coords_to_use[i][1]-p1_long)/stepsizelong)+(resolution[0]/2),
                (0-(coords_to_use[i][0]-p1_lat)/stepsizelat)+(resolution[1]/2), 
                ((coords_to_use[i+1][1]-p1_long)/stepsizelong)+(resolution[0]/2),
                (0-(coords_to_use[i+1][0]-p1_lat)/stepsizelat)+(resolution[1]/2)
                ), 
                fill=(round(i/len(coords_to_use)*255),round((len(coords_to_use)-i)/len(coords_to_use)*255),0))'''
            
            if distance < 500:
                lat_offset = math.sin(math.radians(coords_to_use[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                long_offset = (math.cos(math.radians(coords_to_use[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[i][1]-p1_long))

                lat_offset2 = math.sin(math.radians(coords_to_use[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                long_offset2 = (math.cos(math.radians(coords_to_use[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[i+1][1]-p1_long))


                draw.line(
                    (
                    long_offset*resolution[0]/2+resolution[0]/2, 
                    -lat_offset*resolution[1]/2+resolution[1]/2,
                    long_offset2*resolution[0]/2+resolution[0]/2, 
                    -lat_offset2*resolution[1]/2+resolution[1]/2
                    ), 
                    fill=(255,255,255)
                )

                '''
                draw.point(
                    (
                    long_offset*resolution[0]/2+resolution[0]/2, 
                    -lat_offset*resolution[1]/2+resolution[1]/2
                    ), 
                    fill=(255,255,255)
                )'''

        




    img.save("e:\Programming\Projects\maps\Frames\Sphere_zoom" + str(k) + ".png")

    
