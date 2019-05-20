from evalMatrics import IoU, IoU_w_th
import os

## Building Data
gt_folder = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/TILE/mask/masks'
#pred_folder = '/Users/sukryool.kang/Projects/Geospatial Project/Code/unet/unet-rgb/result_small_unet_i_30_iou'
#pred_folder = '/Users/sukryool.kang/Projects/Geospatial Project/Code/unet/unet-rgb/result_small_unet_i_30_iou_2_gray'

gt_folder = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/TILE/mask/masks_255'
pred_folder = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/Unet_result/epoch_50_small_unet_large_data/results'
pred_folder = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/Unet_result/epoch_50_large_unet_large_data/results'
pred_files =  os.listdir(pred_folder)

## Road data

gt_folder = '/Users/sukryool.kang/data/GIS_data/Road/TILE_test/masks'
pred_folder = '/Users/sukryool.kang/data/GIS_data/Road/small_unet_result/results_road'
pred_files =  os.listdir(pred_folder)




gt_list = []
pred_list = []

for each_file in pred_files:
    if not each_file.endswith('tif'):
        continue

    gt_file = os.path.join(gt_folder,each_file[:-4] + '.png')

    if os.path.exists(gt_file):

        pred_list.append(os.path.join(pred_folder,each_file))
        gt_list.append(os.path.join(gt_folder,each_file[:-4] + '.png'))

#print(pred_list)
#print(gt_list)
#iou, message, status = IoU(gt_list,pred_list,255)
iou, message, status = IoU_w_th(gt_list,pred_list,255,127)
print(iou)
print(message)
