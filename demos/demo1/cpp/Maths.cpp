#include <ctime>
#include <fstream>
#include <iostream>

#include "Maths.hpp"

using namespace maths;

int seed()
{
    int random_seed_a, random_seed_b;
    std::ifstream file("/dev/random", std::ios::binary);
    if(file.is_open())
    {   char* memblock;
        int size_i = sizeof(int);
        memblock = new char[size_i];
        file.read(memblock,size_i);
        file.close();
        random_seed_a = *reinterpret_cast<int*>(memblock);
        delete[] memblock;
    }
    else
        random_seed_a = 0;

    random_seed_b = std::time(nullptr);
    return (random_seed_a ^ random_seed_b);
}
