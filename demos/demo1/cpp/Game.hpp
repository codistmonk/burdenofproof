#ifndef GAME_HPP
#define GAME_HPP

#include <string>
#include <iostream>
#include <cstdint>

#include "Maths.hpp"
#include "CityBlueprint.hpp"

namespace burdenofproof
{

class Game
{

private:

	int64_t time;
	CityBlueprint m_cityBlueprint   ;

public:

	Game(int seed = 0);

	int64_t getTime() const;

	void update(int64_t const milliseconds);
    inline const CityBlueprint& getCityBlueprint() const {return m_cityBlueprint;}
}; // class Game

} // namespace burdenofproof

#endif
