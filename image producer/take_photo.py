import cv2

def change_brightness(input_img, brightness = 0):
    ''' input_image:  color or grayscale image
        brightness:  -127 (all black) to +127 (all white)

            returns image of same type as input_image but with
            brightness adjusted

    '''
    img = input_img.copy()
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        cv2.convertScaleAbs(input_img, img, alpha_b, gamma_b)

    return img

cam = cv2.VideoCapture(0)

ret, image = cam.read()

cv2.imwrite('/home/drones/testimage.jpg', change_brightness(image, -50))
cam.release()
cv2.destroyAllWindows()