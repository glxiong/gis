import xlrd
import os
import shutil
import cv2

input_file = 'building_road_image_files_combine_final.xlsx'
dest_img_folder = '/Users/sukryool.kang/data/GIS_data/Building/test_image'
dest_mask_folder = '/Users/sukryool.kang/data/GIS_data/Building/test_mask'
wb = xlrd.open_workbook(input_file)

sheet = wb.sheet_by_index(0)

for i in range(sheet.nrows):
    #image_file = os.path.join(sheet.cell_value(i,0), sheet.cell_value(i,2))
    #shutil.copyfile( image_file, os.path.join(dest_img_folder,sheet.cell_value(i,2)))

    mask_image = os.path.join(sheet.cell_value(i,1), sheet.cell_value(i,2))
    img = cv2.imread(mask_image,0)
    ret, img = cv2.threshold(img*255, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(os.path.join(dest_mask_folder,sheet.cell_value(i,2)),img)
