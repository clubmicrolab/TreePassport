
import numpy as np 
from math import pi

def calculate_crown_size(image,radius,drone_altitude = 30,camera_angle_view = 77): 
    """ Altitude: m, Camera Angle View: degrees """
    camera_x = image.shape[0]
    camera_y = image.shape[1] 
    
    camera_swath =  camera_y if camera_y > camera_x else camera_x   
     
    pixel_coef = ((np.tan(camera_angle_view/2) * drone_altitude) * 2) / camera_swath  
    
    # Area Of The Circle
    return  int(  pi * ((radius*pixel_coef) **2) )
    