import os
import gdal
import numpy as np
import fiona
import sys
import cv2

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#os.environ["GDAL_DATA"] = '/Users/sukryool.kang/anaconda3/share/gdal'

building_value = 1
road_value = 2

def pointInsideImage(points,x_range,y_range):

    for each_poly in points:
        for each_pt in each_poly:
            if (x_range[0] <= each_pt[0]) and (each_pt[0] <= x_range[1]) and (y_range[0] <= each_pt[1]) and (each_pt[1] <= y_range[1]):
                return True
    return False

def convertPoint(points,gio_transform):

    top_left = [gio_transform[0],gio_transform[3]]
    pixel_size = [gio_transform[1], gio_transform[5]]

    new_points = np.asarray(points)
    new_points = (new_points-top_left)/pixel_size
    new_points = new_points + 0.5
    new_points = new_points.astype(int)

    return new_points

def polyIncludePoly(points1, points2):

    polygon1 = Polygon(points1)
    polygon2 = Polygon(points2)
    prime_idx = 0
    if polygon1.area >= polygon2.area:
        prime_idx = 0
        secondary_idx = 1
        included = True

        for each_point in points2:
            if not polygon1.contains(Point(each_point)):
                included = False
                break
    else:
        prime_idx = 1
        secondary_idx = 0
        included = True

        for each_point in points1:
            if not polygon2.contains(Point(each_point)):
                included = False
                break

    return prime_idx, secondary_idx, included


def convert_polygon_to_mask_w_shape(gis_image_file, gt_shape, output_file):

    ######################################################
    # Extract reference coordinates from gis_image_file
    ######################################################
    src_ds = gdal.Open(gis_image_file, gdal.GA_ReadOnly)
    gio_transform = src_ds.GetGeoTransform()
    cols = src_ds.RasterXSize
    rows = src_ds.RasterYSize
    bands = src_ds.RasterCount
    driver = src_ds.GetDriver().LongName

    # close dataset
    src_ds = None

    # In a north up image, padfTransform[1] is the pixel width, and padfTransform[5] is the pixel height.
    # The upper left corner of the upper left pixel is at position (padfTransform[0],padfTransform[3]).
    top_left = [gio_transform[0],gio_transform[3]]
    bottom_right = [gio_transform[0] + cols*gio_transform[1],gio_transform[3]+rows*gio_transform[5]]
    pixel_size = [gio_transform[1], gio_transform[5]]

    x_range = [top_left[0],bottom_right[0]]
    y_range = [bottom_right[1],top_left[1]]

    building_insert = []
    building_delete = []  #hole

    road_insert = []
    road_delete = []  # hole (Polygon inside Polygon)
    for idx,feat in enumerate(gt_shape):
        # To-Do: Expand the coverage including other geo-data
        if feat['geometry'] == None:
            continue
        #print(feat)
        if feat['geometry']['type'] is not 'Polygon':
            continue
        points = feat['geometry']['coordinates']  # To-Do: some feat has multiple polygon -> handle multiple polygons

        # check whether the points in the image box
        if pointInsideImage( points,x_range,y_range):
            if len(points) == 1:

                new_points = convertPoint(points,gio_transform)

                if feat['properties']['fclass'] == 'building':
                    building_insert.append(new_points)
                elif feat['properties']['fclass'] == 'road':
                    road_insert.append(new_points)

            #To-Do: Check more complex case -> Assumption: Dual polygon -> one should be inside the other polygon
            elif len(points) == 2:
                print("Dual-polygons")
                prime_idx, secondary_idx, included = polyIncludePoly(points[0],points[1])

                if feat['properties']['fclass'] == 'building':
                    if included == True:
                        building_insert.append(convertPoint(points[prime_idx],gio_transform))
                        building_delete.append(convertPoint(points[secondary_idx],gio_transform))
                    else:
                        building_insert.append(convertPoint(points[prime_idx],gio_transform))
                        building_insert.append(convertPoint(points[secondary_idx],gio_transform))

                elif feat['properties']['fclass'] == 'road':

                    if included == True:
                        road_insert.append(convertPoint(points[prime_idx],gio_transform))
                        road_delete.append(convertPoint(points[secondary_idx],gio_transform))
                    else:
                        road_insert.append(convertPoint(points[prime_idx],gio_transform))
                        road_delete.append(convertPoint(points[secondary_idx],gio_transform))
            else:
                print("Polygons more than 2, we cannot handle this case.")

                with open('polygon_more_than_2.csv','a') as fd:
                    fd.write(gis_image_file+'\n')

    road_filename = output_file
    building_filename = output_file[:-4] + "_building" + output_file[-4:]
    road_filename = output_file[:-4] + "_road" + output_file[-4:]
    # building mask
    img_building = np.zeros((rows,cols), dtype=np.uint8)
    cv2.fillPoly(img_building,building_insert,(building_value))
    cv2.fillPoly(img_building,buliding_delete,(0))
    cv2.imwrite(building_filename, img_building)
    # road mask
    img_road = np.zeros((rows,cols), dtype=np.uint8)
    cv2.fillPoly(img_road,road_insert,(road_value))
    cv2.fillPoly(img_road,road_delete,(0))
    cv2.imwrite(road_filename, img_road)
    # building and road mask
    cv2.fillPoly(img_building,road_insert,(road_value))
    cv2.fillPoly(img_building,road_delete,(0))
    cv2.imwrite(output_file,img_building)

    building_check = False
    road_check = False

    if building_insert:
        building_check = True

    if road_insert:
        road_check = True

    #print("Success: " + output_file + " was created.")

    return building_check, road_check

def convert_polygon_to_mask(gis_image_file, shape_file, output_file):

    ######################################################
    # Extract reference coordinates from gis_image_file
    ######################################################
    src_ds = gdal.Open(gis_image_file, gdal.GA_ReadOnly)
    gio_transform = src_ds.GetGeoTransform()
    cols = src_ds.RasterXSize
    rows = src_ds.RasterYSize
    bands = src_ds.RasterCount
    driver = src_ds.GetDriver().LongName

    # close dataset
    src_ds = None

    # In a north up image, padfTransform[1] is the pixel width, and padfTransform[5] is the pixel height.
    # The upper left corner of the upper left pixel is at position (padfTransform[0],padfTransform[3]).
    top_left = [gio_transform[0],gio_transform[3]]
    bottom_right = [gio_transform[0] + cols*gio_transform[1],gio_transform[3]+rows*gio_transform[5]]
    pixel_size = [gio_transform[1], gio_transform[5]]


    ##########################
    #load shape shape_file
    ##########################
    gt_shape = fiona.open(shape_file)

    x_range = [top_left[0],bottom_right[0]]
    y_range = [bottom_right[1],top_left[1]]

    building_insert = []
    building_delete = []  #hole

    road_insert = []
    road_delete = []  # hole (Polygon inside Polygon)
    for idx,feat in enumerate(gt_shape):
        # To-Do: Expand the coverage including other geo-data
        if feat['geometry'] == None:
            continue
        #print(feat)
        if feat['geometry']['type'] is not 'Polygon':
            continue
        points = feat['geometry']['coordinates']  # To-Do: some feat has multiple polygon -> handle multiple polygons

        # check whether the points in the image box
        if pointInsideImage( points,x_range,y_range):
            if len(points) == 1:

                new_points = convertPoint(points,gio_transform)

                if feat['properties']['fclass'] == 'building':
                    building_insert.append(new_points)
                elif feat['properties']['fclass'] == 'road':
                    road_insert.append(new_points)

            #To-Do: Check more complex case -> Assumption: Dual polygon -> one should be inside the other polygon
            elif len(points) == 2:
                print("Dual-polygons")
                prime_idx, secondary_idx, included = polyIncludePoly(points[0],points[1])

                if feat['properties']['fclass'] == 'building':
                    if included == True:
                        building_insert.append(convertPoint(points[prime_idx],gio_transform))
                        building_delete.append(convertPoint(points[secondary_idx],gio_transform))
                    else:
                        building_insert.append(convertPoint(points[prime_idx],gio_transform))
                        building_insert.append(convertPoint(points[secondary_idx],gio_transform))

                elif feat['properties']['fclass'] == 'road':

                    if included == True:
                        road_insert.append(convertPoint(points[prime_idx],gio_transform))
                        road_delete.append(convertPoint(points[secondary_idx],gio_transform))
                    else:
                        road_insert.append(convertPoint(points[prime_idx],gio_transform))
                        road_delete.append(convertPoint(points[secondary_idx],gio_transform))
            else:
                print("Multiple polygons > 2")

                # To-Do: Check if the following assumption is true or not.
                # Assume - index = 0 is prime....
                if feat['properties']['fclass'] == 'building':
                    building_insert.append(convertPoint(points[0],gio_transform))
                    for idx in range(1,len(points)):
                        building_delete.append(convertPoint(points[idx],gio_transform))

                elif feat['properties']['fclass'] == None or feat['properties']['fclass'] == 'secondary':
                    road_insert.append(convertPoint(points[0],gio_transform))
                    for idx in range(1,len(points)):
                        road_delete.append(convertPoint(points[idx],gio_transform))

                # elif feat['properties']['fclass'] == 'road':
                #     road_insert.append(convertPoint(points[0],gio_transform))
                #     for idx in range(1,len(points)):
                #         road_delete.append(convertPoint(points[idx],gio_transform))

                with open('polygon_more_than_2.csv','a') as fd:
                    fd.write(gis_image_file+'\n')

    road_filename = output_file
    building_filename = output_file[:-4] + "_building" + output_file[-4:]
    road_filename = output_file[:-4] + "_road" + output_file[-4:]

    img_building = np.zeros((rows, cols), dtype=np.uint8)
    # building mask
    if building_insert:
        # img_building = np.zeros((rows,cols), dtype=np.uint8)
        cv2.fillPoly(img_building,building_insert,(building_value))
        cv2.fillPoly(img_building,building_delete,(0))
        cv2.imwrite(building_filename, img_building)

    # road mask
    if road_insert:
        img_road = np.zeros((rows,cols), dtype=np.uint8)
        cv2.fillPoly(img_road,road_insert,(road_value))
        cv2.fillPoly(img_road,road_delete,(0))
        cv2.imwrite(road_filename, img_road)
    # building and road mask

    if building_insert or road_insert:
        cv2.fillPoly(img_building,road_insert,(road_value))
        cv2.fillPoly(img_building,road_delete,(0))
        cv2.imwrite(output_file,img_building)

    building_check = False
    road_check = False

    if building_insert:
        building_check = True

    if road_insert:
        road_check = True

    #print("Success: " + output_file + " was created.")

    return building_check, road_check
