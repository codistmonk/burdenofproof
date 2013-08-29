#include "CityBlueprint.hpp"

#include <fstream>
#include <algorithm>
#include <string>
#include <iostream>

#include "Utils.hpp"

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
    }

}

std::ostream & operator<<(std::ostream &os, const CityBlueprint &bp)
{
    for(auto& line: bp.m_blueprint)
        os << " | " <<line << " | "<< std::endl;
    return os;
}
