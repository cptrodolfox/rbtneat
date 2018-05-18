#import .evolve-minimal

from sklearn.model_selection import KFold
from itertools import zip_longest

import graphviz
import random
import numpy as np
import matplotlib.pyplot as plt

from card import kfold
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

inputs = [tuple(pattern[:-1]) for pattern in attr]
outputs = [(pattern[-1],) for pattern in attr]

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

# # Ten K-Fold for RBTNEAT
# def kfold(inputs, outputs, config_file):
#     n_sp = 10
#     kfolder = KFold(n_splits=n_sp, shuffle=True)
#     acc_acum = 0
#     time_average_acum = 0
#     generations_acum = 0
#     outputs = np.asarray(outputs)
#     inputs = np.asarray(inputs)
#     folds = 0
#     for train_index, test_index in kfolder.split(inputs):
#         print(" NEW KFOLD ")
#         #print(" TRAIN: ", train_index, " TEST: ", test_index)
#         in_train, in_test = inputs[train_index], inputs[test_index]
#         out_train, out_test = outputs[train_index], outputs[test_index]
#         in_train = in_train.tolist()
#         in_test = in_test.tolist()
#         out_train = out_train.tolist()
#         out_test = out_test.tolist()
#         test_set = list(zip(in_test,out_test))
#         winner, evol = run(in_train, out_train, config_file)
#         time_average, generations = evol
#         n_test = len(in_test)
#         acc = kfold_acc(winner, test_set, n_test)
#         acc_acum += acc
#         time_average_acum += time_average
#         generations_acum += generations
#         print(" FOLD Acc: ", acc)
#         print(" FOLD Time: ", time_average)
#         folds += 1

#     final_acc = acc_acum / folds
#     final_time =  time_average_acum / folds
#     final_generations = generations_acum / folds
#     print(" Accuracy: ", final_acc)
#     print(" Average Time: ", final_time)
#     print(" Generations: ", final_generations)

#     return final_time, final_generations

times_graph_ind = []
generations_graph_ind = []
s_blocks = 10
block = len(inputs)/s_blocks
blocks = []

for i in range(s_blocks):
    input_block = inputs[:int(block*(i+1))]
    output_block = outputs[:int(block*(i+1))]
    blocks.append(int(block*(i+1)))
    result = kfold(input_block, output_block, 'config-feedforward')
    times_graph_ind.append(result['f_time'])
    generations_graph_ind.append(result['f_generations'])

fig, ax1 = plt.subplots()
x = np.array(blocks)
y = np.array(times_graph_ind)

ax1.plot(x, y, 'b-')
ax1.set_xlabel('Number of pattern')
ax1.set_ylabel('Average time in seconds per generation', color='b')
ax1.tick_params('y', colors = 'b')

ax2 = ax1.twinx()
y2 = np.array(generations_graph_ind)
print(x)
print(y)
print(y2)
ax2.plot(x, y2, 'r-')
ax2.set_ylabel('Average number of generations', color='r')
ax2.tick_params('y', colors = 'r')

fig.tight_layout()
plt.title('Relationship patterns vs time vs generations')

plt.savefig("time vs patterns")
plt.close()

times_graph_attr = []
generations_graph_attr = []
s_blocks = 10
blocks = []
inputs_block = []
for i in range(s_blocks):
    for pattern in attr:
        block = int((len(pattern)-1)/s_blocks)
        inputs_block.append(tuple(pattern[:block*(i+1)]))
    blocks.append(block*(i+1))
    result = kfold(inputs_block, outputs,'config-block-' + str(i+1))
    inputs_block = []
    times_graph_attr.append(result['f_time'])
    generations_graph_attr.append(result['f_generations'])

fig, ax1 = plt.subplots()
x = np.array(blocks)
y = np.array(times_graph_attr)

ax1.plot(x, y, 'b-')
ax1.set_xlabel('Number of input attributes')
ax1.set_ylabel('Average time in seconds per generation', color='b')
ax1.tick_params('y', colors = 'b')

ax2 = ax1.twinx()
y2 = np.array(generations_graph_attr)
print(x)
print(y)
print(y2)
ax2.plot(x, y2, 'r-')
ax2.set_ylabel('Average number of generations', color='r')
ax2.tick_params('y', colors = 'r')

fig.tight_layout()
plt.title('Relationship between input vs time vs generations')

plt.savefig("time vs attr")
plt.close()
