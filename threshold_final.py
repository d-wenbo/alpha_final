from re import T
import numpy as np
import random
import os
import sys
import glob
import csv
import pickle
import pandas as pd
import cv2
import math



def searchnum(list,min,max):
    num_sur = 0
    for n in list:
        if min <= n <= max:
            num_sur+=1
    return num_sur


args = sys.argv





debug = False



pickelefile = args[1]


threshold = 0.7


sigma_multi = 2.0
txtfile = args[2]


t = open(txtfile, 'w')


with open(pickelefile, mode='rb') as f:
    dict_cluster = pickle.load(f)
    


def func(x, a, mu, sigma):
    
    return a * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2 )) 
def get_histogram_arrays(list_val, n_bin, x_min, x_max):
    bin_heights, bin_borders = np.histogram(list_val, n_bin, (x_min, x_max))
    bin_middles = 0.5*(bin_borders[1:] + bin_borders[:-1])
    return bin_middles, bin_heights
def line_equ(x,a,b):
    y = a*x +b
    return y
#os.makedirs(picklefile_write,exist_ok = True)


if __name__ == "__main__":   
   
    
    num_detected = []
    
    
    alpha_mean = 43.85
    alpha_sigma = 14.18
    dist_max = alpha_mean + (sigma_multi * alpha_sigma)
    dist_min = alpha_mean - (sigma_multi * alpha_sigma)
    list_score_all = []
    list_dist_above = []
    j = 0
    for name in dict_cluster:
        num = 0
        err = 0
        er = 0
        list_angle_cluster_d = dict_cluster[name]["angle"]
        list_score_cluster_d = dict_cluster[name]["score"]
        list_dist_cluster_d = dict_cluster[name]["dist"]
        list_score_all.extend(list_score_cluster_d)

        for score,dist in zip(list_score_cluster_d,list_dist_cluster_d):
            if score >= threshold:
                
                num +=1
                
                
        #print(err)
        
        

        num_detected.append(num)
        if 1 <= num <= 5:
            t.write(name + '\n')
        
            
        
    qualify = searchnum(num_detected,1,5)
    

    

    print(qualify)
        
    
            
              
    
    
    

        

    
    
    
    
        
