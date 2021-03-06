# -*- coding: utf-8 -*-
"""FDI_IGMM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uynfwf5hKhL5fZwA68RGD2tme8FxH76M
"""

!pip install sklearn-som
import tensorflow as tf
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import urllib
import sys
import os
import zipfile
import torch.nn as nn
import torch.nn.functional as F
import torch
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader, random_split
import numpy.random as r

import torchvision
from torchvision.datasets import FashionMNIST
from torchvision import transforms
import pandas as pd
from google.colab import drive
from scipy.stats import skew
from scipy.stats import kurtosis
from sklearn import svm
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel, RBF
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.svm import OneClassSVM
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import LocalOutlierFactor
from sklearn_som.som import SOM

drive.mount('/content/drive')

Xt = np.load('/content/drive/My Drive/TSF_1.npy') # load
y = np.load('/content/drive/My Drive/TSC_1.npy')

Xmax = np.amax(Xt,0)
Xmin = np.amin(Xt,0)
X = np.zeros_like(Xt)

#Normalization
difvals = Xmax-Xmin
for i in range(Xt.shape[0]):
  X[i,:] = np.divide(Xt[i,:] - Xmin, difvals)
Xmax = np.amax(X,0)
Xmin = np.amin(X,0)
print(Xmax,Xmin)

Xpass = []
Xfail = []
y_true = []

pca_us = PCA(n_components = 60)
Xpca = pca_us.fit_transform(X)

for i in range(X.shape[0]):
  if y[i] == 0:
    Xpass.append(Xpca[i])
    y_true.append(1)
  else:
    Xfail.append(Xpca[i])
    y_true.append(-1)

Xpass = np.array(Xpass)
Xfail = np.array(Xfail)
y_true = np.array(y_true)
print(Xpass.shape,Xfail.shape)

N = int(0.8*Xpass.shape[0])
Xus_train = Xpass[:N]
Nf = Xfail.shape[0]
Xus_test  = np.vstack((Xfail,Xpass[N:]))
print(Xus_train.shape,Xus_test.shape,y_true.shape)
print(y_true)

# data generation
classes = {}
class_map = []

data = []
for i in range(N):
	classes[i] = [i]
	class_map.append(i)
dataNN = Xus_train
dataNNT = Xus_test
data = np.zeros_like(Xus_train)
datat = np.zeros_like(Xus_test)

#Normalization
dataMean = np.mean(dataNN,axis=0)
dataStd  = np.std(dataNN,axis=0)

for i in range(dataNN.shape[0]):
  data[i] = np.divide(dataNN[i]-dataMean,dataStd)
for i in range(dataNNT.shape[0]):
  datat[i] = np.divide(dataNNT[i]-dataMean,dataStd)

distance_array = []
l = data.shape[0]
minvs = 0
for i in range(l):
  minv = np.Inf
  print(i/l*100)
  for j in range(l):
    if (i!=j):
      d = la.norm(data[i]-data[j])
      if (d < minv):
        minv = d
  minvs = minvs + minv
  distance_array.append(minv*minv)
minvs = minvs/l;
distance_array = np.array(distance_array)
print(distance_array)
avg_distance = minvs*minvs + 0*np.mean(distance_array,axis=0)
print(avg_distance)

np.save('data.npy', data) # save
np.save('datat.npy', datat)
np.save('dArray.npy',distance_array)
np.save('avg_dist.npy',avg_distance)

dataAll = np.load('/content/drive/My Drive/60-pca/data.npy') # load
datatAll = np.load('/content/drive/My Drive/60-pca/datat.npy') # load
distance_array = np.load('/content/drive/My Drive/60-pca/dArray.npy') # load
avg_distance = np.load('/content/drive/My Drive/60-pca/avg_dist.npy') # load

data = dataAll[:6000]
l = data.shape[0]

class_map = []
classes = {}
for i in range(l):
	classes[i] = [i]
	class_map.append(i)

ncluster = 100
kmeans = KMeans(n_clusters=ncluster, random_state=0)
kmeans.fit(dataAll)

class_map = kmeans.labels_
classes = {}
for i in range(class_map.shape[0]):
  cls = class_map[i]
  if cls in classes.keys():
    classes[cls].append(i)
  else:
    classes[cls] = []
    classes[cls].append(i)
class_map = list(class_map)

print(class_map,classes.keys())

# IGMM
itr = 0
Nitr = 5*N
l = data.shape[0]
for i in range(Nitr):
  alpha = 1.0/len(classes.keys())
  if (i%5 == 0):
    print("%:",i/Nitr*100)
		
  itr = np.random.choice(l, 1)[0]
  x = data[itr,:]
  cls = class_map[itr]
  classes[cls].remove(itr)
	
  sel_prob = []
  sel_clst = []
  del_keys = []
  
  for c in classes.keys():
    # print("Key: ",c)
    cdataList = classes[c]
    if (len(cdataList) > 0):
      cdata = data[cdataList,:]
      mu = np.mean(cdata,axis = 0)
      sig = None
      if len(cdataList) > 1:
        sig = np.cov(cdata.T)
      else:
        sig = distance_array[itr]*np.identity(data.shape[1])
      val = len(cdataList)/(alpha+N-1)
      if np.absolute(la.det(sig)) < 1e-8:
        u, s, vh = np.linalg.svd(sig)
        sig = np.identity(data.shape[1])
        for i in range(data.shape[1]):
          sig[i,i] = s[0]
          
      p = np.exp(-0.5*(x-mu) @ la.inv(sig) @ (x-mu).T)
      sel_prob.append(val*p)
      sel_clst.append(c)
    else:
      del_keys.append(c)
	
  for key in del_keys:
    del classes[key]
  val = alpha/(alpha + N-1)
  sig = distance_array[itr]*np.identity(2)
  p = 1
  sel_prob.append(val*p)
  sel_prob = np.array(sel_prob)
  sel_prob = sel_prob/np.sum(sel_prob)
  
  mv = max(sel_clst)
  new_class = None
  for i in range(mv):
    if i not in sel_clst:
      new_class = i
      break
  if new_class == None:
    new_class = mv+1
		
  sel_clst.append(new_class)
  sel_cls = r.choice(sel_clst, 1, p=sel_prob)[0]
  class_map[itr] = sel_cls
  if sel_cls in classes.keys():
    classes[sel_cls] += [itr]
  else:
    classes[sel_cls] = [itr]
		
print(classes,len(classes))

import json
with open('classes.json', 'w') as f:
  json.dump(classes, f)
#with open('my_dict.json') as f:
#  classes = json.load(f)

with open("class_map.txt", "w") as fp:
  json.dump(class_map, fp)

#with open("class_map.txt", "r") as fp:
#  class_map = json.load(fp)

new_cluster_prob = []
class_map_test = []
classes_test = {}
for i in range(dataNNT.shape[0]):
	alpha = 1.0/len(classes.keys())
	x = datat[i]
	sel_prob = []
	sel_clst = []
	del_keys = []
	for c in classes.keys():
		# print("Key: ",c)
		cdataList = classes[c]
		if (len(cdataList) > 0):
			cdata = data[cdataList,:]
			mu = np.mean(cdata,axis = 0)
			sig = None
			if len(cdataList) > 1:
				sig = np.cov(cdata.T)
			else:
				sig = avg_distance*np.identity(data.shape[1])
			val = len(cdataList)/(alpha+N-1)
			if np.absolute(la.det(sig)) < 1e-8:
				u, s, vh = np.linalg.svd(sig)
				#print(s)
				sig = np.identity(data.shape[1])
				for i in range(data.shape[1]):
				 	sig[i,i] = s[0]
				 	
			vec = (x-mu).reshape(1,-1)
      p = np.exp(-0.5*vec @ la.inv(sig) @ vec.T)
			sel_prob.append(val*p)
			sel_clst.append(c)
			
	val = alpha/(alpha + N-1)
	sig = avg_distance*np.identity(data.shape[1])
	
	p = 1
	sel_prob.append(val*p)
	sel_prob = np.array(sel_prob)
	sel_prob = sel_prob/np.sum(sel_prob)
		
	lclass_name = np.argmax(sel_prob)
	
	if lclass_name in classes_test.keys():
		classes_test[lclass_name].append(i)
	else:
		classes_test[lclass_name] = []
		classes_test[lclass_name].append(i)
	
	class_map_test.append(lclass_name)
	new_cluster_prob.append(sel_prob[-1])

new_cluster_prob = np.array(new_cluster_prob)
class_map_test   = np.array(class_map_test)