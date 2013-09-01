// NOLINT(legal/copyright)
#ifndef GAME_HPP_
#define GAME_HPP_

#include <cstdint>
#include <string>
#include <iostream>

#include "Maths.hpp"
#include "CityBlueprint.hpp"
#include "Population.hpp"

namespace burdenofproof {

class Game {
 private:
    int64_t time;

    CityBlueprint m_cityBlueprint;

    Population    m_population;

    explicit Game(Game const &);

    Game& operator=(Game const&);

 public:
    explicit Game(int seed = 0);

    int64_t getTime() const;

    void update(int64_t const milliseconds);

    inline CityBlueprint const & getCityBlueprint() const {
        return m_cityBlueprint;
    }
};  // class Game

}  // namespace burdenofproof

#endif  // GAME_HPP_
