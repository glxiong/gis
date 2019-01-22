from polygon_to_mask import convert_polygon_to_mask

file = '/Users/sukryool.kang/Projects/Geospatial Project/Data_For AI Team/Vecel_Data_Jan_4_2019/Graz/000007_000008-RGB-7cm.tif'
shape_file = '/Users/sukryool.kang/Projects/Geospatial Project/Data_For AI Team/Vecel_Data_Jan_4_2019/Groundtruth data/Graz/Graz_Building_ground truth.shp'

output_file = 'output_test.tif'

print(convert_polygon_to_mask(file,shape_file,output_file))
