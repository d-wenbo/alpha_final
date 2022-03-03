from re import S
import numpy as np
import cv2
import random
import os
import sys
import glob
import math
import csv
import pandas as pd
import pickle

def search_list(list,num):
    n = 0
    for i in list:
        if i >= num:
            n += 1
        else:
            continue
    return n

def distance(x,y,x_base,y_base):
    dx = x - x_base
    dy = y - y_base
    dist = np.hypot(dx,dy)

    return dist

def search_min(a,b,c,d):
    list_dist = []
    list_dist.append(a)
    list_dist.append(b)
    list_dist.append(c)
    list_dist.append(d)
    min_value = min(list_dist)

    return min_value

def func(x, a, mu, sigma):
    
    return a * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2 )) 

def get_histogram_arrays(list_val, n_bin, x_min, x_max):
    bin_heights, bin_borders = np.histogram(list_val, n_bin, (x_min, x_max))
    bin_middles = 0.5*(bin_borders[1:] + bin_borders[:-1])
    return bin_middles, bin_heights

args = sys.argv


debug = False
if debug:
    filename = '0805_1116/0826_all_0805real_alpha.csv' 
    output_file = '0805_1116/alpha_angle_dist.csv' 
    
    #label1_score_pickle = '0805_1116/alpha_label1_score.pickle'
else:
    filename = args[1]
    output_file = args[2]
    
    #label1_score_pickle = args[4]

df_m = pd.read_csv(filename,sep=',')

f = open(output_file, 'w')
writer = csv.writer(f, lineterminator='\n')
writer.writerow(['img_name','angle','score','x_label1','y_label1','distance'])



list_num_point_rm = []


if __name__ == "__main__":


    dict_filename_number = {}
    dict_for_label1 = {}
    list_imgname_t = []
    for j in range(df_m.shape[0]):
        label = int(df_m.loc[j][0])
        score = float(df_m.loc[j][1])
        x_left = int(df_m.loc[j][2])
        y_left = int(df_m.loc[j][3])
        x_right = int(df_m.loc[j][4])
        y_right = int(df_m.loc[j][5])
        img_name_df = df_m.loc[j][6]
        
        if not img_name_df in list_imgname_t:
            list_imgname_t.append(img_name_df)
        
        this_info = {
                    "label": label,
                    "score": score,
                    "x_left": x_left,
                    "y_left": y_left,
                    "x_right": x_right,
                    "y_right": y_right,
                    "x": int((x_left + x_right)/2),
                    "y": int((y_left + y_right)/2),
                    "flag_ghost": False,
                    "img_name_df": img_name_df
                    }

        if label ==1:
            if not img_name_df in dict_for_label1:
                filename_number = {img_name_df: {"count":0, "info":[]}}
                dict_for_label1.update(filename_number)
            
            dict_for_label1[img_name_df]["count"] += 1
            dict_for_label1[img_name_df]["info"].append(this_info)

        else:
            #increse img_name                                                   
            if not img_name_df in dict_filename_number:
                filename_number = {img_name_df: {"count":0, "info":[]}}
                dict_filename_number.update(filename_number)
            
            # increse infomation                                                
            dict_filename_number[img_name_df]["count"] += 1
            dict_filename_number[img_name_df]["info"].append(this_info)

    
    # ghost reduction                                                           
    list_distance = []
    list_distance_nearest = []
    
    mean_x = 0.61 
    sigma_x = 4.09

    mean_y = 0.36
    sigma_y = 4.55
    
    dist_max_x = mean_x + 3*sigma_x
    dist_max_y = mean_y + 3*sigma_y
    # drawing                                                                   
    list_num_point = []
    list_score_label1_max = []
    list_test = []
    
    list_imgname = []
    for i in range(len(list_imgname_t)):
        
        img_name = list_imgname_t[i]
        list_x = []
        list_y = []
        list_score = []
        list_x_label1 =[]
        list_y_label1 =[]
        list_score_label1 = []
        list_angle = []
        list_score_angle = []
        
        if not img_name in dict_filename_number:
            continue
        list_info =  dict_filename_number[img_name]["info"]
        for info in list_info:
            x = info["x"]
            y = info["y"]
            score = info["score"]
            list_x.append(x)
            list_y.append(y)
            list_score.append(score)
            
            
        list_score.reverse()
        list_x.reverse()
        list_y.reverse()


        if img_name in dict_for_label1:
            

            list_info_label1 = dict_for_label1[img_name]["info"]
            #print(list_info_label1)
            for info_1 in list_info_label1:
                x = info_1["x"]
                y = info_1["y"]
                score = info_1["score"]
                list_x_label1.append(x)
                list_y_label1.append(y)
                list_score_label1.append(score)

                         
            if max(list_score_label1) > 0.2:
                list_test.append(img_name) 
                
                list_x_label1_base = []
                list_y_label1_base = []
                list_score_label1_base = []
                index = list_score_label1.index(max(list_score_label1))
                x_label1_base = list_x_label1[index]
                y_label1_base = list_y_label1[index]
                score_label1_base = list_score_label1[index]
                list_x_label1_base.append(x_label1_base)
                list_y_label1_base.append(y_label1_base)
                list_score_label1_base.append(score_label1_base)
                list_score_label1_max.append(max(list_score_label1))
            
                
                for info in list_info:
                    x = info["x"]
                    y = info["y"]
                    score = info["score"]
                    x_left = info["x_left"]
                    y_left = info["y_left"]
                    x_right = info["x_right"]
                    y_right = info["y_right"]
                    dist_tl = distance(x_left,y_left,x_label1_base,y_label1_base)
                    dist_br = distance(x_right,y_right,x_label1_base,y_label1_base)
                    dist_tr = distance(x_right,y_left,x_label1_base,y_label1_base)
                    dist_bl = distance(x_left,y_right,x_label1_base,y_label1_base)
                    dist_nearest = search_min(dist_tl,dist_br,dist_tr,dist_bl)
                    list_distance_nearest.append(dist_nearest)
                    if dist_nearest == dist_tl:
                        
                        x_near = x_left
                        y_near = y_left
                    if dist_nearest == dist_tr:
                        x_near = x_right
                        y_near = y_left
                    if dist_nearest == dist_br:
                        x_near = x_right
                        y_near = y_right
                    if dist_nearest == dist_bl:
                        x_near = x_left
                        y_near = y_right
                    
                    x_gap = x_near - x_label1_base
                    y_gap = y_near - y_label1_base

                    if abs(x_gap) < dist_max_x and abs(y_gap) < dist_max_y:
                        
                        calc_x = x - x_label1_base
                        calc_y = y - y_label1_base
                        angle =  math.degrees(math.atan2(calc_y,calc_x))
                        dist = distance(x,y,x_label1_base,y_label1_base)
                        
                        writer.writerow([img_name,angle,score,x_label1_base,y_label1_base,dist])
                        list_angle.append(angle)
                        list_score_angle.append(score)
                        if not img_name in list_imgname:
                            list_imgname.append(img_name)
    
    '''
    with open(label1_score_pickle, mode='wb') as f:
        pickle.dump(list_score_label1_max,f)    
    '''     