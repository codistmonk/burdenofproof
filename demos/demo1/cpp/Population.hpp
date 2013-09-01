// NOLINT(legal/copyright)
#ifndef POPULATION_HPP_
#define POPULATION_HPP_

#include <set>
#include "Character.hpp"

class Population {
 public:
    Population();

 private:
    void addDemo1Population();

    std::set< Character > m_population;
};

#endif  // POPULATION_HPP_
