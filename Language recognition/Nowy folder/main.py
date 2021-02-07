from collections import Counter
import math
import re

# Tworzenie listy frekwencyjnej unigramów oraz digramów tekstu porównywalnego
def n_gram(filepath):

    txt = open(filepath, 'r', encoding='utf-8')
    x = txt.read().lower()
    words = re.split(r'\W+', x)

    unigramy = []
    digramy = []

    for word in words:
        for letters in word:
            unigramy.append(letters)

    n = -1
    k = 0

    for letters in unigramy:
        if k != len(unigramy) - 1:
            digramy.append((str(unigramy[n + 1]) + str(unigramy[k + 1])))
            n += 1
            k += 1

    cnt = Counter()
    for word in digramy:
        cnt[word] += 1

    return dict(cnt)

# Definicje metryk

def euklides(a, b):
    wynik = 0
    lista = []
    for i in set(list(a.keys()) + list(b.keys())):
        if i in a and i in b:  # w obu
            wynik += (a[i] - b[i]) ** 2
        elif i in a:  # w A
            wynik += a[i] ** 2
        elif i in b:  # w B
            wynik += (0 - b[i]) ** 2
        else:
            pass

    return math.sqrt(wynik)
def taksowkowa(a,b):
    wynik = 0
    for i in set(list(a.keys())+list(b.keys())):
        if i in a and i in b:
         wynik += abs(a[i] - b[i])
        elif i in a:
            wynik+= abs(a[i])
        elif i in b:
            wynik+= abs(b[i])
        else:
            pass

    return wynik

def maksimum(a,b):
    wynik = []
    for i in set(list(a.keys())+list(b.keys())):
        if i in a and i in b:
            wynik.append(abs(a[i] - b[i]))
        elif i in a:
            wynik.append(abs(a[i]))
        elif i in b:
            wynik.append(abs(b[i]))
        else:
            pass

    return max(wynik)

def cos(a,b):

    suma = 0
    mianownika = 0
    mianownikb = 0

    for i in set(list(a.keys())+list(b.keys())):
        if i in a and i in b:
         suma += a[i] * b[i]
        else:
            suma += 0

    for i in a:
        mianownika += a[i]**2
    for i in b:
        mianownikb += b[i]**2

    mianownik = math.sqrt(mianownika)*math.sqrt(mianownikb)
    return 1 - suma/mianownik

# Tworzenie słowników zawierających nazwy plików przetwarzanych

g = {}
dir = []
for i in range(1,5):
    dir.append('eng'+str(i)+'.txt')
    dir.append('ger' + str(i) + '.txt')
for i in range(1,4):
    dir.append('pol' + str(i) + '.txt')
for i in range(1,3):
    dir.append('spa' + str(i) + '.txt')
    dir.append('ita' + str(i) + '.txt')
    dir.append('fin' + str(i) + '.txt')

#Tworzenie słowników z unigramami oraz digramami języków z którymi będzie porównywalny tekst

for plik in dir:
   j = plik[0:3]
   n = n_gram(plik)
   if j not in g:
       g[j] = n
   else:
    for klucz in n:
        if klucz in g[j]:
            g[j][klucz] += n[klucz]
        else:
            g[j][klucz] = n[klucz]


t = n_gram('por.txt')

# Wyświetlanie wyników odgległości między tekstem porównywanym oraz tekstami bazowymi

for i in g:
    print(i)
    print("Euklidesowa", euklides(t, g[i]))
    print("Taksowkowa", taksowkowa(t, g[i]))
    print("Maksimum", maksimum(t, g[i]))
    print("Cosinusowa",cos(t, g[i]))

#Najnmniejsze wartości odległości oznaczają że tekst porównywalny jest w danym języku. W tym przypadku jest to język Polski