from model_singleton import ModelSingleton  
from crown_math import calculate_crown_size 
import cv2 
from deepforest import preprocess
import os 
import threading 
from vegetation_index_ndvi import  calculate_vegetation_index_and_save_img  

from multiprocessing.pool import ThreadPool 
from sklearn.preprocessing import MinMaxScaler 
import numpy as np


def predict_factory_method(image, altitude):
    pool = ThreadPool(processes=1) 
    async_pool_result = pool.apply_async(calculate_vegetation_index_and_save_img, (image,))

    if altitude > 100: 
        # simple segmentation without the ndvi
        predict_crowns_segemented(image,altitude)
    else:
        predict_crowns(image,altitude,async_pool_result)


def predict_crowns(image,altitude,async_pool_result): 
    pred_boxes = ModelSingleton.getInstance().predict_image(image=image[:,:,:3])   
    pred_boxes = pred_boxes[pred_boxes.score > 0.3] 
    ndvi_img = async_pool_result.get() 
    process_save_img(pred_boxes, image, ndvi_img, altitude) 


def predict_crowns_segemented(image,altitude):
    #Create windows of 400px
    windows = preprocess.compute_windows(image, patch_size=400,patch_overlap=0)
    print(f'We have {len(windows)} windows in the image') 
    tile = ModelSingleton.getInstance().predict_tile(image=image,return_plot=False,patch_overlap=0,iou_threshold=0.05,patch_size=400) 
    process_save_img(tile, image,altitude)


def process_save_img(pred_boxes,image, ndvi_img, altitude):  
    img = image.copy()  
    fn_img = image.copy()

    closest_rect = find_closest_rectangle(pred_boxes, fn_img.shape[1], fn_img.shape[0])    
    xmin_closest, xmax_closest, ymax_closest, ymin_closest = closest_rect 

    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0, 255, 0) 
    thickness = 2 

    max_score = pred_boxes.score.max() 
    scaler = MinMaxScaler()

    for index, row in pred_boxes.iterrows():
        cv2.rectangle(img, (int(row["xmin"]), int(row["ymin"])), (int(row["xmax"]), int(row["ymax"])), (0, 0, 0), thickness=10, lineType=cv2.LINE_AA)  
        x_lat =  int(row["xmax"]) - int(row["xmin"])
        y_lat = int(row["ymax"]) - int(row["ymin"])
        x_center =  int(x_lat/2) + int(row["xmin"])
        y_center =  int(y_lat/2) + int(row["ymin"]) 
        
        lat =  int(x_lat/2) if int(x_lat/2) >  int(y_lat/2) else  int(y_lat/2)   

        crown_size = str(calculate_crown_size(img,lat,altitude))
        cv2.putText(img, crown_size,  (x_center, y_center) , font, 0.5, 
                    color, thickness, cv2.LINE_AA, False) 
        
        
        # Crop  IMG
        xmin = int(row["xmin"])
        ymin = int(row["ymin"])
        xmax = int(row["xmax"])
        ymax = int(row["ymax"]) 
        b, g, r = cv2.split(ndvi_img[ymin:ymax, xmin:xmax])

        # Scaler Index 
        red_array_scaled = scaler.fit_transform(r)  
        cv2.rectangle(ndvi_img, (int(row["xmin"]), int(row["ymin"])), (int(row["xmax"]), int(row["ymax"])), (255, 0, 0), thickness=10, lineType=cv2.LINE_AA) 


        vegetation_index = f'{red_array_scaled.mean():.2f}'
        cv2.putText(ndvi_img, vegetation_index,  (x_center, y_center) , font, 0.5, 
                 (255, 0, 0) , thickness, cv2.LINE_AA, False)  

        if int(row["xmax"]) == int(xmax_closest) and int(row["xmin"]) == int(xmin_closest) and int(row["ymin"]) == int(ymin_closest) and  int(row["ymax"]) == int(ymax_closest):
            cv2.rectangle(fn_img, (int(row["xmin"]), int(row["ymin"])), (int(row["xmax"]), int(row["ymax"])), (0, 0, 0), thickness=10, lineType=cv2.LINE_AA)
            cv2.putText(fn_img, crown_size,  (x_center, y_center) , font, 0.5, 
                    color, thickness, cv2.LINE_AA, False)  
            cv2.putText(fn_img, vegetation_index,  (x_center, y_center+50) , font, 0.5, 
                 (0, 0, 255) , thickness, cv2.LINE_AA, False)  




        



    
    current_location = os.getcwd() 
    directory = f'{current_location}/images_recieved' # Replace with the actual directory path
    file_count = len(os.listdir(directory)) 
    new_dir = f'IMGs{file_count+1}'
    os.mkdir(f'{directory}/{new_dir}')
    cv2.imwrite(f'{directory}/{new_dir}/area_of_crowns.png', cv2.cvtColor(img  , cv2.COLOR_BGR2RGB) )  
    cv2.imwrite(f'{directory}/{new_dir}/ndvi_indexes.png', ndvi_img)  
    cv2.imwrite(f'{directory}/{new_dir}/neareast_tree.png', cv2.cvtColor(fn_img  , cv2.COLOR_BGR2RGB)) 





def find_closest_rectangle(pred_boxes, image_width, image_height): 
   
    rectangles = pred_boxes[['xmin', 'xmax', 'ymax', 'ymin']].to_numpy()

    image_center = np.array([image_width / 2, image_height / 2])
    min_distance = float('inf')
    closest_rectangle = None

    for rect in rectangles:
        xmin, xmax, ymax, ymin = rect
        rect_center = np.array([(xmin + xmax) / 2, (ymin + ymax) / 2])
        distance = np.linalg.norm(rect_center - image_center)

        if distance < min_distance:
            min_distance = distance
            closest_rectangle = rect
    
    return closest_rectangle 

