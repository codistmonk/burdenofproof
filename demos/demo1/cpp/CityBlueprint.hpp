// NOLINT(legal/copyright)
#ifndef CITYBLUEPRINT_HPP_
#define CITYBLUEPRINT_HPP_

#include <cstdint>
#include <vector>
#include <string>
#include <ostream>  // NOLINT(readability/streams)

#define BLUEPRINTPATH "../../../city/blueprint.txt"

enum class CityCell : int8_t {
    GROUND,
    ROAD,
    HOUSE,
    POLICE_BUILDING,
    OFFICE_BUILDING
};

class CityBlueprint {
    typedef std::vector< std::string > BluePrint;

    typedef std::vector< std::vector< CityCell > > CityCells;

 public:
    explicit CityBlueprint(std::string const & path = BLUEPRINTPATH);

    inline char getCell(int const line, int const row) const {
        return m_blueprint[line][row];
    }

    friend std::ostream& operator<<(std::ostream &os, CityBlueprint const & p);

    inline CityCell operator()(int const i, int const j) const {
        return m_cityCells[i][j];
    }

 private:
    BluePrint m_blueprint;

    CityCells m_cityCells;

    int m_sizeWE;

    int m_sizeNS;
};

#endif  // CITYBLUEPRINT_HPP_
