from evalMatrics import IoU
import os

gt_folder = '/Users/sukryool.kang/data/GIS_data/LosAngeles_2017/TILE/mask/masks'
#pred_folder = '/Users/sukryool.kang/Projects/Geospatial Project/Code/unet/unet-rgb/result_small_unet_i_30_iou'
pred_folder = '/Users/sukryool.kang/Projects/Geospatial Project/Code/unet/unet-rgb/result_small_unet_i_30_iou_2_gray'
pred_files =  os.listdir(pred_folder)

gt_list = []
pred_list = []

for each_file in pred_files:
    if not each_file.endswith('tif'):
        continue

    pred_list.append(os.path.join(pred_folder,each_file))
    gt_list.append(os.path.join(gt_folder,each_file[:-4] + '.png'))

# print(pred_list)
# print(gt_list)
iou, message, status = IoU(gt_list,pred_list,1)
print(iou)
print(message)
