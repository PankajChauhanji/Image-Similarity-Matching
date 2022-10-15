# This file contains code for calculating similarity between two images.
# This code calculate difference in two images in terms of distance.
# Example posting a local image file:

import requests
import  time
import imagehash
from PIL import Image
from collections import Counter
import numpy as np

def generate_distance_api(letters):
    done = []
    scores = []
    for char1 in letters:
        for char2 in letters:
            if char1 == char2:
                continue
            else:
                if char1+char2 in done or char2+char1 in done:
                    continue
                else:
                    done.append(char1+char2)
                    done.append(char2+char1)
                    path1 = "images/image_" + char1 + "_.png"
                    path2 = "images/image_" + char2 + "_.png"
                    
                    time.sleep(2)
                    resp = get_score_distance(path1, path2)
                    
                    print("Response for: ", char1, " && ", char2, " : ", resp.json())
                    
                    scores.append({char1+char2 : resp.json()})
    
    print("resp: ", scores)
    

# Using Histogram.
def get_hist_image(path):
    im1 = Image.open(path)
    array1 = np.array(im1)
    flat_array_1 = array1.flatten()
    RH1 = Counter(flat_array_1)
    
    H1 = []
    for i in range(256):
        if i in RH1.keys():
            H1.append(RH1[i])
        else:
            H1.append(0)
    
    return H1

def L2Norm(H1,H2):
    distance =0
    for i in range(len(H1)):
        distance += np.square(H1[i]-H2[i])
    return np.sqrt(distance)

def distance_eucledian(letters):
    # We are calculating image differences using Histogram and Eucledian Distance.
    
    done = []
    scores = {}
    max = 0
    
    for char1 in letters:
        temp = {}
        for char2 in letters:
            if char1 == char2 or char1+char2 in done or char2+char1 in done:
                continue
            else:
                path1 = "images/image_" + char1 + "_.png"
                path2 = "images/image_" + char2 + "_.png"
                H1 = get_hist_image(path1)
                H2 = get_hist_image(path2)
                dist = round(L2Norm(H1, H2)/10000, 2)
                
                temp[char2] = dist
                if dist>max:
                    max = dist
                done.append(char1+char2)
        scores[char1] = temp
    return scores, max
   

# Image Hashing.

def image_hash(letters):
    done = []
    scores = {}
    max = 1
    
    for char1 in letters:
        temp = {}
        for char2 in letters:
            if char1 == char2 or char1+char2 in done or char2+char1 in done:
                continue
            else:
                path1 = "images/image_" + char1 + "_.png"
                path2 = "images/image_" + char2 + "_.png"
                
                ahash1 = imagehash.average_hash(Image.open(path1))
                ahash2 = imagehash.average_hash(Image.open(path2))

                # We can also use phash and whash.
                # But as per out test, ahash works better.

                # phash1 = imagehash.phash(Image.open(path1))
                # phash2 = imagehash.phash(Image.open(path2))
                # whash1 = imagehash.whash(Image.open(path1))
                # whash2 = imagehash.whash(Image.open(path2))
                
                # resp = round(1 - (ahash1 - ahash2)/38, 2)
                resp = ahash1-ahash2
                
                temp[char2] = resp
                done.append(char1+char2)
                
                if max<resp:
                    max = resp
        scores[char1] = temp
                    
    return scores, max
    
if __name__ == '__main__':
    print("start: ")
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz!@#$%&(){[}]|?><"
    dict = {}

    # Using paid API.
    # generate_distance_api()
    
    # Using Image hashing.
    score1, max1 = image_hash(letters)
    print(max1, "\n", score1)

    # Using Eucledian distance.
    # score2, max2 = distance_eucledian(letters)
    # print(max1, max2)

    # Result:
    # After observing all results average hashing gives best result.
    
            
        
    
    