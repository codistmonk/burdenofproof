// NOLINT(legal/copyright)
#include "Population.hpp"
#include "Temporalvalue.hpp"
namespace burdenofproof {

    Population::Population() {}

    Population::Population(CityBlueprint const & cbp) {
        this->addDemo1Population(cbp);
    }

void Population::addDemo1Population(CityBlueprint const & demoBp) {
    const auto & cells = demoBp.getCityCells();
    for (unsigned int i = 0 ; i < cells.size(); ++i) {
        for (unsigned int j = 0 ; j < cells[i].size(); ++j) {
            if (cells[i][j] == CityCell::HOUSE) {  // add a citizen
                Character newChar;
                newChar.setHome(MIN_TIME,
                                maths::Vec3f(i, j, 0.0f));
                newChar.setPosition(MIN_TIME,
                                    maths::Vec3f(i, j, 0.0f));
                m_population.insert(newChar);
            }
        }
    }
}

Character const & Population::getCharacter(int id) const {
    // Not using the default constructor, this is a fictive character used to speed-up this method NOLINT(whitespace/line_length)
    static Character c(0);

    c.setId(id);
    assert(m_population.count(c) != 0);
    return *m_population.find(c);
}

void Population::addCharachter() {
    m_population.insert(Character());
    std::cout << "added one citizen. Total number of citizens :"
              << this->getCharacterCount() << std::endl;
}

}  // namespace burdenofproof
