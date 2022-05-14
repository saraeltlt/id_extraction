
from pytesseract import *
import cv2

from unidecode import unidecode

import numpy as np

def extract_ara_num(img1):
    img = resize_ara_num(img1)
    h,w,ch=img.shape
    img = img[int(h/1.8):int(h/1.08), int(w/2.8):int(w/1)]
    copy=img
    #------------------
    count = 0
    while (True):
        count = count + 1
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th, img = cv2.threshold(img, 100, 255, cv2.THRESH_TRUNC)
        res = pytesseract.image_to_string(img, lang="ara_t12").split()
        #print(res)
        if res != []:
            for i in res:
                if len(i) == 14:
                    return i
        f_res=""
        for i in range(1,len(res)+1):
            if i >1:
                temp=res[len(res) - i]
                temp+=f_res
                f_res = temp
            else:
                f_res+= res[len(res) - i]

            if len(f_res)==14:
                return f_res

        img = increase_contrast(copy)
        if count > 1:
            img = increase_contrast(img)
        if count == 3:
           img = np.rot90(img1)
           img = resize_ara_num(img)
           h, w, ch = img.shape
           img = img[int(h / 1.8):int(h / 1.08), int(w / 2.8):int(w / 1)]
        if count == 4:
            return "please re-capture the image"
        continue
 ################################################################

def increase_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))     # Applying CLAHE to L-channel
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)  # Converting image from LAB Color model to RGB model
    return final
 ################################################################

def resize_ara_num(img):
    width = 712
    height = 512
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img


################################################################


img=cv2.imread("data_set/1.jpg")
ara_num_res=extract_ara_num(img)
print("Extracted number= %s" %ara_num_res)
number = unidecode(ara_num_res)
print("     Translation= %s" %number)

cv2.waitKey(0)
