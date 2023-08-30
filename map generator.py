import orjson
import math
import time
import datetime
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter
import scipy
from scipy import interpolate
import numpy as np
#import pyrosm 
#from pyrosm import OSM
#from pyrosm import get_data
from bs4 import BeautifulSoup

# Hardcoded Settings ############################
Zoom_level_min = 0.005


# User Settings #################################
Max_Node_Distance = 500 # Metres
Start_Datetime = [2017,1,1,0,0,0] # Y,M,D,H,M,S
End_Datetime = [2023,7,28,23,59,59] # Y,M,D,H,M,S
Draw_Line = True
Animated = False
Frames = 300
Resolution = (1080*8, 1080*8)
Minimumm_Accuracy = 12
p1_lat = 43.462313 
p1_long = -80.519346  
GPS_Data_Files = ["E:\Programming\Projects\maps\Location History 29-08-2023.json", "E:\Programming\Projects\maps\Location History 08-07-2023.json"]

# Spline Control Points ####################
Zoom = [100, 1, 0]
Zoom_frames = [0, 200, 299]
Zoom_slopes = [-1, 0, 0]

Lat_center_points = [43, 43]
Lat_center_frames = [0, 200]
Lat_center_slopes = [0, 0]

Long_center_points = [-83, -83]
Long_center_frames = [0, 200]
Long_center_slopes = [0, 0]


# Loads data #########################
location_lists = []

for index, file in np.ndenumerate(GPS_Data_Files):
    with open(file, "rb") as f:
        json_data1 = orjson.loads(f.read())
        
        array = json_data1["locations"]
        location_lists.append(array)


# Functions ###########################
def Zoom_control():
    global Zoom_level
    Zoom_level = np.zeros(Frames)

    Zoom_cubic_coefficents = np.zeros((len(Zoom)-1, 4))
    
    for x in range(len(Zoom_frames)-1):
        M = [
        [Zoom_frames[x]**3,Zoom_frames[x]**2,Zoom_frames[x],1],
        [Zoom_frames[x+1]**3,Zoom_frames[x+1]**2,Zoom_frames[x+1],1],
        [3*Zoom_frames[x]**2,2*Zoom_frames[x],1,0],
        [3*Zoom_frames[x+1]**2,2*Zoom_frames[x+1],1,0]
        ]

        y = [Zoom[x],Zoom[x+1],Zoom_slopes[x],Zoom_slopes[x+1]]

        solution = np.matmul(np.linalg.inv(M), y)
        Zoom_cubic_coefficents[x] = solution

        for Frame in range(Frames):
            if Zoom_frames[x] <= Frame <= Zoom_frames[x+1]:  # Ensures correct coefficents are used for each section of the spline curve 
                Zoom_level[Frame] = 0.005 + ((Zoom_cubic_coefficents[x][0]*Frame**3 + Zoom_cubic_coefficents[x][1]*Frame**2 + Zoom_cubic_coefficents[x][2]*Frame + Zoom_cubic_coefficents[x][3]) - 0) * (180 - 0.005) / (100 - 0)


def Lat_control ():
    global Lat_center
    Lat_center = np.zeros(Frames)

    Lat_cubic_coefficents = np.zeros((len(Lat_center_points)-1, 4))

    for x in range(len(Lat_center_points)-1):
        M = [
        [Lat_center_frames[x]**3,Lat_center_frames[x]**2,Lat_center_frames[x],1],
        [Lat_center_frames[x+1]**3,Lat_center_frames[x+1]**2,Lat_center_frames[x+1],1],
        [3*Lat_center_frames[x]**2,2*Lat_center_frames[x],1,0],
        [3*Lat_center_frames[x+1]**2,2*Lat_center_frames[x+1],1,0]
        ]

        y = [Lat_center_points[x],Lat_center_points[x+1],Lat_center_slopes[x],Lat_center_slopes[x+1]]

        solution = np.matmul(np.linalg.inv(M), y)

        Lat_cubic_coefficents[x] = solution

        for Frame in range(Frames):
            if Zoom_frames[x] <= Frame <= Zoom_frames[x+1]: 
                Lat_center[Frame] 

    
def Long_control ():
    Long_cubic_coefficents = np.zeros((len(Long_center_points)-1, 4))

    for x in range(len(Long_center_points)-1):
        M = [
        [Long_center_frames[x]**3,Long_center_frames[x]**2,Long_center_frames[x],1],
        [Long_center_frames[x+1]**3,Long_center_frames[x+1]**2,Long_center_frames[x+1],1],
        [3*Long_center_frames[x]**2,2*Long_center_frames[x],1,0],
        [3*Long_center_frames[x+1]**2,2*Long_center_frames[x+1],1,0]
        ]

        y = [Long_center_points[x],Long_center_points[x+1],Long_center_slopes[x],Long_center_slopes[x+1]]

        solution = np.matmul(np.linalg.inv(M), y)

        Long_cubic_coefficents[x] = solution

    print(Long_cubic_coefficents)


if Animated == True:
    Zoom_control()
    Lat_control()
    Long_control()

pairs = []

for y in range(len(location_lists)):
    a = [(int(i["latitudeE7"])/1e7,      # Latitude
            int(i["longitudeE7"])/1e7,     # Longitude
            int((i["timestamp"][0:4])),    # Year
            int((i["timestamp"][5:7])),    # Month
            int((i["timestamp"][8:10])),   # Day
            int((i["timestamp"][11:13])),  # Hour
            int((i["timestamp"][14:16])),  # Minute
            int((i["timestamp"][17:19])), # Second
            int((i["accuracy"])))  # Accuracy 
            for i in location_lists[y] if "latitudeE7" in i.keys()]
              
    pairs.append(a)

print(len(pairs))
print(len(pairs[0]))
print(len(pairs[1]))
time.sleep(1)

# For an animation ####################
if Animated == True:
    for k in range(0, Frames, 1):
        print(k)
        if k < 200:
            p1_lat = 43.504650 #* k / 200
            p1_long = -80.505161 #* k / 200
        else:
            p1_lat = 43.462313 
            p1_long = -80.519346 

        lat_height = Zoom_level[k] #cs_lat_height(k)
        long_width = Resolution[0]/Resolution[1] * lat_height


        lat1 = p1_lat - lat_height/2
        lat2 = p1_lat + lat_height/2
        long1 = p1_long - long_width/2
        long2 = p1_long + long_width/2


        stepsizelong = (long2 - long1)/Resolution[0]
        stepsizelat = (lat2 - lat1)/Resolution[1]


        coords_to_use = []
        a = []

        for i in range(len(pairs)):
            for coords in pairs[i]:
                if lat1 <= coords[0] <=lat2:
                    if long1 <= coords[1] <= long2:
                        if coords[8] <= 30:
                            a.append(coords)
            
            coords_to_use.append(a)

        

        img1 = Image.new('RGB', (Resolution[0], Resolution[1]), 'black')
        img2 = Image.new('RGB', (Resolution[0], Resolution[1]), 'black')


        draw1 = ImageDraw.Draw(img1)
        for i in range(len(coords_to_use)):
            if i < len(coords_to_use)-1:
                distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use[i][0] - coords_to_use[i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use[i][0])) * math.cos(math.radians(coords_to_use[i+1][0])) * (math.sin(math.radians(coords_to_use[i][1] - coords_to_use[i+1][1])/2)**2)))
                t = (coords_to_use[i][2], coords_to_use[i][3], coords_to_use[i][4], coords_to_use[i][5], coords_to_use[i][6], coords_to_use[i][7], 0, 0, 0)
                t2 = (coords_to_use[i+1][2], coords_to_use[i+1][3], coords_to_use[i+1][4], coords_to_use[i+1][5], coords_to_use[i+1][6], coords_to_use[i+1][7], 0, 0, 0)
                #print(t)

                time_between = time.mktime(t2) - time.mktime(t)
                #print(time_between)
                if time_between <= 30:
                    lat_offset = math.sin(math.radians(coords_to_use[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset = (math.cos(math.radians(coords_to_use[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[i][1]-p1_long))

                    lat_offset2 = math.sin(math.radians(coords_to_use[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset2 = (math.cos(math.radians(coords_to_use[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[i+1][1]-p1_long))

                    if Draw_Line == True:
                        print(time.mktime(t))
                        print(time.mktime((2023, 11, 1)))
                        time.sleep(1)

                        if time.mktime(t) >= time.mktime((2023, 11, 1)):
                            draw1.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=(255,0,0)
                            )
                        else:
                            draw1.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=(0,0,255)
                            )

                    else:
                        draw1.point(
                            (
                            long_offset*Resolution[0]/2+Resolution[0]/2, 
                            -lat_offset*Resolution[1]/2+Resolution[1]/2
                            ), 
                            fill=(255,255,255)
                        )
        '''
        draw = ImageDraw.Draw(img1)
        for i in range(len(coords_to_use)):
            if i < len(coords_to_use)-1:
                distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use[i][0] - coords_to_use[i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use[i][0])) * math.cos(math.radians(coords_to_use[i+1][0])) * (math.sin(math.radians(coords_to_use[i][1] - coords_to_use[i+1][1])/2)**2)))
                t = (coords_to_use[i][2], coords_to_use[i][3], coords_to_use[i][4], coords_to_use[i][5], coords_to_use[i][6], coords_to_use[i][7], 0, 0, 0)
                t2 = (coords_to_use[i+1][2], coords_to_use[i+1][3], coords_to_use[i+1][4], coords_to_use[i+1][5], coords_to_use[i+1][6], coords_to_use[i+1][7], 0, 0, 0)
                #print(t)

                time_between = time.mktime(t2) - time.mktime(t)
                #print(time_between)
                if time_between <= 30:
                    lat_offset = math.sin(math.radians(coords_to_use[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset = (math.cos(math.radians(coords_to_use[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[i][1]-p1_long))

                    lat_offset2 = math.sin(math.radians(coords_to_use[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset2 = (math.cos(math.radians(coords_to_use[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[i+1][1]-p1_long))

                    if Draw_line == True:
                        draw.line(
                            (
                            long_offset*Resolution[0]/2+Resolution[0]/2, 
                            -lat_offset*Resolution[1]/2+Resolution[1]/2,
                            long_offset2*Resolution[0]/2+Resolution[0]/2, 
                            -lat_offset2*Resolution[1]/2+Resolution[1]/2
                            ), 
                            fill=(255,255,255)
                        )

                    else:
                        draw.point(
                            (
                            long_offset*Resolution[0]/2+Resolution[0]/2, 
                            -lat_offset*Resolution[1]/2+Resolution[1]/2
                            ), 
                            fill=(255,255,255)
                        )


        img.save("e:\Programming\Projects\maps\Frames\Zoom 295- accuracy" + str(k) + ".png")'''

# For a static image #################
if Animated == False:
    lat_height = 3
    long_width = Resolution[0]/Resolution[1] * lat_height


    lat1 = p1_lat - lat_height/2
    lat2 = p1_lat + lat_height/2
    long1 = p1_long - long_width/2
    long2 = p1_long + long_width/2


    stepsizelong = (long2 - long1)/Resolution[0]
    stepsizelat = (lat2 - lat1)/Resolution[1]


    

    coords_to_use = []
    a = []

    ### this is running everything twice or something, it's taking way to long
    for i in range(len(pairs)):
        for coords in pairs[i]:
            if coords[8] <= Minimumm_Accuracy:
                if lat1 <= coords[0] <=lat2:
                    if long1 <= coords[1] <= long2:
                        a.append(coords)
            
        coords_to_use.append(a)

    print(len(coords_to_use))


    img1 = Image.new('RGB', (Resolution[0], Resolution[1]), 'black')
    img2 = Image.new('RGB', (Resolution[0], Resolution[1]), 'black')


    draw1 = ImageDraw.Draw(img1)
    draw2 = ImageDraw.Draw(img2)

    for i in range(len(coords_to_use[0])-1):
        
        distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use[0][i][0] - coords_to_use[0][i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use[0][i][0])) * math.cos(math.radians(coords_to_use[0][i+1][0])) * (math.sin(math.radians(coords_to_use[0][i][1] - coords_to_use[0][i+1][1])/2)**2)))
        t = (coords_to_use[0][i][2], coords_to_use[0][i][3], coords_to_use[0][i][4], coords_to_use[0][i][5], coords_to_use[0][i][6], coords_to_use[0][i][7], 0, 0, 0)
        t2 = (coords_to_use[0][i+1][2], coords_to_use[0][i+1][3], coords_to_use[0][i+1][4], coords_to_use[0][i+1][5], coords_to_use[0][i+1][6], coords_to_use[0][i+1][7], 0, 0, 0)
        
        time_between = time.mktime(t2) - time.mktime(t)

        if time_between > 0:
            speed = distance / time_between
        else:
            speed = 0

        if distance <= 2000:
            if time_between <= 240:
                if 0.01 <= speed <= 50:
                    lat_offset = math.sin(math.radians(coords_to_use[0][i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset = (math.cos(math.radians(coords_to_use[0][i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[0][i][1]-p1_long))
                    lat_offset2 = math.sin(math.radians(coords_to_use[0][i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset2 = (math.cos(math.radians(coords_to_use[0][i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[0][i+1][1]-p1_long))


                    if Draw_Line == True:
                        if time.mktime(t) >= time.mktime((2022, 11, 1, 0, 0, 0, 0, 0, 0)):
                            draw2.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=(255,0,0)
                            )
                        else:
                            draw1.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=(0,0,255)
                            )

    
            
    im1arr = np.asarray(img1)
    im2arr = np.asarray(img2)

    im = im2arr + im1arr

    img = Image.fromarray(im)


    img.save("e:\Programming\Projects\maps\Static Render.png")
