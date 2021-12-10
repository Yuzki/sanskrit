import pickle
import re
import sys, os
import tqdm

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + '/utils/')
import ngram

def maketext():
    fname = '../text/RV_TITUS/RV_TITUS_dict_tsu.pkl'
    with open(fname, mode='rb') as f:
        text_dict = pickle.load(f)

    for book_num, hymns in tqdm.tqdm(text_dict.items()):
        print('Writing Book ' + str(book_num))
        for hymn_num, verses in tqdm.tqdm(hymns.items(), leave=False):
            for verse_num, padas in tqdm.tqdm(verses.items(), leave=False):
                for pada_num, texts in tqdm.tqdm(padas.items(), leave=False):
                    samhitapatha_text = texts[1]
                    padapatha_text = texts[2]

                    # print('{}.{}.{}.{}'.format(book_num, hymn_num, verse_num, pada_num))
                    with open('./text/samhita.txt', mode='a', encoding='utf-8') as fs:
                        s = samhitapatha_text
                        s = re.sub(r'(\{..\})', '', s)
                        s = re.sub(r'(\/!\/)', '', s)
                        s = re.sub('_', '', s)
                        s = re.sub(';', 'f', s)
                        fs.write(s.strip(' ') + '\n')
                    with open('./text/padapatha.txt', mode='a', encoding='utf-8') as fp:
                        p = padapatha_text
                        p = re.sub(r'(\{..\})', '', p)
                        p = re.sub(r'(\/!\/)', '', p)
                        p = re.sub('_', '', p)
                        p = re.sub(';', 'f', p)
                        fp.write(p.strip(' ') + '\n')


def inittext(fname):
    with open(fname, mode='w', encoding='utf-8') as fs:
        fs.write('')


def makengramtext(n, fname):
    fngram = fname[:-4] + '_{}-gram.txt'.format(n)
    
    inittext(fngram)
    with open(fname, mode='r', encoding='utf-8') as f:
        for line in tqdm.tqdm(f):
            line = line.rstrip()
            line = re.sub(' ', 'R', line)
            ngram_list = ngram.ngram(line, n)
            
            with open(fngram, mode='a') as fn:
                fn.write(' '.join(ngram_list) + '\n')




if __name__ == '__main__':
    fs = './text/samhita.txt'
    fp = './text/padapatha.txt'

    # print('Initialize Samhitapatha')
    # inittext(fs)
    # print('Initialize Padapatha')
    # inittext(fp)


    maketext()

    for n in range(6, 7):
    # for n in range(1, 6):
        print('Making {}-gram text'.format(n))
        makengramtext(n, fs)
        makengramtext(n, fp)
