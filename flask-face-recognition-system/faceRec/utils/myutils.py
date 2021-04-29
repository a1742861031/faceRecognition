import os, base64
import cv2
import numpy as np


def base64_2_npimage(base_str):
    index = base_str.find(',')
    image = base64.b64decode(base_str[index:])
    nparr = np.fromstring(image, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np
