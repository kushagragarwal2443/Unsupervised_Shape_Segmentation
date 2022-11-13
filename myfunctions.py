import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import time

def get_corrected_dict(dicti):
    '''On dumping a dictionary as JSON object, all the integer key values are converted to strings.
    This function reverses that change'''
    new_dict = dict()
    for key in dicti:
        new_dict[int(key)] = dicti[key]
    return new_dict

def get_root(node, tree):
    while(True):
        if(len(tree[node]["parent"])==0):
            return node
        node = tree[node]["parent"][0]

def get_roots(tree):
    roots = []
    for key in tree:
        if(len(tree[key]["parent"])==0):
            roots.append(key)
    return roots

def get_leaves(tree):
    leafs = []
    for key in tree:
        if(len(tree[key]["child"])==0):
            leafs.append(key)
    return leafs

def get_paths(tree):
    paths = []
    leafs = get_leaves(tree)
    for node in leafs:
        node_path = [node]
        cur_node = node
        while(True):
            if(len(tree[cur_node]["parent"])!=0):
                node_path.append(tree[cur_node]["parent"][0])
                cur_node = tree[cur_node]["parent"][0]
                continue
            else:
                break
        paths.append(node_path[::-1])
    return paths
        
def get_subnodes(paths):
    subnodes = dict()
    for i in paths:
        for j in i:
            subnodes[j] = set()     
    # now going up and adding elements along with their subnodes
    for i in paths:
        for j in range(len(i)-2, -1, -1):
            subnodes[i[j]].add(i[j+1])
            for element in list(subnodes[i[j+1]]):
                subnodes[i[j]].add(element)                   
    return subnodes  

def get_possible_subchildren(node, subchildren, tree):
    children = tree[node]["child"]
    if(len(children) == 0):
        subchildren[node] = []
        return
    if(children[0] not in subchildren):
        get_possible_subchildren(children[0], subchildren, tree)
    possible_children = list(subchildren[children[0]])
    possible_children.append([children[0]])
    for i in range(1, len(children)):
        if(children[i] not in subchildren):
            get_possible_subchildren(children[i], subchildren, tree)
        subchild = list(subchildren[children[i]])
        subchild.append([children[i]])
        new_possible_children = []
        for x in possible_children:
            for y in subchild:
                z = x + y
                new_possible_children.append(z)
        possible_children = []
        possible_children = new_possible_children
    subchildren[node] = possible_children
    return subchildren   

def get_complete_children_sets(tree):
    subchildren = dict()
    # storing root nodes
    roots = []
    for key in tree:
        if(len(tree[key]["parent"])==0):
            roots.append(key)
    for key in roots:
        if(len(tree[key]["child"])==0 and len(tree[key]["parent"])==0):
            subchildren[key] = []
        else:
            subchildren = get_possible_subchildren(key, subchildren, tree)
    return subchildren

def get_subchildren_roots(subchildren, roots):
    
    subroots = []
    for root in roots:
        subchild = subchildren[root]
        subroot = [root]
        for element in subchild:
            subroot.extend(element)
        subroots.append(list(set(subroot)))

    return subroots

def is_valid_subset(subset, paths):
    subset = list(subset)
    if(len(subset)<1):
        return 0
    flag = 0
    for path in paths:
        fpath = 0
        for index in path:
            if(index in subset):
                fpath+=1    
        if(fpath > 1):
            flag = 1  
    return abs(1-flag)

def is_correct_subset(subset, paths):
    subset = list(subset)
    if(len(subset)<1):
        return 0
    flag = 0
    for path in paths:
        for index in path:
            if(index in subset):
                flag +=1     
    if(flag == len(paths)):
        return 1
    else:
        return 0
    
def check_validity_correctness(cluster, tree):
    paths = get_paths(tree)
    if(is_correct_subset(cluster, paths) == 1 and is_valid_subset(cluster, paths) == 1):
        print("OK!!")
    else:
        print("ERROR!!")

def get_diff_bw_clusters(a,b):
    for node in a:
        if(node not in b):
            print(node, "Only in First")
    for node in b:
        if(node not in a):
            print(node, "Only in Second")
            
def get_sqdist(vec1, vec2):
    
    length = len(vec1)
    assert(len(vec2)==length)
    sum_sq = 0
    for i in range(length):
        sum_sq += (vec1[i]-vec2[i])**2
    return sum_sq

def get_fitness(population, dist):
    pop_size = len(population)
    fitness_vec = []
    for pop in range(pop_size):
        a = list(population[pop])
        length = len(a)
        total_distance = 0
        for i in range(length):
            for j in range(i+1, length):
                total_distance += dist[a[i]][a[j]]
        total_pairs = length*((length-1)/2.0)
        fitness_vec.append(total_pairs/total_distance) ## inverse of avg distance
    return fitness_vec

def get_fitness_nearestNeighbour(population, dist):
    pop_size = len(population)
    fitness_vec = []
    for pop in range(pop_size):
        a = list(population[pop])
        length = len(a)
        total_distance = 0
        for i in range(length):
#             print("\nNEW ELEMENT")
            cur_closest_distance = 100000000
            for j in range(length):
                if(i!=j):
                    cur_distance = dist[a[i]][a[j]]
#                     print(cur_distance)
                    if(cur_distance < cur_closest_distance):
                        cur_closest_distance = cur_distance
#                         print("Closest distance updated to", cur_closest_distance)
#             print("FINAL CLOSEST DISTANCE FOR THE NEW ELEMENT", cur_closest_distance)
            total_distance += cur_closest_distance
#             print("NEW TOTAL DISTANCE", total_distance)
#         print("\nFINAL TOTAL DISTANCE", total_distance)
#         print("LENGTH", length)
#         print(length/total_distance)
        fitness_vec.append(length/total_distance) ## inverse of avg nearest neighbour distance
    return fitness_vec

def get_fitness_KnearestNeighbour(population, dist, knn):
    pop_size = len(population)
    fitness_vec = []
    for pop in range(pop_size):
        a = list(population[pop])
        length = len(a)
        if(knn > (length-1) or knn<1):
            print("Choose an appropriate K-NN value -> [1, number of roots - 1]")
            return -1
        total_distance = 0
        for i in range(length):
            cur_distance = []
            for j in range(length):
                if(i!=j):
                    cur_distance.append(dist[a[i]][a[j]])
#             print("\nNEW ELEMENT")
#             print(cur_distance)
#             print("SORTING....")
            cur_distance = np.sort(np.array(cur_distance))
#             print(cur_distance)
            cur_closest_distance = np.sum(cur_distance[:knn])/knn
#             print("AVERAGE CLOSEST DISTANCE", cur_closest_distance)
            total_distance += cur_closest_distance
#             print("TOTAL DISTANCE TILL NOW", total_distance)
#         print("LENGTH", length)
#         print(length/total_distance)
        fitness_vec.append(length/total_distance) ## inverse of avg nearest neighbour distance
    return fitness_vec