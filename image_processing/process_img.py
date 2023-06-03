from model_singleton import ModelSingleton  
from crown_math import calculate_crown_size 
import cv2 
from deepforest import preprocess
import os

def predict_factory_method(image,altitude):
    if altitude > 100:
        predict_crowns_segemented(image,altitude)
    else:
        predict_crowns(image,altitude)


def predict_crowns(image,altitude): 
    pred_boxes = ModelSingleton.getInstance().predict_image(image=image[:,:,:3]) 
    process_save_img(pred_boxes, image,altitude)


def predict_crowns_segemented(image,altitude):
    #Create windows of 400px
    windows = preprocess.compute_windows(image, patch_size=400,patch_overlap=0)
    print(f'We have {len(windows)} windows in the image') 
    tile = ModelSingleton.getInstance().predict_tile(image=image,return_plot=False,patch_overlap=0,iou_threshold=0.05,patch_size=400) 
    process_save_img(tile, image,altitude)


def process_save_img(pred_boxes,image,altitude): 
    img = image.copy() 

    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0, 255, 0) 
    thickness = 2

    for index, row in pred_boxes.iterrows():
        cv2.rectangle(img, (int(row["xmin"]), int(row["ymin"])), (int(row["xmax"]), int(row["ymax"])), (0, 0, 0), thickness=10, lineType=cv2.LINE_AA)  
        x_lat =  int(row["xmax"]) - int(row["xmin"])
        y_lat = int(row["ymax"]) - int(row["ymin"])
        x_center =  int(x_lat/2) + int(row["xmin"])
        y_center =  int(y_lat/2) + int(row["ymin"]) 
        
        lat =  int(x_lat/2) if int(x_lat/2) >  int(y_lat/2) else  int(y_lat/2)   

        
        cv2.putText(img, str(calculate_crown_size(img,lat,altitude) ),  (x_center, y_center) , font, 0.5, 
                    color, thickness, cv2.LINE_AA, False)

    
    current_location = os.getcwd() 
    directory = f'{current_location}/images_recieved' # Replace with the actual directory path
    IMG_COUNTER = len(os.listdir(directory))
    cv2.imwrite(f'{directory}/kek{IMG_COUNTER+1}.png', cv2.cvtColor(img  , cv2.COLOR_BGR2RGB))


