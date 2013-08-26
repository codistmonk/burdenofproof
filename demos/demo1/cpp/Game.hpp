#ifndef GAME_HPP
#define GAME_HPP

#include <string>
#include <iostream>

class Game
{

private:

	std::string text;

public:

	void printText()
	{
		std::cout << this->text << std::endl;
	}

	void setText(std::string const & text)
	{
		this->text = text;
	}

};

#endif
