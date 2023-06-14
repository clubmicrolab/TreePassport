
import numpy as np  
import cv2 
from color_map_fastiecm  import fastiecm 
import os 



def calculate_vegetation_index_and_save_img(image): 
    contrasted = add_contrast(image) 
    ndvi = calculate_ndvi(contrasted)
    ndvi_contrasted = add_contrast(ndvi)
    color_mapped_prep = ndvi_contrasted.astype(np.uint8) 
    color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm) 
    
    current_location = os.getcwd() 
    directory = f'{current_location}/vegetation_map_ndvi' 
    IMG_COUNTER = len(os.listdir(directory))
    cv2.imwrite(f'{directory}/kek{IMG_COUNTER+1}.png', color_mapped_image) 
    return color_mapped_image




def add_contrast(img): 
    im = img.copy()
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out 

def calculate_ndvi(img):
    image = img.copy()
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi