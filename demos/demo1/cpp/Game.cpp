#include "Game.hpp"
#include <boost/python.hpp>

using namespace boost::python;

namespace burdenofproof
    {

    Game::Game(int seed): time(0LL), m_population() {}

    int64_t Game::getTime() const
    {
        return this->time;
    }

    void Game::update(int64_t const milliseconds)
    {
        this->time += milliseconds;
    }

    BOOST_PYTHON_MODULE(bop)
    {
        class_<CityBlueprint>("CityBlueprint")
                .def("getCell", &CityBlueprint::getCell)
                .def(self_ns::str(self))
                ;
        class_<Game, boost::noncopyable>("Game")
                .def("getTime", &Game::getTime)
                .def("update", &Game::update)
                .def("getCityBlueprint", &Game::getCityBlueprint, return_internal_reference<1>())
                ;

    }

    } // namespace burdenofproof
