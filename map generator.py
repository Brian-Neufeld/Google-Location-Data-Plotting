import orjson
import math
import time
import datetime
from PIL import Image, ImageDraw, ImageFont
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
Start_DateTime = (2017,1,1,0,0,0) # Y,M,D,H,M,S
Start_DateTime_Unix = time.mktime(datetime.datetime(2017,1,1,0,0,0).timetuple())
End_DateTime = (2025,1,1,0,0,0) # Y,M,D,H,M,S
End_DateTime_Unix = time.mktime(datetime.datetime(2025,1,1,0,0,0).timetuple())
Draw_Line = True
Animated = False
Frames = 300
Resolution = (1080*8, 1080*8)
Minimumm_Accuracy = 36
p1_lat = 43.462313 
p1_long = -80.519346  
GPS_Data_Files = ["E:\Programming\Projects\maps\Location Data 2024-04-06.json"]

# Spline Control Points ####################
Zoom = [2, 2]
Zoom_frames = [0, 365*3]
Zoom_slopes = [0, 0]

Lat_center_points = [43.462313, 43.462313]
Lat_center_frames = [0, 365*3]
Lat_center_slopes = [0, 0]

Long_center_points = [-80.519346, -80.519346]
Long_center_frames = [0, 365*3]
Long_center_slopes = [0, 0]


# Loads data #########################
location_lists = []

for index, file in np.ndenumerate(GPS_Data_Files):
    with open(file, "rb") as f:
        json_data1 = orjson.loads(f.read())
        
        array = json_data1["locations"]
        location_lists.append(array)


# Functions ###########################
# The following functions take the information under spline control points and generates the values for each frame
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

    #print(Long_cubic_coefficents)


if Animated == True:
    Zoom_control()
    Lat_control()
    Long_control()


points = []

'''for y in range(len(location_lists)):
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
        


    points.append(a)'''

for y in range(len(location_lists)):
    a = [(int(i["latitudeE7"])/1e7,      # Latitude
            int(i["longitudeE7"])/1e7,     # Longitude
            int(time.mktime(datetime.datetime(int((i["timestamp"][0:4])), int((i["timestamp"][5:7])), int((i["timestamp"][8:10])), int((i["timestamp"][11:13])), int((i["timestamp"][14:16])), int((i["timestamp"][17:19]))).timetuple())),
            int((i["accuracy"])))  # Accuracy 
            for i in location_lists[y] if "latitudeE7" in i.keys()]
    
    points.append(a)



# For an animation ####################

# For a static image #################
if Animated == False:
    lat_height = 4
    long_width = Resolution[0]/Resolution[1] * lat_height


    lat1 = p1_lat - lat_height/2
    lat2 = p1_lat + lat_height/2
    long1 = p1_long - long_width/2
    long2 = p1_long + long_width/2


    stepsizelong = (long2 - long1)/Resolution[0]
    stepsizelat = (lat2 - lat1)/Resolution[1]


    

    coords_to_use = []
    a = []

    print("Organizing points")
    for i in range(len(points[0])):
        print(round(i/len(points[0])*100))
        z = points[0][i] 
        if z[3] <= 36:
            if Start_DateTime_Unix <= z[2] <= End_DateTime_Unix:
                if lat1 <= z[0] <=lat2:
                    if long1 <= z[1] <= long2:
                        a.append(z)
                
            
    coords_to_use.append(a)



    img1 = Image.new('RGBA', (Resolution[0], Resolution[1]), (150, 150, 150, 255))
    img2 = Image.new('RGBA', (Resolution[0], Resolution[1]), (0, 0, 0, 0))
    img3 = Image.new('RGBA', (Resolution[0], Resolution[1]), (0, 0, 0, 0))
    img4 = Image.new('RGBA', (Resolution[0], Resolution[1]), (0, 0, 0, 0))
    img5 = Image.new('RGBA', (Resolution[0], Resolution[1]), (0, 0, 0, 0))
    img6 = Image.new('RGBA', (Resolution[0], Resolution[1]), (0, 0, 0, 0))


    draw1 = ImageDraw.Draw(img1)
    draw2 = ImageDraw.Draw(img2)
    draw3 = ImageDraw.Draw(img3)
    draw4 = ImageDraw.Draw(img4)
    draw5 = ImageDraw.Draw(img5)
    draw6 = ImageDraw.Draw(img6)

    for i in range(len(coords_to_use[0])-1):
        if round(i/(len(coords_to_use[0])-1)*100) % 1 == 0:
            print(round(i/(len(coords_to_use[0])-1)*100))
        distance = (2*6378.137*1000) * math.asin(math.sqrt((math.sin((math.radians(coords_to_use[0][i][0] - coords_to_use[0][i+1][0]))/2)**2) + math.cos(math.radians(coords_to_use[0][i][0])) * math.cos(math.radians(coords_to_use[0][i+1][0])) * (math.sin(math.radians(coords_to_use[0][i][1] - coords_to_use[0][i+1][1])/2)**2)))
        t = coords_to_use[0][i][2]
        t2 = coords_to_use[0][i+1][2]
        
        time_between = t2 - t

        if time_between > 0:
            speed = distance / time_between
        else:
            speed = 0

        if distance <= 750:
            if time_between <= 240:
                if 0.001 <= speed <= 100:
                    lat_offset = math.sin(math.radians(coords_to_use[0][i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset = (math.cos(math.radians(coords_to_use[0][i][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[0][i][1]-p1_long))
                    lat_offset2 = math.sin(math.radians(coords_to_use[0][i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))
                    long_offset2 = (math.cos(math.radians(coords_to_use[0][i+1][0]-p1_lat)) / math.sin(math.radians(lat_height/2))) * math.sin(math.radians(coords_to_use[0][i+1][1]-p1_long))

                    font = ImageFont.truetype(r'c:\Users\Brian\Desktop\AdobeGothicStd-Bold.otf', 50)

                    draw1.text((0,0), "speed <= " + str(round(20*3.6)), fill=(0,0,255), font=font)
                    draw2.text((0,100), str(round(20*3.6)) + " < speed <= " + str(round(25*3.6)), fill=(0,255,0), font=font)
                    draw3.text((0,200), str(round(25*3.6)) + " < speed <= " + str(round(30*3.6)), fill=(255,255,0), font=font)
                    draw4.text((0,300), str(round(30*3.6)) + " < speed <= " + str(round(35*3.6)), fill=(255,127,0), font=font)
                    draw5.text((0,400), str(round(35*3.6)) + " < speed <= " + str(round(40*3.6)), fill=(255,0,0), font=font)
                    draw6.text((0,500), str(round(40*3.6)) + " < speed", fill=(255,0,255), font=font)

                    if Draw_Line == True:
                        if speed <= 20:
                            Linefill = (0,0,255)
                            draw1.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=Linefill
                            )
                        
                        elif 20 < speed <= 25:
                            Linefill = (0,255,0)
                            draw2.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=Linefill
                            )

                        elif 25 < speed <= 30:
                            Linefill = (255,255,0)
                            draw3.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=Linefill
                            )

                        elif 30 < speed <= 35:
                            Linefill = (255,127,0)
                            draw4.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=Linefill
                            )

                        elif 35 < speed <= 40:
                            Linefill = (255,0,0)
                            draw5.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=Linefill
                            )

                        elif 45 < speed:
                            Linefill = (255,0,255)
                            draw6.line(
                                (
                                long_offset*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset*Resolution[1]/2+Resolution[1]/2,
                                long_offset2*Resolution[0]/2+Resolution[0]/2, 
                                -lat_offset2*Resolution[1]/2+Resolution[1]/2
                                ), 
                                fill=Linefill
                            )

                        

                        '''if time.mktime(t) >= time.mktime((2022, 11, 1, 0, 0, 0, 0, 0, 0)):
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
                            )'''

    
            
    img = Image.alpha_composite(img1, img2)
    img = Image.alpha_composite(img, img3)
    img = Image.alpha_composite(img, img4)
    img = Image.alpha_composite(img, img5)
    img = Image.alpha_composite(img, img6)


    img.save("e:\Programming\Projects\maps\Static Render.png")
    img1.save("e:\Programming\Projects\maps\Static Render1.png")
    img2.save("e:\Programming\Projects\maps\Static Render2.png")
    img3.save("e:\Programming\Projects\maps\Static Render3.png")
    img4.save("e:\Programming\Projects\maps\Static Render4.png")
    img5.save("e:\Programming\Projects\maps\Static Render5.png")
    img6.save("e:\Programming\Projects\maps\Static Render6.png")
