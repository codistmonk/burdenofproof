#ifndef CITYBLUEPRINT_HPP
#define CITYBLUEPRINT_HPP

#include <vector>
#include <string>
#include <ostream>


#define BLUEPRINTPATH "../../../city/blueprint.txt"

class CityBlueprint
{
    typedef std::vector<std::string> BluePrint;
public:
    CityBlueprint(const std::string& path = BLUEPRINTPATH);
    inline char getCell(int line, int row) const {return m_blueprint.at(line).at(row);}
    friend std::ostream& operator<<(std::ostream &os, const CityBlueprint& p);
private:
    BluePrint m_blueprint;
    int m_sizeWE;
    int m_sizeNS;
};

#endif // CITYBLUEPRINT_H
