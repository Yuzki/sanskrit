import tensorflow as tf
import tensorflow_text as text
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
import string
import re
import pathlib
import os
import logging
import collections
import tqdm


n = 0
if n >= 0 and n < 6:
    work_dir = f'/sandhi/n{n}/'




logging.getLogger('tensorflow').setLevel(logging.ERROR)  # suppress warnings


export_dir = work_dir + 'translator'
translator = tf.saved_model.load(export_dir=export_dir)


vname = work_dir + 'val.csv'

sentence_list = []
grtruth_list = []
with open(vname, mode='r', encoding='utf-8') as f:
    for line in f:
        samh, pada = line.rstrip().split(',')
        sentence_list.append(samh)
        grtruth_list.append(pada)


def get_score(y_test, y_out):
    precisions = []
    recalls = []
    accuracies = []

    for outp, gen in zip(y_test, y_out):
        outpl = outp.split(' ')
        genl = gen.split(' ')

        intersection = set(outpl).intersection(genl)
        prec = len(intersection) * 1.0 / len(genl)
        recall = len(intersection) * 1.0 / len(outpl)

        if outp == gen:
            accuracies.append(1.0)
        else:
            accuracies.append(0.0)
        
        precisions.append(prec)
        recalls.append(recall)
        
    return(precisions, recalls, accuracies)

# example_sentence = 'agnfim Ixe purohfitam'
# example_trans = translator(example_sentence)

# print('Example Input: ' + example_sentence)
# print('Example Output: ' + example_trans.numpy().decode('utf-8'))

print('Translating ' + str(len(sentence_list)) + ' sentences')
gen_list = []
for index_sent in tqdm.tqdm(range(len(sentence_list))):
    sentence = sentence_list[index_sent]
    ground_truth = grtruth_list[index_sent]
    translated_text = translator(sentence).numpy().decode('utf-8')
    gen_list.append(translated_text)
# gen_list = [translator(sentence_list[index_sent]).numpy().decode('utf-8') for index_sent in range(len(sentence_list))]

with open(work_dir + 'transl.txt', mode='w', encoding='utf-8') as f:
    for ind, tru_sent in enumerate(sentence_list):
        gen_sent = gen_list[ind]
        f.write(tru_sent + '\n' + gen_sent + '\n\n')

precisions, recalls, accuracies = get_score(grtruth_list, gen_list)

avg_prec = np.mean(np.array(precisions)) * 100.0
avg_recall = np.mean(np.array(recalls)) * 100.0
f1_score = 2 * avg_prec * avg_recall / ( avg_prec + avg_recall )
avg_acc = np.mean(np.array(accuracies))

rname = work_dir + 'score.txt'
with open(rname, mode='w', encoding='utf-8') as f:
    f.write('Precision: ' + str(avg_prec) + '\n'
        + 'Recall:' + str(avg_recall) + '\n'
        + 'F1: ' + str(f1_score) + '\n'
        + 'Accuracy: ' + str(avg_acc))

print('Result is in ' + rname)