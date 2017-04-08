// compile with: g++ -std=c++11 find_duplicates.cpp 

#include <iostream>
#include <fstream>
#include <map>
#include <utility>
#include <cmath>

using namespace std;

int main(int argc, const char *argv[])
{

   map<unsigned long long, pair<unsigned long long,unsigned long long> > collisions;
   if (argc < 3) {
      cerr << "Usage: " << argv[0] << "<filename1> <filename2>\n";
      return 1;
   }
   ifstream in(argv[1], ios::binary);
   unsigned long long old_l;
   in.read(reinterpret_cast<char*>(&old_l), sizeof old_l);
   while (in) {
      unsigned long long l;
      in.read(reinterpret_cast<char*>(&l), sizeof l);
      if (in) {
         //cout << "Read a " << l << "\n";
         if (old_l == l) {
            collisions.insert(make_pair(l, make_pair(-1, -1)));
            cout << "Found collision " << l << endl;
         }
      }
      old_l = l;
   }
   in.close();
   cout << "Nr collisions = " << collisions.size() << endl;

   ifstream in2(argv[1], ios::binary);
   unsigned long long index = 0;
   while (in2) {
      unsigned long long l;
      in2.read(reinterpret_cast<char*>(&l), sizeof l);
      if (in2) {
         // cout << "Read a " << l << "\n";
         if (collisions.find(l) != collisions.end()) {
            auto p = collisions.at(l);
            if (p.first == 18446744073709551615)
               p.first = index;
            else if (p.second == 18446744073709551615)
               p.second = index;
            collisions[l] = p;
            cout << "updated " << l << " locations: " << p.first << " " << p.second << endl;
         }
      }
      index++;
   }
   in2.close();

   for (auto it = collisions.begin(); it != collisions.end(); it++) {
      cout << "Collision value: " << it->first << " locations: " << it->second.first << " - " << it->second.second << endl;
   }

   return 0;
}
