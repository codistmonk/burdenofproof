#ifndef CITYBLUEPRINT_HPP
#define CITYBLUEPRINT_HPP

#include <vector>
#include <string>
#include <ostream>
#include <cstdint>

#define BLUEPRINTPATH "../../../city/blueprint.txt"

enum class CityCell : int8_t {GROUND, ROAD,HOUSE,POLICE_BUILDING, OFFICE_BUILDING};


class CityBlueprint
{
    typedef std::vector<std::string> BluePrint;
    typedef std::vector<std::vector<CityCell> > CityCells;
public:
    CityBlueprint(const std::string& path = BLUEPRINTPATH);
    inline char getCell(int line, int row) const {return m_blueprint[line][row];}
    friend std::ostream& operator<<(std::ostream &os, const CityBlueprint& p);
    inline CityCell operator()(int i, int j) const {return m_cityCells[i][j];}
private:
    BluePrint m_blueprint;
    CityCells m_cityCells;
    int m_sizeWE;
    int m_sizeNS;
};

#endif // CITYBLUEPRINT_H
