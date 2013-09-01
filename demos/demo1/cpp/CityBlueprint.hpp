// NOLINT(legal/copyright)
#ifndef CITYBLUEPRINT_HPP_
#define CITYBLUEPRINT_HPP_

#include <cstdint>
#include <vector>
#include <string>
#include <ostream>  // NOLINT(readability/streams)

std::string const BLUEPRINTPATH = "models/cityblueprint.txt";

namespace burdenofproof {

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

    inline int getSizeNS() const {
        return m_sizeNS;
    }

    inline int getSizeWE() const {
        return m_sizeWE;
    }

    inline CityCell getCell(int const nsIndex, int const weIndex) const {
        return m_cityCells[nsIndex][weIndex];
    }

    friend std::ostream& operator<<(std::ostream & os, CityBlueprint const & p);

    inline CityCell operator()(int const i, int const j) const {
        return m_cityCells[i][j];
    }

 private:
    BluePrint m_blueprint;

    CityCells m_cityCells;

    int m_sizeWE;

    int m_sizeNS;
};

}  // namespace burdenofproof

#endif  // CITYBLUEPRINT_HPP_
