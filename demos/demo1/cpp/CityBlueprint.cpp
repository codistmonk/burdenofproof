// NOLINT(legal/copyright)
#include "CityBlueprint.hpp"

#include <fstream>  // NOLINT(readability/streams)
#include <algorithm>
#include <string>
#include <iostream>  // NOLINT(readability/streams)
#include <vector>

#include "Utils.hpp"

using std::vector;
using std::string;

namespace burdenofproof {

static CityCell cellFromChar(char const c) {
    switch (c) {
        case '_' : return CityCell::GROUND;
        case 'H' : return CityCell::HOUSE;
        case 'S' : return CityCell::ROAD;
        case 'O' : return CityCell::OFFICE_BUILDING;
        case 'P' : return CityCell::POLICE_BUILDING;
        default  : {
            DEBUG;
            return CityCell::GROUND;
        }
    }
}

CityBlueprint::CityBlueprint(std::string const & path)
        : m_sizeWE(-1), m_sizeNS(-1) {
    std::string line;
    std::ifstream blueprintFile(path, std::ios::in);

    if (blueprintFile.is_open()) {
        while (blueprintFile >> line) {
            m_blueprint.push_back(std::move(line));  // move may be dangerous
        }

        auto compareFonction = [&](
            std::string const & s1,
            std::string const & s2) {
            return s1.size() < s2.size();
        };

        std::vector<std::string>::const_iterator it = std::max_element(
            m_blueprint.cbegin(), m_blueprint.cend(), compareFonction);
        m_sizeWE = (*it).size();
        m_sizeNS = m_blueprint.size();

        for (auto & blueprintRow : m_blueprint) {
            vector< CityCell > cityRow;
            cityRow.reserve(blueprintRow.size());

            std::transform(blueprintRow.begin(), blueprintRow.end(),
                std::back_inserter(cityRow), cellFromChar);

            m_cityCells.push_back(cityRow);
        }
    }
}

std::ostream & operator<<(std::ostream & os, CityBlueprint const & bp) {
    for (auto & line : bp.m_blueprint) {
        os << " | " << line << " | "<< std::endl;
    }

    return os;
}

}  // namespace burdenofproof
