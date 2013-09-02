// NOLINT(legal/copyright)
#ifndef GAME_HPP_
#define GAME_HPP_

#include <thread>
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

    Time_Duration     m_time;

    CityBlueprint     m_cityBlueprint;

    Population        m_population;

    explicit Game(Game const &);

    Game & operator=(Game const&);

    std::thread       m_updateThread;

 public:
    // TODO(?) use seed
    Game(std::string const & scriptPath = ".", int const seed = 0);

    inline std::int64_t getTime() const {
        return m_time.ticks();
    }

    void update(const Time_Duration & duration);

    inline CityBlueprint const & getCityBlueprint() const {
        return m_cityBlueprint;
    }
};  // class Game

}  // namespace burdenofproof

#endif  // GAME_HPP_
