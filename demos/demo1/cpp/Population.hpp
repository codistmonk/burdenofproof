#ifndef POPULATION_HPP
#define POPULATION_HPP

#include <set>

#include "Character.hpp"

class Population
{
public:
    Population();
private:
    std::set<Character> m_population;
};

#endif // POPULATION_HPP
