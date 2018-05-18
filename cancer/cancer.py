#import .evolve-minimal
import neat
from sklearn.model_selection import KFold
import numpy as np
from evolve import run
# Load Data
file = open('cancer.txt')
diabetes_inputs = []
diabetes_output = []

for line in file:
    lineSplitted = line.split("   ")
    lineSplitted = lineSplitted[1:]
    patterns = list(map(float, lineSplitted))
    diabetes_inputs.append(tuple(patterns[:-1]))
    diabetes_output.append((patterns[-1],))

# Fitness function for use in kfold.
def kfold_fitness(net, test_set, n_test):
    fitness = n_test
    for xi, xo in test_set:
        output = net.activate(xi)
        fitness -= (output[0] - xo[0]) ** 2
    return fitness

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

n_sp = 10
kfolder = KFold(n_splits=n_sp, shuffle=True)
fitness_acum = 0
acc_acum = 0
diabetes_output = np.asarray(diabetes_output)
diabetes_inputs = np.asarray(diabetes_inputs)
folds = 0
for train_index, test_index in kfolder.split(diabetes_inputs):
    print(" NEW KFOLD ")
    #print(" TRAIN: ", train_index, " TEST: ", test_index)
    in_train, in_test = diabetes_inputs[train_index], diabetes_inputs[test_index]
    out_train, out_test = diabetes_output[train_index], diabetes_output[test_index]
    in_train = in_train.tolist()
    in_test = in_test.tolist()
    out_train = out_train.tolist()
    out_test = out_test.tolist()
    test_set = list(zip(in_test,out_test))
    winner = run(in_train, out_train)
    n_test = len(in_test)
    fold_fitness = kfold_fitness(winner, test_set, n_test)
    acc = kfold_acc(winner, test_set, n_test)
    acc_acum += acc
    fitness_acum += fold_fitness
    print(" FOLD FITNESS : ", fold_fitness)
    print(" FOLD ACC : ", acc)
    folds += 1
final_fitness = fitness_acum / folds
final_acc = acc_acum / folds
print( " FITNESS TOTAL : ", final_fitness)
print( " ACC TOTAL : ", final_acc)



