// NOLINT(legal/copyright)
#ifndef POPULATION_HPP_
#define POPULATION_HPP_

#include <cassert>
#include <set>
#include "CityBlueprint.hpp"
#include "Character.hpp"

namespace burdenofproof {

class Population {
 public:
    Population();
    explicit Population(CityBlueprint const & cbp);
    inline int getCharacterCount() const { return m_population.size(); }
    Character const & getCharacter(int id) const;

 private:
    void addDemo1Population(CityBlueprint const & demoBp);
    void addCharachter();
    std::set< Character, CharacterComparator > m_population;
};

}  // namespace burdenofproof

#endif  // POPULATION_HPP_
