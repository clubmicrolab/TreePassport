
from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2  
import threading 
from process_img import predict_factory_method


app = Flask(__name__)


@app.route('/api/image', methods=['POST'])
def image():
    r = request 
    altitude = r.args.get('altitude') 
    nparr = np.fromstring(r.data, np.uint8)
    imageBGR  = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  
    imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)

    thread = threading.Thread(target=predict_factory_method,args=(imageRGB, int(altitude)))
    thread.start()

    response = {'message': 'succesfully recieved'}
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")