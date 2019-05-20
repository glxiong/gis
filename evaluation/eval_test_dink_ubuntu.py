from evalMatrics import IoU, IoU_w_th
import os

## Building Data

gt_folder = '/home/ubuntu/gis/DeepGlobe-Road-Extraction-Challenge/dataset/test_building_crop'

#pred_folder = '/Users/sukryool.kang/data/GIS_data/Building/dlink_test/log01_dink34_building'
pred_folder = '/home/ubuntu/gis/DeepGlobe-Road-Extraction-Challenge/submits/log01_dink34_building_crop'


## Road data
#gt_folder = '/Users/sukryool.kang/data/GIS_data/Road/dlink_test/test_data'

##pred_folder = '/Users/sukryool.kang/data/GIS_data/Road/dlink_test/log01_dink34'
#pred_folder = '/Users/sukryool.kang/data/GIS_data/Road/dlink_test/log01_Unet'


pred_files =  os.listdir(pred_folder)

gt_list = []
pred_list = []

for each_file in pred_files:
    if not each_file.endswith('_mask.png'):
        continue

    gt_file = os.path.join(gt_folder,each_file)

    if os.path.exists(gt_file):
        #mask
        #each_mask = os.path.join(pred_folder,each_file)
        # mmask
        each_mask = os.path.join(pred_folder,each_file[:-9]+'_mmask.png')

        pred_list.append(each_mask)
        gt_list.append(os.path.join(gt_folder,each_file))

#print(pred_list)
#print(gt_list)
#iou, message, status = IoU(gt_list,pred_list,255)
iou, message, status = IoU_w_th(gt_list,pred_list,255,127)
print(iou)
print(message)
