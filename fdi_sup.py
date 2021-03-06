# -*- coding: utf-8 -*-
"""FDI_SUP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15Jkw1lHsH8YYbdVWRNtJdAebe3I12Gef
"""

import tensorflow as tf
import numpy as np
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
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score

drive.mount('/content/drive')

zip_ref = zipfile.ZipFile("/content/drive/My Drive/SeqData.zip", 'r')
zip_ref.extractall("/home")
zip_ref.close()

!ls /home/ReadDataFolder

path = "/home/ReadDataFolder/"
def rearrangeData(dp):
  a = []
  for i in range(dp.shape[0]):
    a.append(dp[i,1:])
  return np.array(a)

def extractdata(fname):
  data =  pd.read_csv(path + fname,sep=' ',header=None)
  dataPoints = rearrangeData(data.to_numpy())
  return dataPoints


normal100 = []
normal300 = []
normal1500= []
failed100 = []
failed300 = [] 
failed1500= []

normal100Type = []
normal300Type = []
normal1500Type = []
failed100Type = []
failed300Type = [] 
failed1500Type = []

for filename in os.listdir(path):
  if filename[-2] == 'N':
    datap = extractdata(filename)
    if datap.shape[0] == 100:
      normal100.append(datap)
      normal100Type.append(filename[-2:])
    elif datap.shape[0] == 300:
      normal300.append(datap)
      normal300Type.append(filename[-2:])
    else:
      normal1500.append(datap)
      normal1500Type.append(filename[-2:])
  else:
    datap = extractdata(filename)
    if datap.shape[0] == 100:
      failed100.append(datap)
      failed100Type.append(filename[-2:])
    elif datap.shape[0] == 300:
      failed300.append(datap)
      failed300Type.append(filename[-2:])
    else:
      failed1500.append(datap)
      failed1500Type.append(filename[-2:])

normal100 = np.array(normal100)
failed100 = np.array(failed100)
normal300 = np.array(normal300)
failed300 = np.array(failed300)
normal1500= np.array(normal1500)
failed1500= np.array(failed1500)

print(normal300Type)

print(normal100.shape)
print(failed100.shape)
print(normal300.shape)
print(failed300.shape)
print(normal1500.shape)
print(failed1500.shape)

p = 5

plt.plot(normal1500[p][:,0],normal1500[p][:,1])
plt.plot(normal1500[p][:,0],normal1500[p][:,2])
plt.plot(normal1500[p][:,0],normal1500[p][:,3])
plt.plot(normal1500[p][:,0],normal1500[p][:,4])
plt.show()

plt.plot(normal1500[p][:,0],normal1500[p][:,5])
plt.plot(normal1500[p][:,0],normal1500[p][:,6])
plt.plot(normal1500[p][:,0],normal1500[p][:,7])
plt.show()

plt.plot(normal1500[p][:,0],normal1500[p][:,8])
plt.plot(normal1500[p][:,0],normal1500[p][:,9])
plt.plot(normal1500[p][:,0],normal1500[p][:,10])
plt.plot(normal1500[p][:,0],normal1500[p][:,11])
plt.show()

plt.plot(normal1500[p][:,0],normal1500[p][:,12])
plt.plot(normal1500[p][:,0],normal1500[p][:,13])
plt.plot(normal1500[p][:,0],normal1500[p][:,14])
plt.plot(normal1500[p][:,0],normal1500[p][:,15])
plt.plot(normal1500[p][:,0],normal1500[p][:,16])
plt.plot(normal1500[p][:,0],normal1500[p][:,17])
plt.plot(normal1500[p][:,0],normal1500[p][:,18])
plt.plot(normal1500[p][:,0],normal1500[p][:,19])
plt.show()

p = 5

plt.plot(failed1500[p][:,0],failed1500[p][:,1])
plt.plot(failed1500[p][:,0],failed1500[p][:,2])
plt.plot(failed1500[p][:,0],failed1500[p][:,3])
plt.plot(failed1500[p][:,0],failed1500[p][:,4])
plt.show()

plt.plot(failed1500[p][:,0],failed1500[p][:,5])
plt.plot(failed1500[p][:,0],failed1500[p][:,6])
plt.plot(failed1500[p][:,0],failed1500[p][:,7])
plt.show()

plt.plot(failed1500[p][:,0],failed1500[p][:,8])
plt.plot(failed1500[p][:,0],failed1500[p][:,9])
plt.plot(failed1500[p][:,0],failed1500[p][:,10])
plt.plot(failed1500[p][:,0],failed1500[p][:,11])
plt.show()

plt.plot(failed1500[p][:,0],failed1500[p][:,12])
plt.plot(failed1500[p][:,0],failed1500[p][:,13])
plt.plot(failed1500[p][:,0],failed1500[p][:,14])
plt.plot(failed1500[p][:,0],failed1500[p][:,15])
plt.plot(failed1500[p][:,0],failed1500[p][:,16])
plt.plot(failed1500[p][:,0],failed1500[p][:,17])
plt.plot(failed1500[p][:,0],failed1500[p][:,18])
plt.plot(failed1500[p][:,0],failed1500[p][:,19])
plt.show()

seqlength = 100
overlap = 1.0
dataCollection = []
dataType = []

for i in range(normal300.shape[0]):
  ldata = normal300[i]
  ldata[1:,11:] = ldata[1:,11:]-ldata[:-1,11:]
  ltype = normal300Type[i]
  for j in range(0,ldata.shape[0]-seqlength,int(seqlength*overlap)):
    dataCollection.append(ldata[j:j+seqlength][:])
    dataType.append(ltype)

for i in range(normal1500.shape[0]):
  ldata = normal1500[i]
  ldata[1:,11:] = ldata[1:,11:]-ldata[:-1,11:]
  ltype = normal1500Type[i]
  for j in range(0,ldata.shape[0]-seqlength,int(seqlength*overlap)):
    dataCollection.append(ldata[j:j+seqlength][:])
    dataType.append(ltype)

for i in range(failed300.shape[0]):
  ldata = failed300[i]
  ldata[1:,11:] = ldata[1:,11:]-ldata[:-1,11:]
  ltype = failed300Type[i]
  for j in range(0,ldata.shape[0]-seqlength,int(seqlength*overlap)):
    dataCollection.append(ldata[j:j+seqlength][:])
    dataType.append(ltype)

for i in range(failed1500.shape[0]):
  ldata = failed1500[i]
  ldata[1:,11:] = ldata[1:,11:]-ldata[:-1,11:]
  ltype = failed1500Type[i]
  for j in range(0,ldata.shape[0]-seqlength,int(seqlength*overlap)):
    dataCollection.append(ldata[j:j+seqlength][:])
    dataType.append(ltype)

dataCollection = np.array(dataCollection)
print(dataCollection.shape)
print(dataType)

def extractFeatures(dp):
  f = []
  eps = 1e-16
  for i in range(1,dp.shape[1]):
    # temporal
    M = np.mean(dp[:,i]) # mean
    AM = np.mean(np.absolute(dp[:,i])) # absolute mean
    RMS = np.sqrt(np.mean(np.power(dp[:,i],2))) # RMS
    AVP = np.mean(np.power(dp[:,i],2)) # Average power
    ROA = np.mean(np.sqrt(np.absolute(dp[:,i])))**2.0 # Root Amplitude
    PE = np.max(np.absolute(dp[:,i])) # peak
    PEP = np.max(dp[:,i]) - np.min(dp[:,i]) # peak 2 peak
    VA = np.var(dp[:,i]) # variance
    STD = np.std(dp[:,i]) # standard dev
    SK = skew(dp[:,i]) # skewness
    KU = kurtosis(dp[:,i]) # kurtosis

    WAI = (RMS+eps)/(AM+eps)
    IMI = (PE+eps)/(AM+eps)
    CRI = (PE+eps)/(RMS+eps)
    MAI = (PE+eps)/(ROA+eps)
    SKI = (SK+eps)/(STD**3+eps)
    KUI = (KU+eps)/(STD**4+eps)

    #frequency
    xd = dp[1:,i]-dp[:-1,i]
    FC = (np.dot(dp[1:,i],xd) + eps)/(2.0*np.pi*np.dot(dp[:,i],dp[:,i]) + eps)
    MSF = (np.dot(xd,xd) + eps)/(4.0*(np.pi**2)*np.dot(dp[:,i],dp[:,i]) + eps)
    RMSF = np.sqrt(MSF)
    VF = MSF - FC**2
    RVF = np.sqrt(np.absolute(VF))

    #f = f + [M,AM,RMS,AVP,ROA,PE,PEP,VA,STD,SK,KU,WAI,CRI,IMI,MAI,SKI,KUI,FC,MSF,RMSF,VF,RVF]
    f = f + [M,AM,RMS,ROA,PEP,STD,SK,KU,WAI,CRI,IMI,MAI,FC,MSF,RMSF,VF,RVF]
  return np.array(f)

X = []
classname = []
for i in range(len(dataCollection)):
  dp = dataCollection[i]
  features = extractFeatures(dp)
  X.append(features)
  if dataType[i][0] == 'N':
    classname.append(0)
  else:
    classname.append(1)

data = np.array(X)
classes = np.array(classname)

idx = np.random.permutation(data.shape[0])
Xt,y = data[idx], classes[idx]

print(Xt.shape,y.shape)
print(y)

#np.save('TSF_2.npy', Xt) # save
#np.save('TSC_2.npy', y)

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

N = int(X.shape[0]*0.8)
Xtrain = X[:N]
ytrain = y[:N]

Xtest = X[N:]
ytest = y[N:]
print(N)

pca = PCA(n_components = 10)
  
X_train = pca.fit_transform(Xtrain)
X_test = pca.transform(Xtest)

print(X_train.shape)
print(X_test.shape)
print(X_test)

classfier_names = ['KNN','DTree','RForest_D5_N10','RForest_D3_N1000','NN','AdaBoost','QDA']
classifiers1 = [
    KNeighborsClassifier(),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    RandomForestClassifier(max_depth=3, n_estimators=1000, max_features=1),
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(),
    QuadraticDiscriminantAnalysis()]
itr = 0
for clf in classifiers1:
  clf.fit(X_train, ytrain)
  ypred = clf.predict(X_test)
  score = clf.score(X_test, ytest)
  #y_score = clf.decision_function(X_test)
  print(classfier_names[itr]+'-Score: ',score)

  y_score = clf.predict_proba(X_test)
  y_score = y_score[:,1]
  
  y_true = ytest


  # Compute ROC curve and ROC area for each class
  fpr = dict()
  tpr = dict()
  roc_auc = dict()
  for i in range(1):
      fpr[i], tpr[i], _ = roc_curve(y_true, y_score)
      roc_auc[i] = auc(fpr[i], tpr[i])

  # Compute micro-average ROC curve and ROC area
  fpr["micro"], tpr["micro"], _ = roc_curve(y_true.ravel(), y_score.ravel())
  roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
  

  plt.figure(1,figsize=(8, 8),dpi=300)
  lw = 2
  colorV = np.random.rand(1,3)
  plt.plot(fpr[0], tpr[0],color = (colorV[0][0],colorV[0][1],colorV[0][2]),
          lw=lw, label='ROC curve'+' ' + classfier_names[itr] +' (Acc = %0.3f)' % score)
  plt.legend(loc="lower right")
  if (itr == 0):
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlabel('False Positive Rate',fontsize=12)
    plt.ylabel('True Positive Rate',fontsize=12)
    plt.title('Receiver operating characteristic example',fontsize=15)
    plt.grid()
    plt.yticks(fontsize=12)
    plt.yticks(fontsize=12)
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.05])
  

  itr += 1

clf = LinearSVC(random_state=0, tol=1e-5)
clf.fit(X_train, ytrain)
ypred = clf.predict(X_test)
score = clf.score(X_test, ytest)
print('SVC-Score: ',score)
y_score = clf.decision_function(X_test)
print(y_score)
y_true = ytest
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(1):
  fpr[i], tpr[i], _ = roc_curve(y_true, y_score)
  roc_auc[i] = auc(fpr[i], tpr[i])

fpr["micro"], tpr["micro"], _ = roc_curve(y_true.ravel(), y_score.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
plt.figure(1)
plt.plot(fpr[0], tpr[0],color = (colorV[0][0],colorV[0][1],colorV[0][2]),
          lw=lw, label='ROC curve ' + 'SVC' +' (Acc = %0.3f)' % score)

plt.savefig("Supervised.jpg")
plt.show()

plt.hist(y_score,100)

# voting (soft)
# sklearn.ensemble.VotingClassifier
classifiers1 = [
    KNeighborsClassifier(),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    QuadraticDiscriminantAnalysis()]
classifiers2 = [
    LinearSVC(random_state=0, tol=1e-5),
    SVC(kernel=RBF(), C=0.025,probability=True), # predict_proba - True
    #SVC(gamma=2, C=1),
    #GaussianProcessClassifier(1.0 * RBF(1.0))
    ]


estimators = []
i = 1
for clf in classifiers1:
  estimators.append((str(i),clf))
  i+=1
for clf in classifiers2:
  estimators.append((str(i),clf))
  i+=1

eclf = VotingClassifier(estimators=estimators, voting='hard') # soft
eclf.fit(X_train, ytrain)
ypred = eclf.predict(X_test)
score = eclf.score(X_test,ytest)
print('Ensemble Score: ',score)

# DB Scan
# K-means, GMM (Bayesian)
# 1 class SVM

classifiers2 = [
    LinearSVC(random_state=0, tol=1e-5),
    #SVC(kernel=RBF(), C=0.025),
    #SVC(gamma=2, C=1),
    GaussianProcessClassifier(1.0 * RBF(1.0))]

for clf in classifiers2:
  clf.fit(X_train, ytrain)
  ypred = clf.predict(X_test)
  score = clf.score(X_test, ytest)
  print('Score: ',score)

Xpass = []
Xfail = []
y_true = []

pca_us = PCA(n_components = 140)
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
Xus_test  = np.vstack((Xfail,Xpass[N:]))
print(Xus_train.shape,Xus_test.shape,y_true.shape)
print(y_true)

def sepPlot(distance,n):
  dm = []
  for i in range(distance.shape[0]):
    dm.append(np.min(distance[i]))
  dm = np.array(dm)
  plt.plot(np.log10(dm))
  plt.show()
  plt.title(str(n) + '-clusters')

for ncluster in range(1000,3000,200):
  kmeans = KMeans(n_clusters=ncluster, random_state=0)
  kmeans.fit(Xus_train)
  distance = kmeans.transform(Xus_test)
  #prediction = kmeans.predict(Xus_test)
  sepPlot(distance,ncluster)

pca_us = PCA(n_components = 2)
Xpca = pca_us.fit_transform(X)
print(Xpca.shape)
clf = OneClassSVM(kernel=RBF(),gamma='auto').fit(Xpca[:int(Xpca.shape[0]/2)])
y_pred = clf.predict(Xpca)
print(y_pred)

confusion_matrix(y_true, y_pred)