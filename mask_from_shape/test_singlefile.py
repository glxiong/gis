import os
from polygon_to_mask import convert_polygon_to_mask, convert_polygon_to_mask_w_shape, convert_polygon_to_roadmask
# import fiona
import time

#from openpyxl import Workbook

#road
# selected_folder = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/Road_Images/33 Series'
# mask_folder = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/Road_Mask'
# shape_file = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/Phase 1 Road Polygon/Phase 1 Road Polygon.shp'
# meta_file = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/road_image_files.xlsx'


input_file = "/Users/sukryool.kang/data/GIS_data/Road/Series S-28 to S-32/Images/000032_000095-RGB-7cm.tif"
shape_file = '/Users/sukryool.kang/data/GIS_data/Sample_Training_Data/Road_Shapefiles/Roads_Groundtruth_S-59 to S-69_new_coor.shp'

input_file = "/Users/sukryool.kang/data/GIS_data/Road/000068_000098-RGB-7cm.tif"
shape_file = '/Users/sukryool.kang/data/GIS_data/Road/Shapefiles/Roads_Groundtruth_S-59 to S-69_new_coor.shp'


output_file = "/Users/sukryool.kang/data/GIS_data/Road/000068_000098-RGB-7cm_mask.png"
building_check, road_check = convert_polygon_to_roadmask(input_file,shape_file,output_file )
print(road_check)
