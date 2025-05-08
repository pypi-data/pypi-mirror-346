import os
import sys
import time
import torch
import skimage
import sklearn.metrics
import wandb

import numpy as np
import matplotlib.pyplot as plt

import mnds
import mnmodel
import evaluation


# Hyperparameters
CURRENT_PATH = os.getcwd()
DIRECTORY = CURRENT_PATH + '/dataset_v2'
OUTPUT_DIR = "/model_output/output/"
SCALE_FACTOR = 1.0
THRESHOLD = 0.5

filelist = os.listdir(DIRECTORY + OUTPUT_DIR)
files = [file for file in filelist if file.endswith('.npy')]

for file in files:
    imid = file.split('.')[0]
    prob = np.load(DIRECTORY + OUTPUT_DIR + file)
    mn_prob = prob[0,:,:] > THRESHOLD
    mn_gt = mnds.read_micronuclei_masks(DIRECTORY, imid, SCALE_FACTOR)
    evaluation.segmentation_report(imid=imid, predictions=mn_pred, gt=mn_gt, intersection_ratio=0.1, report_obj='Micronuclei')