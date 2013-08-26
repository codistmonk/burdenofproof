#ifndef GAME_HPP
#define GAME_HPP

#include <string>
#include <iostream>
#include <cstdint>

namespace burdenofproof
{

class Game
{

private:

	int64_t time;

public:

	Game();

	int64_t getTime() const;

	void update(int64_t const milliseconds);

}; // class Game

} // namespace burdenofproof

#endif
