// NOLINT(legal/copyright)
#ifndef POPULATION_HPP_
#define POPULATION_HPP_

#include <cassert>
#include <set>
#include "Character.hpp"

class Population {
 public:
    Population();

    inline int getCharacterCount() const { return m_population.size(); }
    Character const & getCharacter(int id) const;

 private:
    void addDemo1Population();

    std::set< Character, CharacterComparator > m_population;
};

#endif  // POPULATION_HPP_
