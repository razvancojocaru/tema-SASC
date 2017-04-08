# tema-SASC

## Setup

1. Instal boost libs
  sudo apt-get install libboost-all-dev
  
2. Use additional repo for external-sort
  https://github.com/alveko/external_sort
  
3. Example to generate random data (1GB) and sort with external-sort:
  ./external_sort --act all --msize 100 --munit M --log 6 --tmpdir ./tmp --gen.ofile my_generated --gen.fsize 1024 --gen.blocks 2
  
4. Run on actual data and find collisions and their indexes in the original data:
  ./find_collisions data.sorted data
