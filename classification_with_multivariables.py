# -*- coding: utf-8 -*-
"""Classification with multivariables.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10Lk6tR-1kAEdqbJud5bfuc4yEgzvGSaV
"""

import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt

#suppress warnings
warnings.filterwarnings('ignore')

path = 'DataForLongMultiTarget.data'

data = pd.read_csv(path, header=None, names=['x1',
                                             'x2',
                                             'x3',
                                             'x4',
                                             'x5',
                                             'x6',
                                             'x7',
                                             'x8',
                                             'x9',
                                             'x10',
                                             'x11',
                                             'x12',
                                             'x13',
                                             'x14',
                                             'x15',
                                             'x16',
                                             'x17',
                                             'x18',
                                             'x19',
                                             'x20',
                                             'x21',
                                             'x22',
                                             'x23',
                                             'x24',
                                             'x25',
                                             'x26',
                                             'x27',
                                             'x28',
                                             'x29',
                                             'x30',
                                             'x31',
                                             'Admitted'])
#print("DATA : ",data.head(10))
arr = data.to_numpy()

cols = data.shape[1]-1
#print(arr[0][1])
Xdata = data.iloc[:,:cols]

#print(cols)
#print('X2 = ')
#print(X2.head(10))
#print('................................................')
Ydata = data.iloc[:,cols:cols+1]
#print('y2 = ')
#print(y2.head(10))
#print('................................................')

DataX = Xdata.to_numpy()
DataY = Ydata.to_numpy()

#print(data) 
#print(X) 
#print(Y)
#print('X Shape = ' ,  X.shape) 
#print('Y Shape = ', Y.shape)

#print(data['X'][0]) 
#print(data['X'][0][155]) 
#print('===================================================')


def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def cost(theta, X, y, learningRate):
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    first = np.multiply(-y, np.log(sigmoid(X * theta.T)))
    second = np.multiply((1 - y), np.log(1 - sigmoid(X * theta.T)))
    reg = (learningRate / 2 * len(X)) * np.sum(np.power(theta[:,1:theta.shape[1]], 2))
    return np.sum(first - second) / (len(X)) + reg


def gradient_with_loop(theta, X, y, learningRate):
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    
    parameters = int(theta.ravel().shape[1])
    grad = np.zeros(parameters)
    
    error = sigmoid(X * theta.T) - y
    
    for i in range(parameters):
        term = np.multiply(error, X[:,i])
        
        if (i == 0):
            grad[i] = np.sum(term) / len(X)
        else:
            grad[i] = (np.sum(term) / len(X)) + ((learningRate / len(X)) * theta[:,i])
    
    return grad

def gradient(theta, X, y, learningRate):
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    
    parameters = int(theta.ravel().shape[1])
    error = sigmoid(X * theta.T) - y
    
    grad = ((X.T * error) / len(X)).T + ((learningRate / len(X)) * theta)
    
    # intercept gradient is not regularized
    grad[0, 0] = np.sum(np.multiply(error, X[:,0])) / len(X)
    
    return np.array(grad).ravel()

from scipy.optimize import minimize

def one_vs_all(X, y, num_labels, learning_rate):
    rows = X.shape[0] #5000
    params = X.shape[1] #31
    
    # k X (n + 1) array for the parameters of each of the k classifiers
    all_theta = np.zeros((num_labels, params + 1))
    
    print('all_theta shape ' , all_theta.shape)
    # insert a column of ones at the beginning for the intercept term
    X = np.insert(X, 0, values=np.ones(rows), axis=1)
    print('X shape ' , X.shape)
    
    # labels are 1-indexed instead of 0-indexed
    for i in range(1, num_labels + 1):
        theta = np.zeros(params + 1)
        y_i = np.array([1 if label == i else 0 for label in y])
        y_i = np.reshape(y_i, (rows, 1))
        
        # minimize the objective function
        fmin = minimize(fun=cost, x0=theta, args=(X, y_i, learning_rate), method='TNC', jac=gradient)
        all_theta[i-1,:] = fmin.x
    
    return all_theta



rows = DataX.shape[0]
params = DataX.shape[1]

#print('rows = ' ,rows)
#print('params = ' , params)

#print('===================================================')


all_theta = np.zeros((5, params + 1))

#print('all_theta \n' , all_theta)
#print('all_theta shape \n' , all_theta.shape)

print('===================================================')


X = np.insert(DataX, 0, values=np.ones(rows), axis=1)


#print(X) 
#print('X Shape = ' ,  X.shape) 

#print('===================================================')

theta = np.zeros(params + 1)

#print('theta \n' , theta ) 

#print('===================================================')


y_0 = np.array([1 if label == 0 else 0 for label in DataY])

#print('y_0')
#print(y_0.shape)
#print(y_0)

#print('===================================================')

y_0 = np.reshape(y_0, (rows, 1))


#print('y_0')
#print(y_0.shape)
#print(y_0)

#print('===================================================')

#print()
#print('X.shape = ',X.shape)
#print()
#print('y.shape = ',y_0.shape)
#print()
#print('theta.shape = ',theta.shape)
#print()
#print('all_theta.shape = ',all_theta.shape)

print()
print('data array = ' , np.unique(DataY))

print()

all_theta = one_vs_all(DataX, DataY, 5, 0.0000001)

print('Theta shape =   ' , all_theta.shape)
print('Theta = ')
print(all_theta)
 


def predict_all(X, all_theta):
    rows = X.shape[0]
    params = X.shape[1]
    num_labels = all_theta.shape[0]
    
    # same as before, insert ones to match the shape
    X = np.insert(X, 0, values=np.ones(rows), axis=1)
    
    # convert to matrices
    X = np.matrix(X)
    all_theta = np.matrix(all_theta)
    
    # compute the class probability for each class on each training instance
    h = sigmoid(X * all_theta.T)
    
    # create array of the index with the maximum probability
    h_argmax = np.argmax(h, axis=1)
    
    # because our array was zero-indexed we need to add one for the true label prediction
    h_argmax = h_argmax + 1
    
    return h_argmax

y_pred = predict_all(DataX, all_theta)
correct = [1 if a == b else 0 for (a, b) in zip(y_pred, DataY)]
accuracy = (sum(map(int, correct)) / float(len(correct)))
print ('accuracy = {0}%'.format(accuracy * 100))
 #46.29555320468391%

import numpy as np
import pandas as pd
import warnings

#suppress warnings
warnings.filterwarnings('ignore')

path = 'DataForLongMultiTarget.data'

data = pd.read_csv(path, header=None, names=['x1',
                                             'x2',
                                             'x3',
                                             'x4',
                                             'x5',
                                             'x6',
                                             'x7',
                                             'x8',
                                             'x9',
                                             'x10',
                                             'x11',
                                             'x12',
                                             'x13',
                                             'x14',
                                             'x15',
                                             'x16',
                                             'x17',
                                             'x18',
                                             'x19',
                                             'x20',
                                             'x21',
                                             'x22',
                                             'x23',
                                             'x24',
                                             'x25',
                                             'x26',
                                             'x27',
                                             'x28',
                                             'x29',
                                             'x30',
                                             'x31',
                                             'Admitted'])
degree = 4

for j in range(1,32):
  for i in range(1,32):
    if(j < i):
      for t in range(1, degree): # degree = 5 | 1,2,3,4
        for n in range(0, t):  # 0 , 1 , 2 ,2
          data['F ['+str(j)+']['+str(i)+']' + str(t) + str(n)] = np.power(data['x'+str(j)], t-n) * np.power(data['x'+str(i)], n) # i=3 , j=2

for i in range(1,32):
  data.drop('x'+str(i), axis=1, inplace=True)

#print("DATA : ",data.head(10))

cols = data.shape[1]-1
#print(arr[0][1])
Xdata = data.iloc[:,1:cols]

#print(cols)
#print('Xdata = ')
#print(Xdata.head(10))
#print('................................................')
Ydata = data.iloc[:,0:1]
#print('Ydata = ')
#print(Ydata.head(10))
#print('................................................')

DataX = Xdata.to_numpy()
DataY = Ydata.to_numpy()

#print('data') 
#print(DataX) 
#print(DataY)
#print('X Shape = ' ,  DataY.shape) 
#print('Y Shape = ', DataY.shape)

#print(data['X'][0]) 
#print(data['X'][0][155]) 
#print('===================================================')





def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def cost(theta, X, y, learningRate):
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    first = np.multiply(-y, np.log(sigmoid(X * theta.T)))
    second = np.multiply((1 - y), np.log(1 - sigmoid(X * theta.T)))
    reg = (learningRate / 2 * len(X)) * np.sum(np.power(theta[:,1:theta.shape[1]], 2))
    return np.sum(first - second) / (len(X)) + reg


def gradient_with_loop(theta, X, y, learningRate):
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    
    parameters = int(theta.ravel().shape[1])
    grad = np.zeros(parameters)
    
    error = sigmoid(X * theta.T) - y
    
    for i in range(parameters):
        term = np.multiply(error, X[:,i])
        
        if (i == 0):
            grad[i] = np.sum(term) / len(X)
        else:
            grad[i] = (np.sum(term) / len(X)) + ((learningRate / len(X)) * theta[:,i])
    
    return grad

def gradient(theta, X, y, learningRate):
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    
    parameters = int(theta.ravel().shape[1])
    error = sigmoid(X * theta.T) - y
    
    grad = ((X.T * error) / len(X)).T + ((learningRate / len(X)) * theta)
    
    # intercept gradient is not regularized
    grad[0, 0] = np.sum(np.multiply(error, X[:,0])) / len(X)
    
    return np.array(grad).ravel()

from scipy.optimize import minimize

def one_vs_all(X, y, num_labels, learning_rate):
    rows = X.shape[0] #5000
    params = X.shape[1] #31
    
    # k X (n + 1) array for the parameters of each of the k classifiers
    all_theta = np.zeros((num_labels, params + 1))
    
    print('all_theta shape ' , all_theta.shape)
    # insert a column of ones at the beginning for the intercept term
    X = np.insert(X, 0, values=np.ones(rows), axis=1)
    print('X shape ' , X.shape)
    
    # labels are 1-indexed instead of 0-indexed
    for i in range(1, num_labels + 1):
        theta = np.zeros(params + 1)
        y_i = np.array([1 if label == i else 0 for label in y])
        y_i = np.reshape(y_i, (rows, 1))
        
        # minimize the objective function
        fmin = minimize(fun=cost, x0=theta, args=(X, y_i, learning_rate), method='TNC', jac=gradient)
        all_theta[i-1,:] = fmin.x
    
    return all_theta



rows = DataX.shape[0]
params = DataX.shape[1]

#print('rows = ' ,rows)
#print('params = ' , params)

#print('===================================================')


all_theta = np.zeros((5, params + 1))

#print('all_theta \n' , all_theta)
#print('all_theta shape \n' , all_theta.shape)

print('===================================================')


X = np.insert(DataX, 0, values=np.ones(rows), axis=1)


#print(X) 
#print('X Shape = ' ,  X.shape) 

print('===================================================')

theta = np.zeros(params + 1)

#print('theta \n' , theta ) 

#print('===================================================')


y_0 = np.array([1 if label == 0 else 0 for label in DataY])

#print('y_0')
#print(y_0.shape)
#print(y_0)

#print('===================================================')

y_0 = np.reshape(y_0, (rows, 1))


#print('y_0')
#print(y_0.shape)
#print(y_0)

#print('===================================================')

#print()
#print('X.shape = ',X.shape)
#print()
#print('y.shape = ',y_0.shape)
#print()
#print('theta.shape = ',theta.shape)
#print()
#print('all_theta.shape = ',all_theta.shape)

#print()
#print('data array = ' , np.unique(DataY))

#print()





all_theta = one_vs_all(DataX, DataY, 5,1)

print('Theta shape =   ' , all_theta.shape)
print('Theta = ')
print(all_theta)
 


def predict_all(X, all_theta):
    rows = X.shape[0]
    params = X.shape[1]
    num_labels = all_theta.shape[0]
    
    # same as before, insert ones to match the shape
    X = np.insert(X, 0, values=np.ones(rows), axis=1)
    
    # convert to matrices
    X = np.matrix(X)
    all_theta = np.matrix(all_theta)
    
    # compute the class probability for each class on each training instance
    h = sigmoid(X * all_theta.T)
    
    # create array of the index with the maximum probability
    h_argmax = np.argmax(h, axis=1)
    
    # because our array was zero-indexed we need to add one for the true label prediction
    h_argmax = h_argmax + 1
    
    return h_argmax

y_pred = predict_all(DataX, all_theta)
correct = [1 if a == b else 0 for (a, b) in zip(y_pred, DataY)]
accuracy = (sum(map(int, correct)) / float(len(correct)))
print ('accuracy = {0}%'.format(accuracy * 100))

#44.23813519133258

from numpy.lib.function_base import place
import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier


path = '/content/drive/MyDrive/dataset /Mohammed.csv'
data = pd.read_csv(path, sep=',',header=None, names=['x1',
                                             'x2',
                                             'x3',
                                             'x4',
                                             'x5',
                                             'x6',
                                             'x7',
                                             'x8',
                                             'x9',
                                             'x10',
                                             'x11',
                                             'x12',
                                             'x13',
                                             'x14',
                                             'x15',
                                             'x16',
                                             'x17',
                                             'x18',
                                             'x19',
                                             'x20',
                                             'x21',
                                             'x22',
                                             'x23',
                                             'x24',
                                             'x25',
                                             'x26',
                                             'x27',
                                             'x28',
                                             'x29',
                                             'x30',
                                             'x31',
                                             'x32',
                                             'x33',
                                             'x34',
                                             'x35',
                                             'x36',
                                             'x37',
                                             'x38',
                                             'x39',
                                             'x40',
                                             'x41',
                                             'x42',
                                             'x43',
                                             'x44',
                                             'x45',
                                             'x46',
                                             'x47',
                                             'x48',
                                             'x49',
                                             'x50',
                                             'x51',
                                             'Admitted'])

positiveA = data[data['Admitted'].isin([1])]
negative = data[data['Admitted'].isin([0])]

#for i in range(1,51):
#   Mohammed test
#  fig, ax = plt.subplots(figsize=(15,15))
#  ax.scatter(positiveA['x'+str(i)], positiveA['x'+str(i+1)],s=50, c='#0000BF', marker='o', label='Accepted A')
#  ax.scatter(positiveB['x'+str(i)], positiveB['x'+str(i+1)],s=50, c='#002FFF', marker='o', label='Accepted B')
#  ax.scatter(positiveC['x'+str(i)], positiveC['x'+str(i+1)],s=50, c='#00AFFF', marker='o', label='Accepted C')
#  ax.scatter(positiveD['x'+str(i)], positiveD['x'+str(i+1)],s=50, c='#3FFFBF', marker='o', label='Accepted D')
#  ax.scatter(positiveE['x'+str(i)], positiveE['x'+str(i+1)],s=50, c='#BFFF3F', marker='o', label='Accepted E')
#  ax.scatter(negative['x'+str(i)], negative['x'+str(i+1)],s=50, c='r', marker='x', label='Rejected')
#  ax.legend()
#  ax.set_xlabel('Test '+str(i))
#  ax.set_ylabel('Test '+str(i+1))

y= data["Admitted"]
X = data.drop("Admitted",axis=1)
X['x1'].astype(float)

#print(y)
#print(X)
#print(X["x11"])
#print(X["x12"])


mymodel = KNeighborsClassifier()
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size= 0.2)

mymodel.fit(X_train,y_train)
print('score',mymodel.score(X_test,y_test))

print('score cross',cross_val_score(KNeighborsClassifier(350),X_train,y_train,cv=5,scoring='accuracy').mean())

#val_score= []
#for k in range(1,50):
#  score = cross_val_score(KNeighborsClassifier(k),X_train,y_train, cv = 5).mean()
#  val_score.append(score)
#plt.plot(val_score)

from sklearn.model_selection import validation_curve

k= np.arange(1,50)

train_score,val_score = validation_curve(mymodel,X_train,y_train,param_name='n_neighbors',param_range=k,cv=5)
plt.plot(k,val_score.mean(axis=1),label='validation')
plt.plot(k,train_score.mean(axis=1),label='train')
plt.ylabel('score')
plt.xlabel('n_neighbors')
plt.legend()

from sklearn.model_selection import GridSearchCV

param_grid = {'n_neighbors':np.arange(1,50),
              'metric':['euclidean','manhattan']}
grid = GridSearchCV(KNeighborsClassifier(),param_grid,cv=15)
grid.fit(X_train,y_train)
grid.best_score_

print('best score : ',grid.best_score_)
model = grid.best_estimator_
print('test score',model.score(X_test,y_test))

from sklearn.model_selection import learning_curve

N,train_score,val_score = learning_curve(model,X_train,y_train,np.linspace(0.1,1.0,50),cv=5)
plt.plot(N,train_score.mean(axis=1),label='train')
plt.plot(N,val_score.mean(axis=1),label='validation')
plt.xlabel('train_sizes')
plt.legend()

from google.colab import drive
drive.mount('/content/drive')