import pickle
import numpy as np
import fiona
import cv2
import rasterio

from shapely.geometry import mapping, Polygon
from matplotlib import pyplot as plt
from rdp import rdp


def Polygon_from_mask(mask):
    
    output_image = np.zeros([mask.shape[0],mask.shape[1],3],dtype=np.uint8)
    mask = mask.astype(np.uint8)
    im2,contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    output_image = cv2.drawContours(output_image, contour, -1, (0,255,0), 3)
    gray_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY)
    
    #lines = rdp(contour,epsilon=100)
    
    for each_contour in contours:
        points = rdp(each_contour,epsilon=1.5, algo="iter")
    
        cv2.polylines(output_image,lines,True,(255,0,0),1)
        plt.figure(figsize=(20,20))
        plt.imshow(output_image)
        
        break
    
    plt.figure(figsize=(20,20))
    
    plt.imshow(output_image)
    
