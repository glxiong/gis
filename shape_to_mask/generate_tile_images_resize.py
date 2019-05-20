import cv2
from openpyxl import Workbook, load_workbook
import os
import csv
from sklearn.externals import joblib
import numpy as np
from scipy import ndimage as ndi
from scipy.ndimage.morphology import distance_transform_edt

meta_file = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/building_road_image_files_combine_final.xlsx'

tile_mask_folder = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/TILE_300/mask'
tile_img_folder = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/TILE_300/train/images'
new_meta_file = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/TILE_300/stage_metadata_new_resize.csv'

# 7cm data -> tile_size
tile_size = 500
image_size = 300

def label(mask):
    labeled, nr_true = ndi.label(mask)
    return labeled

def is_on_border(mask, border_width):
    return not np.any(mask[border_width:-border_width, border_width:-border_width])

def update_distances(dist, mask):
    if dist.sum() == 0:
        distances = distance_transform_edt(1 - mask)
    else:
        distances = np.dstack([dist, distance_transform_edt(1 - mask)])
    return distances

def get_size_matrix(mask):
    sizes = np.ones_like(mask)
    labeled = label(mask)
    for label_nr in range(1, labeled.max() + 1):
        label_size = (labeled == label_nr).sum()
        sizes = np.where(labeled == label_nr, label_size, sizes)
    return sizes

def get_distance_matrix(mask):

    distances = np.zeros_like(mask)
    labeled = label(mask)

    for label_nr in range(1,labeled.max()+1):
        each_mask = np.zeros_like(mask)
        each_mask = np.where(labeled == label_nr,1,each_mask)

        if is_on_border(each_mask,2):
            continue

        distances = update_distances(distances,each_mask)

    return distances


def clean_distances(distances):
    if len(distances.shape) < 3:
        distances = np.dstack([distances, distances])
    else:
        distances.sort(axis=2)
        distances = distances[:, :, :2]
    second_nearest_distances = distances[:, :, 1]
    distances_clean = np.sum(distances, axis=2)
    return distances_clean.astype(np.float16), second_nearest_distances


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

            # resize image
            rgb_patch = cv2.resize(rgb_patch, (image_size, image_size))
            mask_patch = cv2.resize(mask_patch, (image_size, image_size))

            rgb_img_file = os.path.join( tile_img_folder,img_file[:-4] + "_" +  str(count).zfill(3) + '.tif')
            mask_file = os.path.join( tile_mask_folder+'/masks',img_file[:-4] + "_" +  str(count).zfill(3) + '.png')
            size_file = os.path.join( tile_mask_folder+'/sizes',img_file[:-4] + "_" +  str(count).zfill(3) )
            distance_file = os.path.join( tile_mask_folder+'/distances',img_file[:-4] + "_" +  str(count).zfill(3) )



            cv2.imwrite(rgb_img_file,rgb_patch)
            cv2.imwrite(mask_file,mask_patch)

            # sizes
            sizes = get_size_matrix(mask_patch)
            joblib.dump(sizes, size_file)

            # distances

            distances = get_distance_matrix(mask_patch)
            distances, second_nearest_distances = clean_distances(distances)
            joblib.dump(distances, distance_file)

            idx.append(count)
            img_files.append(rgb_img_file)
            mask_files.append(mask_file)
            count = count + 1

    return status, idx, img_files,mask_files


def write_csv(new_meta_file, idx, img_files,mask_files,int_c):

    with open(new_meta_file,'a') as f:
        writer = csv.writer(f)
        for i in range(len(idx)):
            writer.writerows([[str(int_c+i),img_files[i],mask_files[i],str(0),str(1),str(0)]])


    return int_c + len(idx)





if not os.path.exists(tile_img_folder):
    os.makedirs(tile_img_folder)

if not os.path.exists(tile_mask_folder):
    os.makedirs(tile_mask_folder)
    os.makedirs(os.path.join(tile_mask_folder,'masks'))
    os.makedirs(os.path.join(tile_mask_folder,'distances'))
    os.makedirs(os.path.join(tile_mask_folder,'sizes'))


meta_data = load_workbook(filename = meta_file, data_only=True, read_only=True)

building_sheet = meta_data.get_sheet_by_name('Building')

with open(new_meta_file,'a') as f:
    writer = csv.writer(f)
    writer.writerows([['ImageId','file_path_image','file_path_mask_eroded_0_dilated_0','is_test','is_train','is_valid','n_buildings'] ])


count = 0
for each_row in building_sheet:
    if each_row[3].value == 'o':
#         img_file  = [each_row[0].value,each_row[2].value]
#         mask_file = [each_row[1].value,each_row[2].value] # building = 1, road = 2
        status, idx, img_files,mask_files = CreateTileImages(each_row[0].value,each_row[1].value,each_row[2].value,tile_size,tile_img_folder,tile_mask_folder )

        if status == True:
            count = write_csv(new_meta_file, idx, img_files,mask_files,count)
        else:
            print("Error - need to check")
