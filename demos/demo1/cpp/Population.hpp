#ifndef POPULATION_HPP
#define POPULATION_HPP

#include <set>
#include "Character.hpp"

class Population
{
public:
    Population();
private:
    void addDemo1Population();
    std::set<Character> m_population;
};

#endif // POPULATION_HPP