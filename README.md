# tema-SASC

## Setup

1. Instal boost libs
  ```
  sudo apt-get install libboost-all-dev
  ```
  
2. Use additional repo for external-sort (git clone in folderul SASC)
  https://github.com/alveko/external_sort
  
3. prepare external sort
```
  cd external_sort/examples
  make
```
4. Sort the actual data (fisierul trebuie sa se numeasca total.out si sa fie in folderul SASC, comanda rulata din folderul examples):
```
 mkdir tmp && ./external_sort --act srt --msize 512 --munit M --log 6 --tmpdir ./tmp --srt.ifile ../../total.out --spl.blocks 2 
```
  
5. Run on actual data and find collisions and their indexes in the original data:
```
  ./find_collisions data.sorted data
  ```
