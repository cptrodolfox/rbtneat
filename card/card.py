from sklearn.model_selection import KFold

import random
import numpy as np

from evolve import run
import neat

# Load Data
file = open('card.txt')
inputs = []
outputs = []
attr = []

for line in file:
    lineSplitted = line.split("   ")
    lineSplitted = lineSplitted[1:]
    patterns = list(map(float, lineSplitted))
    attr.append(patterns)

random.shuffle(attr)

for pattern in attr:
    inputs.append(tuple(pattern[:-1]))
    outputs.append((pattern[-1],))

def kfold_fit(net, test_set, n_test):
    fitness = n_test
    for xi, xo in test_set:
        output = net.activate(xi)
        fitness -= (output[0] - xo[0]) ** 2
    return fitness / n_test  


# Our sign function
def our_sign(x):
    if x > 0.5:
        return 1
    else:
        return 0

# Accuracy of network
def kfold_acc(net, test_set, n_test):
    count = 0
    for xi, xo in test_set:
        output = net.activate(xi)
        if our_sign(output[0]) == xo[0]:
            count += 1
    acc = count/n_test 
    return acc

# Ten K-Fold for RBTNEAT

def kfold(inputs,outputs,config):
    n_sp = 10
    kfolder = KFold(n_splits=n_sp, shuffle=True)
    fit_acum = 0
    acc_acum = 0
    time_average_acum = 0
    generations_acum = 0
    fitn = []
    accu = []
    tim = []
    gen = []
    genomes = []
    outputs = np.asarray(outputs)
    inputs = np.asarray(inputs)
    folds = 0
    for train_index, test_index in kfolder.split(inputs):
        print('--------------------------------------------------------------')
        print(" KFOLD: " + str(folds))
        #print(" TRAIN: ", train_index, " TEST: ", test_index)
        in_train, in_test = inputs[train_index], inputs[test_index]
        out_train, out_test = outputs[train_index], outputs[test_index]
        in_train = in_train.tolist()
        in_test = in_test.tolist()
        out_train = out_train.tolist()
        out_test = out_test.tolist()
        test_set = list(zip(in_test,out_test))
        result = run(in_train, out_train,config)
        time_average, generations = result['evol']
        n_test = len(in_test)
        fit = kfold_fit(result['net'], test_set, n_test)
        acc = kfold_acc(result['net'], test_set, n_test)
        fit_acum += fit
        acc_acum += acc
        time_average_acum += time_average
        generations_acum += generations
        fitn.append(fit)
        accu.append(acc)
        tim.append(time_average)
        gen.append(generations)
        genomes.append(result['genome'])
        print(" FOLD Fit: ", fit)
        print(" FOLD Acc: ", acc)
        print(" FOLD Time: ", time_average)
        folds += 1

    final_fit = fit_acum / folds
    final_acc = acc_acum / folds
    final_time =  time_average_acum / folds
    final_generations = generations_acum / folds
    print('--------------------------------------------------------------')
    print(" Fitness list: ", str(fitn))
    print(" Accuracy list: ", str(accu))
    print(" Average Time list: ", str(tim))
    print(" Generations list: ", str(gen))
    print(" Fitness: ", final_fit)
    print(" Accuracy: ", final_acc)
    print(" Average Time: ", final_time)
    print(" Generations: ", final_generations)

    return {'f_fit': final_fit, 'f_acc': final_acc, 'f_time': final_time, 'f_generations': final_generations, 'fit_list': fitn, 'accu_list': accu, 'time_list' : tim, 'gen_list': gen, 'genomes': genomes }

kfold(inputs,outputs,'config-feedforward')

