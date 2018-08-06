import numpy
import autograd
import matplotlib.pyplot as pl

dataset = {
    "hours" : [1, 2, 3, 4],
    "gpa" : [2, 4, 6, 8]
}


def compute_gradient(w, x, y, bias):
    gradient_sum = 0
    for i in range(0, len(x)):
        partial = 2*((w*x[i]) - y[i])*x[i]
        gradient_sum += partial
    print('Gradient sum : ', gradient_sum)
    return -gradient_sum

def bias_gradient(w, x, y, bias):
    gradient_sum = 0
    for i in range(0, len(x)):
        partial = 2*((w*x[i] + bias) - y[i])
        gradient_sum+=partial
    return bias
    pass


lr = 0.0001 #learning rate


def train(epochs):

    #single neuron weight :
    w = 0 #random

    #bias = 1
    for i in range(0, epochs):
        wx = []
        for j in dataset['hours']:
            wxi = (w*j)
            wx.append(wxi)
    #compute mean squared error:
        mse = []
        for j in range(0, len(dataset['hours'])):
            mse.append((dataset['gpa'][j] - wx[j])**2)
        cost = sum(mse)/len(dataset['hours'])
        gradient = compute_gradient(w, dataset['hours'], dataset['gpa'], 0)
        w = w + lr*gradient
        #bias = bias+lr*bias_gradient(w, dataset['hours'], dataset['gpa'], bias)
        print("Cost : ", cost, "Weight: ", w, "For: ", i)

        if(cost == 0 or w < 0) : break


train(50000)
