# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 13:07:26 2018

@author: Eray
"""

from matplotlib import pyplot as plt
import random


import math



import operator




def purity(groups):
    purity = 0
    num = 0
    for i in range(len(groups)):
        classes = {}
        for j in range(1, len(groups[i])):
            num += 1
            # if class not in classes, then add 
            if groups[i][j][2] not in classes:
                classes[groups[i][j][2]] = 1
            
            # else adding +1
            else:
                classes[groups[i][j][2]] += 1
        
        if len(classes) == 0:
            mx = 0
        else:
            mx  = max(classes.values()) # find value of existing maximum class
        purity += mx
    return purity/num


def update_clusters(groups):
    new_cls = []
    for i in range(len(groups)):
        nw = []
        for k in range(len(groups[1][0])):        
            summ = 0
            for j in range(len(groups[i])):    
                summ += groups[i][j][k]
            summ = summ / len(groups[i])
            nw.append(summ)
        new_cls.append(nw)
    return new_cls


def checkClusts(list_clusts, upt_clusts):
    num = 0
    for i in range(len(list_clusts)):
        for j in range(len(list_clusts[i])):
            if abs(list_clusts[i][j] - upt_clusts[i][j]) < 0.001:
                num +=1
    if num == len(list_clusts)*len(list_clusts[0]):
        return True
    else:
        return False

def find_min_max(trainingSet):
    min_data = 0
    max_data = 0
    min_max = []
    for j in range(len(trainingSet[0]) - 1):
        min_data = trainingSet[0][j]
        max_data = trainingSet[0][j]
        for i in range(len(trainingSet)):
            if min_data > trainingSet[i][j]:
                min_data = trainingSet[i][j]
            if max_data < trainingSet[i][j]:
                max_data = trainingSet[i][j]
        min_max.append([min_data, max_data])
    return min_max


def distances(instance, list_clusts):
    dist_list = []
    for x in range(len(list_clusts)):
        dist = 0
        for y in range(len(instance) - 1):
            dist += pow((instance[y] - list_clusts[x][y]), 2)
        dist =  math.sqrt(dist)
        dist_list.append([list_clusts[x], dist])
    return dist_list



def intialize_centroids(k, set_):
    
    list_clusts = [] # each iteration different centroid lists
        
    for k_ in range(k):
        initial_centroids = []  
        min_max = find_min_max(set_) # finds min max values for each attribute
        
        for j in range(len(min_max)):
            initial_centroids.append(random.uniform(min_max[j][0], min_max[j][1]))
        list_clusts.append(initial_centroids) # holds initial centroids coordinates
    return list_clusts



def plot_scatter(groups, iteration):
    lst1 = ([0.7, 1.5, 1.1, 1.3, 1.9, 0.6, 1.2], [1, 1.5, 0.9, 0.4, 1.2, 1.5, 1.9])
    lst2 = ([2.5, 3, 3.2, 2.8, 3.1, 3.9, 3], [2.3, 2.1, 2, 2.8, 2.2, 1.9, 1.7])
    lst3 = ([5, 4.5, 5.6, 5.2, 5.1, 4.9, 5.3], [4, 4.4, 5, 5.2, 6, 5, 4.3])
    plt.figure()
    plt.scatter(lst1[0], lst1[1])
    plt.scatter(lst2[0], lst2[1])
    plt.scatter(lst3[0], lst3[1])
    plt.axis([0, 7, 0, 7])
    plt.title("Iteration " + str(iteration+1))

    for i in range(len(groups)):
        plt.scatter(groups[i][0], groups[i][1], marker=r'+', color='black') 
        plt.scatter(groups[i][0], groups[i][1], marker=r'+', color='black')
        plt.scatter(groups[i][0], groups[i][1], marker=r'+', color='black')
    plt.show()


def starting_with_iteration(set_ , k, iteration_num):

    list_clusts = intialize_centroids(k, set_)
    for _ in range(iteration_num): 
        
        plot_scatter(list_clusts,_)
       # plot_scatter(list_clusts, _)
        groups = dict()
        for i in range(len(list_clusts)):
            groups.setdefault(i, []).append(list_clusts[i])
                
        for x in range(len(set_)):  
            list_clusts_and_dists = distances(set_[x], list_clusts)
            list_clusts_and_dists.sort(key=operator.itemgetter(1))
            
            for j in range(len(list_clusts)):      
                if groups[j][0] == list_clusts_and_dists[0][0]:
                    groups.setdefault(j, []).append(set_[x])
        
        upt_clusts = update_clusters(groups)
        list_clusts = upt_clusts
  
    
    return groups


def starting_with_epsilon(set_, k):
    list_clusts = intialize_centroids(k, set_)
    start= True
    iteration_num = 0
    # plot_scatter(list_clusts, _)
    while start:
        plot_scatter(list_clusts,iteration_num)
        groups = dict()
        for i in range(len(list_clusts)):
            groups.setdefault(i, []).append(list_clusts[i])
                
        for x in range(len(set_)):  
            list_clusts_and_dists = distances(set_[x], list_clusts)
            list_clusts_and_dists.sort(key=operator.itemgetter(1))
            
            for i in range(len(list_clusts)):      
                if groups[i][0] == list_clusts_and_dists[0][0]:
                    groups.setdefault(i, []).append(set_[x])
        
        upt_clusts = update_clusters(groups)
        
        if checkClusts(list_clusts, upt_clusts):
            start = False
        else:
            list_clusts = upt_clusts
            
        iteration_num += 1
    
    return groups
    

dataset = [ (0.7, 1, "Small"),
           (1.5, 1.5, "Small"),
           (1.1, 0.9, "Small"),
           (1.3, 0.4, "Small"),
           (1.9, 1.2, "Small"),
           (0.6, 1.5, "Small"),
           (1.2, 1.9, "Small"),
           (2.5, 2.3, "Medium"),
           (3, 2.1, "Medium"),
           (3.2, 2, "Medium"),
           (2.8, 2.8, "Medium"),
           (3.1, 2.2, "Medium"),
           (3.9, 1.9, "Medium"),
           (3, 1.7, "Medium"),
           (5, 4, "Large"),
           (4.5, 4.4, "Large"),
           (5.6, 5, "Large"),
           (5.2, 5.2, "Large"),
           (5.1, 6, "Large"),
           (4.9, 5, "Large"),
           (5.3, 4.3, "Large")
            ]


clusters = starting_with_epsilon(dataset, 3)
for value in clusters.values():
    for data in value:
        print(data)
    print()

purity_num = purity(clusters)
print("Purity: " + str(purity_num))














