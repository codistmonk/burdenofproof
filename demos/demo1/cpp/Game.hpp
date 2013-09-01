// NOLINT(legal/copyright)
#ifndef GAME_HPP_
#define GAME_HPP_

#include <cstdint>
#include <string>
#include <iostream>  // NOLINT(readability/streams)

#include "Maths.hpp"
#include "CityBlueprint.hpp"
#include "Population.hpp"

namespace burdenofproof {

class Game {
 private:
    std::string const m_scriptPath;

    int64_t           m_time;

    CityBlueprint     m_cityBlueprint;

    Population        m_population;

    explicit Game(Game const &);

    Game & operator=(Game const&);

 public:
    // TODO(?) use seed
    Game(std::string const & scriptPath = ".", int const seed = 0);

    inline int64_t getTime() const {
        return m_time;
    }

    void update(int64_t const milliseconds);

    inline CityBlueprint const & getCityBlueprint() const {
        return m_cityBlueprint;
    }
};  // class Game

}  // namespace burdenofproof

#endif  // GAME_HPP_
