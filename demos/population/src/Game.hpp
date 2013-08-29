#ifndef GAME_HPP
#define GAME_HPP
#include "CityBlueprint.hpp"
#include "Maths.hpp"

class Game
{
public:
    Game(int seed = maths::seed());
    inline const CityBlueprint& getCityBlueprint() const {return m_cityBlueprint;}

private:
    CityBlueprint m_cityBlueprint   ;

};

#endif // GAME_HPP
