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


# Settings #################################
Line_distance = 500 # Metres
Start_datetime = [2017,1,1,0,0,0] # Y,M,D,H,M,S
End_datetime = [2023,7,28,23,59,59] # Y,M,D,H,M,S
Draw_line = True
Animated = False
Frames = 300
resolution = (1080*2, 1080*2)
accuracy = 60
p1_lat = 43.063
p1_long = -80.676 
data_files = ["E:\Programming\Projects\maps\Location History 09-08-2023.json", "E:\Programming\Projects\maps\Location History 17-03-2020.json"]

# Spline Control Points ####################
# zoom 100% fills image with globe, 0% is 0.005, > 100% shows entire globe with blank space around it. 
Zoom_level = 1

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
with open("E:\Programming\Projects\maps\Location History 09-08-2023.json", "rb") as f:
    json_data1 = orjson.loads(f.read())

locationlist1 = json_data1["locations"]

with open("E:\Programming\Projects\maps\Dom's Location History.json", "rb") as f:
    json_data2 = orjson.loads(f.read())

locationlist2 = json_data2["locations"]

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

#datasource = "E:\Programming\Projects\maps\Location History 09-08-2023.json"

#datadict = json.loads(datasource)




pairs1 = [(int(i["latitudeE7"])/1e7,      # Latitude
          int(i["longitudeE7"])/1e7,     # Longitude
          int((i["timestamp"][0:4])),    # Year
          int((i["timestamp"][5:7])),    # Month
          int((i["timestamp"][8:10])),   # Day
          int((i["timestamp"][11:13])),  # Hour
          int((i["timestamp"][14:16])),  # Minute
          int((i["timestamp"][17:19])), # Second
          int((i["accuracy"])))  # Accuracy 
          for i in locationlist1 if "latitudeE7" in i.keys()]

pairs2 = [(int(i["latitudeE7"])/1e7,      # Latitude
          int(i["longitudeE7"])/1e7,     # Longitude
          int((i["timestamp"][0:4])),    # Year
          int((i["timestamp"][5:7])),    # Month
          int((i["timestamp"][8:10])),   # Day
          int((i["timestamp"][11:13])),  # Hour
          int((i["timestamp"][14:16])),  # Minute
          int((i["timestamp"][17:19])), # Second
          int((i["accuracy"])))  # Accuracy 
          for i in locationlist2 if "latitudeE7" in i.keys()]


# For an animation ####################
if Animated == True:
    for k in range(0, Frames, 1):
        print(k)
        if k < 200:
            p1_lat = 43.504650 #* k / 200
            p1_long = -80.505161 #* k / 200
        else:
            p1_lat = 43.504650 
            p1_long = -80.505161 

        lat_height = Zoom_level[k] #cs_lat_height(k)
        long_width = resolution[0]/resolution[1] * lat_height


        lat1 = p1_lat - lat_height/2
        lat2 = p1_lat + lat_height/2
        long1 = p1_long - long_width/2
        long2 = p1_long + long_width/2


        stepsizelong = (long2 - long1)/resolution[0]
        stepsizelat = (lat2 - lat1)/resolution[1]


        coords_to_use1 = []
        coords_to_use2 = []

        for coords in pairs1:
            if lat1 <= coords[0] <=lat2:
                if long1 <= coords[1] <= long2:
                    if coords[8] <= 30:
                        coords_to_use1.append(coords)

        for coords in pairs2:
            if lat1 <= coords[0] <=lat2:
                if long1 <= coords[1] <= long2:
                    if coords[8] <= 30:
                        coords_to_use2.append(coords)

        img1 = Image.new('RGB', (resolution[0], resolution[1]), 'black')
        img2 = Image.new('RGB', (resolution[0], resolution[1]), 'black')


        draw1 = ImageDraw.Draw(img1)
        for i in range(len(coords_to_use1)):
            if i < len(coords_to_use1)-1:
                distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use1[i][0] - coords_to_use1[i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use1[i][0])) * math.cos(math.radians(coords_to_use1[i+1][0])) * (math.sin(math.radians(coords_to_use1[i][1] - coords_to_use1[i+1][1])/2)**2)))
                t = (coords_to_use1[i][2], coords_to_use1[i][3], coords_to_use1[i][4], coords_to_use1[i][5], coords_to_use1[i][6], coords_to_use1[i][7], 0, 0, 0)
                t2 = (coords_to_use1[i+1][2], coords_to_use1[i+1][3], coords_to_use1[i+1][4], coords_to_use1[i+1][5], coords_to_use1[i+1][6], coords_to_use1[i+1][7], 0, 0, 0)
                #print(t)

                time_between = time.mktime(t2) - time.mktime(t)
                #print(time_between)
                if time_between <= 30:
                    lat_offset = math.sin(math.radians(coords_to_use1[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset = (math.cos(math.radians(coords_to_use1[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use1[i][1]-p1_long))

                    lat_offset2 = math.sin(math.radians(coords_to_use1[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset2 = (math.cos(math.radians(coords_to_use1[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use1[i+1][1]-p1_long))

                    if Draw_line == True:
                        draw1.line(
                            (
                            long_offset*resolution[0]/2+resolution[0]/2, 
                            -lat_offset*resolution[1]/2+resolution[1]/2,
                            long_offset2*resolution[0]/2+resolution[0]/2, 
                            -lat_offset2*resolution[1]/2+resolution[1]/2
                            ), 
                            fill=(255,255,255)
                        )

                    else:
                        draw1.point(
                            (
                            long_offset*resolution[0]/2+resolution[0]/2, 
                            -lat_offset*resolution[1]/2+resolution[1]/2
                            ), 
                            fill=(255,255,255)
                        )
        '''
        draw = ImageDraw.Draw(img1)
        for i in range(len(coords_to_use)):
            if i < len(coords_to_use)-1:
                distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use1[i][0] - coords_to_use1[i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use1[i][0])) * math.cos(math.radians(coords_to_use1[i+1][0])) * (math.sin(math.radians(coords_to_use1[i][1] - coords_to_use1[i+1][1])/2)**2)))
                t = (coords_to_use1[i][2], coords_to_use1[i][3], coords_to_use1[i][4], coords_to_use1[i][5], coords_to_use1[i][6], coords_to_use1[i][7], 0, 0, 0)
                t2 = (coords_to_use1[i+1][2], coords_to_use1[i+1][3], coords_to_use1[i+1][4], coords_to_use1[i+1][5], coords_to_use1[i+1][6], coords_to_use1[i+1][7], 0, 0, 0)
                #print(t)

                time_between = time.mktime(t2) - time.mktime(t)
                #print(time_between)
                if time_between <= 30:
                    lat_offset = math.sin(math.radians(coords_to_use1[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset = (math.cos(math.radians(coords_to_use1[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use1[i][1]-p1_long))

                    lat_offset2 = math.sin(math.radians(coords_to_use1[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset2 = (math.cos(math.radians(coords_to_use1[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use1[i+1][1]-p1_long))

                    if Draw_line == True:
                        draw.line(
                            (
                            long_offset*resolution[0]/2+resolution[0]/2, 
                            -lat_offset*resolution[1]/2+resolution[1]/2,
                            long_offset2*resolution[0]/2+resolution[0]/2, 
                            -lat_offset2*resolution[1]/2+resolution[1]/2
                            ), 
                            fill=(255,255,255)
                        )

                    else:
                        draw.point(
                            (
                            long_offset*resolution[0]/2+resolution[0]/2, 
                            -lat_offset*resolution[1]/2+resolution[1]/2
                            ), 
                            fill=(255,255,255)
                        )


        img.save("e:\Programming\Projects\maps\Frames\Zoom 295- accuracy" + str(k) + ".png")'''

# For a static image #################
if Animated == False:
    lat_height = Zoom_level
    long_width = resolution[0]/resolution[1] * lat_height


    lat1 = p1_lat - lat_height/2
    lat2 = p1_lat + lat_height/2
    long1 = p1_long - long_width/2
    long2 = p1_long + long_width/2


    stepsizelong = (long2 - long1)/resolution[0]
    stepsizelat = (lat2 - lat1)/resolution[1]


    

    coords_to_use1 = []
    coords_to_use2 = []

    for coords in pairs1:
        if lat1 <= coords[0] <=lat2:
            if long1 <= coords[1] <= long2:
                if coords[8] <= 30:
                    coords_to_use1.append(coords)

    for coords in pairs2:
        if lat1 <= coords[0] <=lat2:
            if long1 <= coords[1] <= long2:
                if coords[8] <= 30:
                    coords_to_use2.append(coords)

    img1 = Image.new('RGB', (resolution[0], resolution[1]), 'black')
    img2 = Image.new('RGB', (resolution[0], resolution[1]), 'black')


    draw1 = ImageDraw.Draw(img1)
    draw2 = ImageDraw.Draw(img2)

    for i in range(len(coords_to_use1)-1):
        
        distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use1[i][0] - coords_to_use1[i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use1[i][0])) * math.cos(math.radians(coords_to_use1[i+1][0])) * (math.sin(math.radians(coords_to_use1[i][1] - coords_to_use1[i+1][1])/2)**2)))
        t = (coords_to_use1[i][2], coords_to_use1[i][3], coords_to_use1[i][4], coords_to_use1[i][5], coords_to_use1[i][6], coords_to_use1[i][7], 0, 0, 0)
        t2 = (coords_to_use1[i+1][2], coords_to_use1[i+1][3], coords_to_use1[i+1][4], coords_to_use1[i+1][5], coords_to_use1[i+1][6], coords_to_use1[i+1][7], 0, 0, 0)
        
        time_between = time.mktime(t2) - time.mktime(t)

        if time_between > 0:
            speed = distance / time_between
        else:
            speed = 0

        if distance <= 500:
            if time_between <= 60:
                if speed <= 45:
                    lat_offset = math.sin(math.radians(coords_to_use1[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset = (math.cos(math.radians(coords_to_use1[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use1[i][1]-p1_long))
                    lat_offset2 = math.sin(math.radians(coords_to_use1[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset2 = (math.cos(math.radians(coords_to_use1[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use1[i+1][1]-p1_long))


                    if Draw_line == True:
                        draw1.line(
                        (
                        long_offset*resolution[0]/2+resolution[0]/2, 
                        -lat_offset*resolution[1]/2+resolution[1]/2,
                        long_offset2*resolution[0]/2+resolution[0]/2, 
                        -lat_offset2*resolution[1]/2+resolution[1]/2
                        ), 
                        fill=(round(255*speed/45), 0, round(255-255*speed/45))
                        )

                    else:
                        draw1.point(
                        (
                        long_offset*resolution[0]/2+resolution[0]/2, 
                        -lat_offset*resolution[1]/2+resolution[1]/2
                        ), 
                        fill=(0,255,0)
                        )

    for i in range(len(coords_to_use2)-1):
        
        distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use2[i][0] - coords_to_use2[i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use2[i][0])) * math.cos(math.radians(coords_to_use2[i+1][0])) * (math.sin(math.radians(coords_to_use2[i][1] - coords_to_use2[i+1][1])/2)**2)))
        t = (coords_to_use2[i][2], coords_to_use2[i][3], coords_to_use2[i][4], coords_to_use2[i][5], coords_to_use2[i][6], coords_to_use2[i][7], 0, 0, 0)
        t2 = (coords_to_use2[i+1][2], coords_to_use2[i+1][3], coords_to_use2[i+1][4], coords_to_use2[i+1][5], coords_to_use2[i+1][6], coords_to_use2[i+1][7], 0, 0, 0)
        
        time_between = time.mktime(t2) - time.mktime(t)
        
        if distance <= 500:
            lat_offset = math.sin(math.radians(coords_to_use2[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
            long_offset = (math.cos(math.radians(coords_to_use2[i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use2[i][1]-p1_long))
            lat_offset2 = math.sin(math.radians(coords_to_use2[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
            long_offset2 = (math.cos(math.radians(coords_to_use2[i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use2[i+1][1]-p1_long))


            if Draw_line == True:
                draw2.line(
                (
                long_offset*resolution[0]/2+resolution[0]/2, 
                -lat_offset*resolution[1]/2+resolution[1]/2,
                long_offset2*resolution[0]/2+resolution[0]/2, 
                -lat_offset2*resolution[1]/2+resolution[1]/2
                ), 
                fill=(255,0,0)
                )

            else:
                draw2.point(
                (
                long_offset*resolution[0]/2+resolution[0]/2, 
                -lat_offset*resolution[1]/2+resolution[1]/2
                ), 
                fill=(255,0,0)
                )
            
    im1arr = np.asarray(img1)
    im2arr = np.asarray(img2)

    addition = im1arr + im2arr

    img = Image.fromarray(addition)


    img1.save("e:\Programming\Projects\maps\Static Render.png")
