import cv2
import os
import numpy as np


image_folder = '/home/ubuntu/data/LA_GT_data/Images'
mask_folder =  '/home/ubuntu/data/LA_GT_data/Masks'

tile_mask_folder = '/home/ubuntu/data/LA_GT_data/TILE/masks'
tile_img_folder = '/home/ubuntu/data/LA_GT_data/TILE/images'

# 7cm data -> tile_size
tile_size = 500

def CreateTileImages(img_folder,mask_folder,img_file,tile_size,tile_img_folder,tile_mask_folder):

    status = True

    rgb_image = cv2.imread(os.path.join(img_folder,img_file))
    mask_image = cv2.imread(os.path.join(mask_folder,img_file),0)

    row,col = mask_image.shape

    idx = []
    img_files = []
    mask_files = []


    if row%tile_size != 0 or col%tile_size != 0:
        status = False
        return status, idx, img_files,mask_files

    count = 0

    for i in range(int(row/tile_size)): #y axis
        for j in range(int(col/tile_size)): # x axis
            rgb_patch  = rgb_image[tile_size*i:tile_size*(1+i), tile_size*j:tile_size*(1+j),:]
            mask_patch = mask_image[tile_size*i:tile_size*(1+i), tile_size*j:tile_size*(1+j)]

            rgb_img_file = os.path.join( tile_img_folder,img_file[:-4] + "_" +  str(count).zfill(3) + '.tif')
            mask_file = os.path.join(tile_mask_folder,img_file[:-4] + "_" +  str(count).zfill(3) + '.png')

            cv2.imwrite(rgb_img_file,rgb_patch)
            cv2.imwrite(mask_file,mask_patch)

            idx.append(count)
            img_files.append(rgb_img_file)
            mask_files.append(mask_file)
            count = count + 1

    return status, idx, img_files,mask_files

if not os.path.exists(tile_img_folder):
    os.makedirs(tile_img_folder)

if not os.path.exists(tile_mask_folder):
    os.makedirs(tile_mask_folder)


image_files = os.listdir(image_folder)
mask_files = os.listdir(mask_folder)


count = 0
for each_image in image_files:
    if each_image.endswith('.tif') and each_image in mask_files :

        status, idx, img_files,mask_files = CreateTileImages(image_folder,mask_folder,each_image,tile_size,tile_img_folder,tile_mask_folder )

        if status == False:
            print("Error - need to check", each_image)
