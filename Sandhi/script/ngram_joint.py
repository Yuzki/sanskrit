def joint_ngram(ngram_sent):
    ngram_list = ngram_sent.split(' ')

    delete_index_list = []

    for index_word in range(len(ngram_list) - 1):

        g1 = ngram_list[index_word]
        g2 = ngram_list[index_word + 1]

        g_len = min(len(g1), len(g2))

        for joint_point in range(g_len):
            
            if g1[(len(g1) - joint_point):] == g2[:joint_point]:
                g2_joint = g1[:(len(g1) - joint_point)] + g2
                # print(g1, g2)
                ngram_list[index_word + 1] = g2_joint
                delete_index_list.append(index_word)
    
    return [ngram_list[i] for i in range(len(ngram_list)) if not i in delete_index_list]

import random
with open('./text/samhita_5-gram.txt', mode='r', encoding='utf-8') as f:
    lines = f.readlines()


i = random.randrange(len(lines))
sent = lines[i].rstrip()

with open('./text/samhita.txt', mode='r', encoding='utf-8') as f:
    trlines = f.readlines()


print(trlines[i].rstrip())
print(sent)
print(joint_ngram(sent)[0].split('R'))
