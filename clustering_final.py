import numpy as np
import random
import os
import sys
import glob
import matplotlib.pyplot as plt
import csv
import pandas as pd

import pickle

from scipy.stats.stats import sigmaclip


plt.rcParams['font.size'] = 14

def func(x, a, mu, sigma,c):
    
    return a * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2 )) + c
def get_histogram_arrays(list_val, n_bin, x_min, x_max):
    bin_heights, bin_borders = np.histogram(list_val, n_bin, (x_min, x_max))
    bin_middles = 0.5*(bin_borders[1:] + bin_borders[:-1])
    return bin_middles, bin_heights



args = sys.argv

debug = False

if debug:
    filename_d = '0805_1122/alpha_angle.csv' 
    picklename =  '0805_1122/alpha_cluster.pickle'
    

else:
    filename_d = args[1]
    picklename = args[2]


df_d = pd.read_csv(filename_d,sep=',')
'''
new_dir_path = outputname
os.makedirs(new_dir_path,exist_ok = True)
new_dir_path_graph = new_dir_path + '/' + 'hist/'
os.makedirs(new_dir_path_graph,exist_ok = True)
'''
if __name__ == "__main__":

    
    dict_file_d = {}

    #print(dict_file_a)

    for j in range(df_d.shape[0]):
        img_name = df_d.loc[j][0]
        angle = df_d.loc[j][1]
        score = df_d.loc[j][2]
        dist = df_d.loc[j][5]
        if not img_name in dict_file_d:
            info = {img_name:{"angle":[],"score":[],"dist":[]}}
            dict_file_d.update(info)
        dict_file_d[img_name]["angle"].append(angle)
        dict_file_d[img_name]["score"].append(score)
        dict_file_d[img_name]["dist"].append(dist)
    #print(dict_file_d)
    
    list_angle_diff = []
    list_score_all = [] 
    list_dist_all = []

    fig = plt.figure()
    
    
    sigma =  2.8 * 3
    
    
  

    dict_file_d_clu = {}
    for name in dict_file_d:
        
        info = {}
        
        list_angle_d = dict_file_d[name]["angle"]
        list_score_d = dict_file_d[name]["score"]
        list_dist_d = dict_file_d[name]["dist"]
        i = 0 
        for angle,score,dist in zip(list_angle_d,list_score_d,list_dist_d):
            info_gene = {"angle":[],"score":[],"dist":[],"clustering":[]}  
            info_gene['angle'].append(angle)
            info_gene['score'].append(score)
            info_gene['dist'].append(dist)
            info_gene['clustering'].append('ready')
            info[i] = info_gene
            i += 1
        dict_file_d_clu[name] = info
    #print(dict_file_d_clu)
    


    dict_cluster = {}
    
    for name in dict_file_d:
        list_per_name = dict_file_d_clu[name]
        info = {'angle':[],'score':[],'dist':[]}
        for p in range(len(list_per_name)) :
            if list_per_name[p]['clustering'][0] == 'ready':
                list_per_name[p]['clustering'][0] = 'done'
                st_angle = list_per_name[p]['angle'][0] 
                st_score = list_per_name[p]['score'][0]
                st_dist = list_per_name[p]['dist'][0]
                list_calc_angle = []
                list_calc_score = []
                list_calc_dist = []
                list_calc_angle.append(st_angle)
                list_calc_score.append(st_score)
                list_calc_dist.append(st_dist)
                q = p + 1
                for q in range(len(list_per_name)):
                    ac_min = st_angle - sigma 
                    ac_max = st_angle + sigma 
                    if ac_min < -180:
                        #print(ac_min)
                        ac_min = ac_min + 360

                    if ac_max > 180:
                        #print(ac_max)
                        ac_max = ac_max -360

                    if ac_min <list_per_name[q]['angle'][0] < ac_max and list_per_name[q]['clustering'][0] == 'ready':
                        list_per_name[q]['clustering'][0] = 'done'
                        list_calc_angle.append(list_per_name[q]['angle'][0])
                        list_calc_score.append(list_per_name[q]['score'][0])
                        list_calc_dist.append(list_per_name[q]['dist'][0])
                    
                    else:
                        continue
                arr_calc_angle = np.array(list_calc_angle)
                arr_calc_score = np.array(list_calc_score)
                arr_calc_dist = np.array(list_calc_dist)
                new_score = arr_calc_score.sum()
                new_dist = np.dot(arr_calc_dist,arr_calc_score)/new_score
                new_angle = np.dot(arr_calc_angle,arr_calc_score)/new_score
                info['angle'].append(new_angle)
                info['score'].append(new_score)
                info['dist'].append(new_dist)


            else:
                continue

        dict_cluster[name] = info
    
    #print(dict_cluster)
    
    '''
    for name in dict_cluster:
        list_test = []
        list_test = dict_cluster[name]['angle']
        print(list_test)
    '''
    with open(picklename, mode='wb') as f:
        pickle.dump(dict_cluster,f)
        

    
    
    
    
    
