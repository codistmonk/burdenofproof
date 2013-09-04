// NOLINT(legal/copyright)
#include "Population.hpp"

Population::Population() {}

Character const & Population::getCharacter(int id) const {
    // Not using the default constructor, this is a fictive character used to speed-up this method NOLINT(whitespace/line_length)
    static Character c(0);

    c.setId(id);
    assert(m_population.count(c) != 0);
    return *m_population.find(c);
}
