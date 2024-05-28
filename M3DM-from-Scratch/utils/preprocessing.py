'''
Author: wangwei83 wangwei83@cuit.edu.cn
Date: 2024-05-28 10:48:48
LastEditors: wangwei83 wangwei83@cuit.edu.cn
LastEditTime: 2024-05-28 23:12:57
FilePath: /wangwei/X-23d-Y-ai-Z-detection/M3DM-from-Scratch/utils/preprocessing.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import argparse
import os
from pathlib import Path
from PIL import Image
import numpy as np
import mvtec3d_util as mvt_util

def remove_plane(organized_pc_clean, organized_rgb,distance_threshold=0.005):
    # Remove the plane
    
    unorganized_pc  = mvt_util.organized_pc_to_unorganized_pc(organized_pc_clean)
    
    
    planeless_organized_pc = organized_pc_clean
    planeless_organized_rgb = organized_rgb
    return planeless_organized_pc, planeless_organized_rgb

def preprocess_pc(tiff_path):
    organized_pc = mvt_util.read_tiff_organized_pc(tiff_path)
    rgb_path = str(tiff_path).replace("xyz", "rgb").replace("tiff", "png")
    # print(rgb_path)
    gt_path = str(tiff_path).replace("xyz", "gt").replace("tiff", "png")
    # print(gt_path)
    organized_rgb = np.array(Image.open(rgb_path))
    organized_gt=None
    gt_exists = os.path.isfile(gt_path)
    if gt_exists:
        organized_gt = np.array(Image.open(gt_path))
        # print(organized_gt)
    
    planeless_organized_pc, planeless_organized_rgb = remove_plane(organized_pc, organized_rgb)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_path', type=str, help='path to the dataset')
    args=parser.parse_args()
    root_path = args.dataset_path
    paths=Path(root_path).rglob('*.tiff')
    print(f"Found {len(list(paths))} tiff files in {root_path}")
    
    for path in Path(root_path).rglob('*.tiff'):
        preprocess_pc(path)