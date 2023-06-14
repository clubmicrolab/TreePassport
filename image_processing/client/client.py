import requests
import json
import cv2

addr = 'http://localhost:5000'
test_url = addr + '/api/image'

content_type = 'image/jpeg'
headers = {'content-type': content_type} 

params = {
    'altitude': '50'
}

img = cv2.imread('2.jpg')
_, img_encoded = cv2.imencode('.jpg', img)
response = requests.post(test_url, data=img_encoded.tostring(), params = params, headers=headers)
print(json.loads(response.text))
