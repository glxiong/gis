import numpy as np
import cv2

def IoU( gt_list, pred_list, label_val ):

    ## gt_list: list of ground truth file names
    ## pred_list: list of predicted file names
    ## label_val: label value to measure IoU, ex) building value: 1, road value : 2

    iou = 0
    message = ''
    status = True

    intersection = 0
    union = 0
    if not isinstance(gt_list, str): # if gt_list is list,
        if len(gt_list) != len(pred_list):
            message = 'The number of data for ground truth and output is different. The data number should be identical.'
            status = False
            return iou, message, status


    # if gt_list is string of filename
    if isinstance(gt_list,str): # if gt_list is string

        gt_img = cv2.imread(gt_list,cv2.IMREAD_GRAYSCALE)
        out_img = cv2.imread(pred_list,cv2.IMREAD_GRAYSCALE)

        # if the image size is different
        if gt_img.shape != out_img.shape:
            message = 'Different image size between ' + gt_file + " and " + out_list[idx]
            status = False
            return iou, message, status

        gt_img_label = gt_img == label_val
        out_img_label = out_img == label_val

        intersection = intersection + np.sum(np.logical_and(gt_img_label,out_img_label))
        union = union + np.sum(np.logical_or(gt_img_label,out_img_label))

        iou = intersection / union
        message = 'IOU measured.'
        return iou, message, status

    else:  # if gt_list is list
        if isinstance(gt_list[0],str): # if gt_list[0] -> string
            for idx, gt_file in enumerate(gt_list):

                gt_img = cv2.imread(gt_file,cv2.IMREAD_GRAYSCALE)
                out_img = cv2.imread(pred_list[idx],cv2.IMREAD_GRAYSCALE)

                # if the image size is different
                if gt_img.shape != out_img.shape:
                    message = 'Different image size between ' + gt_file + " and " + out_list[idx]
                    status = False
                    return iou, message, status

                gt_img_label = gt_img == label_val
                out_img_label = out_img == label_val

                intersection = intersection + np.sum(np.logical_and(gt_img_label,out_img_label))
                union = union + np.sum(np.logical_or(gt_img_label,out_img_label))

            iou = intersection / union
            message = 'IOU measured.'
            return iou, message, status

        else:
            # assump if the data npy
            gt_flatten = gt_list.flatten()
            pred_flatten = pred_list.flatten()

            gt_flatten_label = gt_flatten == label_val
            pred_flatten_label = pred_flatten == label_val

            iuo = np.sum(np.logical_and(gt_flatten_label,pred_flatten_label))/np.sum(np.logical_or(gt_flatten_label,pred_flatten_label))
            message = 'IOU measured.'
            return iou, message, status

def IoU_w_th( gt_list, pred_list, label_val, th_val):

    ## gt_list: list of ground truth file names
    ## pred_list: list of predicted file names
    ## label_val: label value to measure IoU, ex) building value: 1, road value : 2

    iou = 0
    message = ''
    status = True

    intersection = 0
    union = 0
    if not isinstance(gt_list, str): # if gt_list is list,
        if len(gt_list) != len(pred_list):
            message = 'The number of data for ground truth and output is different. The data number should be identical.'
            status = False
            return iou, message, status


    # if gt_list is string of filename
    if isinstance(gt_list,str): # if gt_list is string

        gt_img = cv2.imread(gt_list,cv2.IMREAD_GRAYSCALE)
        out_img = cv2.imread(pred_list,cv2.IMREAD_GRAYSCALE)
        binary, out_img = cv2.threshold(out_img, th_val, 255, cv2.THRESH_BINARY)

        # if the image size is different
        if gt_img.shape != out_img.shape:
            message = 'Different image size between ' + gt_file + " and " + out_list[idx]
            status = False
            return iou, message, status

        gt_img_label = gt_img == label_val
        out_img_label = out_img == label_val

        intersection = intersection + np.sum(np.logical_and(gt_img_label,out_img_label))
        union = union + np.sum(np.logical_or(gt_img_label,out_img_label))

        iou = intersection / union
        message = 'IOU measured.'
        return iou, message, status

    else:  # if gt_list is list
        if isinstance(gt_list[0],str): # if gt_list[0] -> string
            for idx, gt_file in enumerate(gt_list):

                gt_img = cv2.imread(gt_file,cv2.IMREAD_GRAYSCALE)
                out_img = cv2.imread(pred_list[idx],cv2.IMREAD_GRAYSCALE)
                binary, out_img = cv2.threshold(out_img, th_val, 255, cv2.THRESH_BINARY)

                # if the image size is different
                if gt_img.shape != out_img.shape:
                    message = 'Different image size between ' + gt_file + " and " + out_list[idx]
                    status = False
                    return iou, message, status

                gt_img_label = gt_img == label_val
                out_img_label = out_img == label_val

                intersection = intersection + np.sum(np.logical_and(gt_img_label,out_img_label))
                union = union + np.sum(np.logical_or(gt_img_label,out_img_label))

            iou = intersection / union
            message = 'IOU measured.'
            return iou, message, status

        else:
            # assump if the data npy
            gt_flatten = gt_list.flatten()
            pred_flatten = pred_list.flatten()

            gt_flatten_label = gt_flatten == label_val
            pred_flatten_label = pred_flatten == label_val

            iuo = np.sum(np.logical_and(gt_flatten_label,pred_flatten_label))/np.sum(np.logical_or(gt_flatten_label,pred_flatten_label))
            message = 'IOU measured.'
            return iou, message, status
