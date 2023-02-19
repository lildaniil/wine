from aiogram import types
from utils.misc.functions import random_name
import os
import cv2
from pyzbar.pyzbar import decode


def set_path():
    name = random_name(pas='temp_')
    path = 'data/pics' +'/'+ str(name)+'.jpg'

    return path

# DeprecationWarning

def get_code(path:str):
    
    try:
        img = cv2.imread(path)
        code = decode(img)
        print(code)
        print((code[0][0]).decode("utf-8"))
        print(code[0][1])

        barcode = (code[0][0]).decode("utf-8")
        type = (code[0][1])

        try:
            os.remove(path)
        except:
            pass

        return type, barcode

    except: 
        print("йук капут")
        try:
            os.remove(path)
        except:
            pass
        
        return None
        
    
    
    

