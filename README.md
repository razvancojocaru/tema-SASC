# tema-SASC

## Descriere generala
Attack on 64-bit block size ciphers: https://sweet32.info/

## Descrierea proiectului:
```browser.py```
Acest fisier cripteaza un request HTTP de foarte multe ori, generand o cantitate mare (~35GB) de ciphertext. Cifrul folosit este 3DES, modul este CBC cu random IV.

Cum sa iti generezi singur datele (dureaza aproximativ 2h):

python browser.py file_1.out

python browser.py file_2.out

python browser.py file_3.out

python browser.py file_4.out

cat file_1.out file_2.out file_3.out file_4.out > total.out

## Sortarea blocurilor de ciphertext (timpul de sortare ar trebui sa fie intre 30min si 2h maxim)

1. Instal boost libs
  ```
  sudo apt-get install libboost-all-dev
  ```
  
2. Use additional repo for external-sort (git clone in folderul tema-SASC)
  https://github.com/alveko/external_sort
  
3. prepare external sort
```
  cd external_sort/examples
  make
```

4. Sort the actual data (fisierul trebuie sa se numeasca total.out si sa fie in folderul tema-SASC, comanda rulata din folderul examples):

```
 mkdir tmp && ./external_sort --act srt --msize 512 --munit M --log 6 --tmpdir ./tmp --srt.ifile ../../total.out --spl.blocks 2 
```

## Gasirea coliziunilor in datele sortate (aprox. 30 minute)

Run on actual data and find collisions and their indexes in the original data:

```
g++ -std=c++11 find_duplicates.cpp 
./find_collisions total.out.sorted total.out
```

Exemplu de output:
```
Found collision 735174213495964967
Found collision 1247948159810218381
Found collision 6810904725035589557
Found collision 7704228482905844942
Found collision 13709301323247256842
Nr collisions = 5
updated 735174213495964967 locations: 122347852 18446744073709551615
updated 13709301323247256842 locations: 122347853 18446744073709551615
updated 1247948159810218381 locations: 122347854 18446744073709551615
updated 7704228482905844942 locations: 122347855 18446744073709551615
updated 735174213495964967 locations: 122347852 893212236
updated 13709301323247256842 locations: 122347853 893212237
updated 1247948159810218381 locations: 122347854 893212238
updated 7704228482905844942 locations: 122347855 893212239
updated 6810904725035589557 locations: 1064792912 18446744073709551615
updated 6810904725035589557 locations: 1064792912 3260804768
Collision value: 735174213495964967 locations: 122347852 - 893212236
Collision value: 1247948159810218381 locations: 122347854 - 893212238
Collision value: 6810904725035589557 locations: 1064792912 - 3260804768
Collision value: 7704228482905844942 locations: 122347855 - 893212239
Collision value: 13709301323247256842 locations: 122347853 - 893212237

```

## Recuperarea cookie-ului secret folosind coliziunile

Codul se afla in fisierul recover_plaintext.py

Coliziunile gasite in sectiunea anterioara trebuie puse in fisier, variabila collisions

Example output:

```
useful collision
found secret cookie: ABCDEFGH
useful collision
found secret cookie: ABCDEFGH
```

## Update-ul nostru

In fisierul browser_updated.py se afla scriptul care genereaza ciphertext.

De data aceasta, clientul va randomiza de fiecare data headerele HTTP inainte de a cripta.

Scriptul se ruleaza la fel ca cel de la pasul anterior.

## Misiunea voastra

1. Folositi scriptul browser_updated.py pentru a generate o cantitate necesara de ciphertext (cat doriti voi).

2. Incercati sa recuperati COOKIE folosind doar acest ciphetext. NU folositi variabila 'cookie' setata in fisier. NU folositi cheia secreta de criptare.
