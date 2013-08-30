#include "CityBlueprint.hpp"

#include <fstream>
#include <algorithm>
#include <string>
#include <iostream>

#include "Utils.hpp"

using std::vector;
using std::string;

CityBlueprint::CityBlueprint(const std::string &path) : m_sizeWE(-1), m_sizeNS(-1)
{
    std::string line;
    std::ifstream blueprintFile(path,std::ios::in);
    if(blueprintFile.is_open()){
        while(blueprintFile >> line)
            m_blueprint.push_back(std::move(line)); //move may be dangerous

        auto compareFonction = [&](const std::string& s1, const std::string& s2) { return s1.size() < s2.size(); };

        std::vector<std::string>::const_iterator it = std::max_element(m_blueprint.cbegin(),
                                                                       m_blueprint.cend(),
                                                                       compareFonction
                                                                       );
        m_sizeWE = (*it).size();
        m_sizeNS = m_blueprint.size();

        for(int i = 0; i < m_blueprint.size();++i){
            int width = m_blueprint[i].size();
            m_cityCells.push_back(vector<CityCell>(width));
            for(int j = 0; j <  width;++j){
                switch(m_blueprint[i][j]){
                case '_' : {m_cityCells[i].push_back(CityCell::GROUND); break;}
                case 'H' : {m_cityCells[i].push_back(CityCell::HOUSE); break;}
                case 'S' : {m_cityCells[i].push_back(CityCell::ROAD); break;}
                case 'O' : {m_cityCells[i].push_back(CityCell::OFFICE_BUILDING); break;}
                case 'P' : {m_cityCells[i].push_back(CityCell::POLICE_BUILDING); break;}
                default  : {DEBUG; break;}
                }
            }
        }

    }

}

std::ostream & operator<<(std::ostream &os, const CityBlueprint &bp)
{
    for(auto& line: bp.m_blueprint)
        os << " | " <<line << " | "<< std::endl;
    return os;
}
