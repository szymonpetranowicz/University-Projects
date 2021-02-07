from collections import Counter
import re



filepath = 'wiki.txt'
txt = open(filepath, 'r',encoding='utf-8')
x = txt.read().lower()

#tworzenie listy frekwencyjnej

words = re.split(r'\W+', x)
z = Counter(words).most_common()
a = []
s = {}
cleaned = {}

for i in z:
    s[i[0]] = i[1]
for i in range(48,57):
    a.append(chr(i))

for i in s:
    for b in i:
        if b not in a:
            cleaned[i] = s[i]

#preprocessing, odsiew słów poprawnych
tekst = (input("Wpisz tekst"))
tekst_list = tekst.lower().split()
przetwarzany = tekst.lower().split()

# z frekwencyjnej

for i in przetwarzany:
    if i in cleaned:
        przetwarzany.remove(i)
#z sjp

filepath_3 = 'slowa.txt'
txt_3 = open(filepath_3, 'r',encoding='utf-8')
slowa = txt_3.read().split()

for i in przetwarzany:
    if i in slowa:
        przetwarzany.remove(i)

#z clp

from clp3 import clp
clp_id = []
for i in przetwarzany:
    clp_id.append(clp(i))
    if clp(i) != []:
        przetwarzany.remove(i)

#definicja Levenstheina

import numpy as np

def levenstein(word1, word2):
    w1 = word1  # wiersze
    w2 = word2  # kolumny
    a = np.zeros((len(w1) + 1) * (len(w2) + 1)).reshape((len(w1) + 1), (len(w2) + 1))

    for i in range(0, len(w2) + 1):
        a[0][i] = i
    for i in range(0, len(w1) + 1):
        a[i][0] = i

    for b in range(1, len(w2) + 1):
        for i in range(1, len(w1) + 1):
            if w1[i - 1] == w2[b - 1]:
                a[i, b] = min(
                    a[i - 1, b] + 1,
                    a[i - 1, b - 1],
                    a[i, b - 1] + 1)
            else:
                a[i, b] = min(
                    a[i - 1, b] + 1,
                    a[i - 1, b - 1] + 1,
                    a[i, b - 1] + 1)

    a
    wynik = a[len(w1), len(w2)]
    return wynik

#porównywanie przez odległość Levenstheina błędnego słowa z słowami z sjp

lev = {}

for words in range(0,len(slowa)):
    print(words,'/3045885')
    for elements in przetwarzany:
        a = levenstein(slowa[words],elements)
        if a < 3 :
            lev[slowa[words]] = int(a)

#tworzenie dwuczłonowych słów korpusu

def n_gram(filepath):

    print('Tworzę dwuczłonowe słowa korpusu')
    txt = open(filepath, 'r', encoding='utf-8')

    x = txt.read().lower()

    words = re.split(r'\W+', x)

    double_words = []

    for i in range(0, len(words)-1):
        double_words.append(words[i] + ' ' + words[i + 1])

    z = Counter(double_words).most_common()
    double_words_freq = {}
    for i in range(0,len(z)):
        double_words_freq[z[i][0]] = z[i][1]
    return double_words_freq



double_words_freq =  n_gram('korpus.txt')
#odsiew słów z słownika lev które nie występują w korpusie

def n_gram_without_counter(filepath):
    print("Tworze pojędyncze słowa korpusu")
    txt = open(filepath, 'r', encoding='utf-8')

    x = txt.read().lower()

    words = re.split(r'\W+', x)
    return words

words_korpus = n_gram_without_counter('korpus.txt')

for i in set(lev.keys()):
    if i not in words_korpus:
        lev.pop(i)

print(lev)
#odnajdowanie indexu błędnego słowa w zdaniu

index = {}

for i in przetwarzany:
    index[i] = tekst_list.index(i)

#tworzenie dwuczłownych słów z słowem porpzedzającym lub następującym słowo błędne, z słowami sugerowanymi przez odległosć Levenstheina

double_word_back= []
double_word_front = []


for i in index:
    for e in lev:
     if index[i] == 0:
        double_word_front.append(e + ' ' + tekst_list[1])
     elif index[i] == len(tekst_list)-1:
        double_word_back.append(tekst_list[len(tekst_list)-2] +  ' ' + e)
     else:
        double_word_front.append(e + ' ' + tekst_list[index[i] + 1])
        double_word_back.append(tekst_list[index[i] - 1] +' ' + e)

#sprawdzanie częstotliwośći podwójnych słów w korpusie

max_double_words_freq_back = {}
max_double_words_freq_front = {}

for i in double_words_freq:
    for e in double_word_back:
        if i == e:
            max_double_words_freq_back[e] = double_words_freq[i]

for i in double_words_freq:
    for e in double_word_front:
        if i == e:
            max_double_words_freq_front[e] = double_words_freq[i]


for i in index:
    if index[i] == 0:
        if max_double_words_freq_front != {}:
            for e in max_double_words_freq_front:
                tekst_list[0] = max(max_double_words_freq_front, key=max_double_words_freq_front.get).split()[0]
        else:
            tekst_list[0] = min(lev, key=lev.get)

    elif index[i] == len(tekst_list)-1:
        if max_double_words_freq_back != {}:
            for e in max_double_words_freq_back:
                tekst_list[len(tekst_list)-1] = max(max_double_words_freq_back, key=max_double_words_freq_back.get).split()[1]
        else:
            tekst_list[len(tekst_list)-1] = min(lev, key=lev.get)

    else:
        if max_double_words_freq_front != {} and max_double_words_freq_back != {} and max_double_words_freq_front[max(max_double_words_freq_front, key=max_double_words_freq_front.get)] > max_double_words_freq_back[max(max_double_words_freq_back, key=max_double_words_freq_back.get)] or max_double_words_freq_back == {} and max_double_words_freq_front != {}:
            tekst_list[index[i]] =  max(max_double_words_freq_front, key=max_double_words_freq_front.get).split()[0]
        elif max_double_words_freq_front != {} and max_double_words_freq_back != {} and max_double_words_freq_back[max(max_double_words_freq_back, key=max_double_words_freq_back.get)] > max_double_words_freq_front[max(max_double_words_freq_front, key=max_double_words_freq_front.get)] or max_double_words_freq_front == {} and max_double_words_freq_back != {}:
            tekst_list[index[i]] = max(max_double_words_freq_back, key=max_double_words_freq_back.get).split()[1]
        else:
            tekst_list[index[i]] = min(lev, key=lev.get)
poprawny = ''
for i in tekst_list:
    poprawny += i + ' '
print(poprawny)