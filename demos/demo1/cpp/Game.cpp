// NOLINT(legal/copyright)
#include "Game.hpp"
#include <boost/python.hpp>

namespace burdenofproof {

Game::Game(int const seed): m_time(0LL), m_population() {}

void Game::update(int64_t const milliseconds) {
    m_time += milliseconds;

    // TODO(?) update population
}

using boost::python::class_;
using boost::python::self;
using boost::python::return_internal_reference;

BOOST_PYTHON_MODULE(bop) {
    class_<CityBlueprint>("CityBlueprint")
            .def("getCell", &CityBlueprint::getCell)
            .def(boost::python::self_ns::str(self));
    class_<Game, boost::noncopyable>("Game")
            .def("getTime", &Game::getTime)
            .def("update", &Game::update)
            .def("getCityBlueprint",
                &Game::getCityBlueprint,
                return_internal_reference<1>());
}

}  // namespace burdenofproof
