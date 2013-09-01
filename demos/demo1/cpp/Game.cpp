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
using boost::python::enum_;
using boost::python::self;
using boost::python::return_internal_reference;

BOOST_PYTHON_MODULE(bop) {
    enum_<CityCell>("CityCell")
            .value("GROUND", CityCell::GROUND)
            .value("ROAD", CityCell::ROAD)
            .value("HOUSE", CityCell::HOUSE)
            .value("POLICE_BUILDING", CityCell::POLICE_BUILDING)
            .value("OFFICE_BUILDING", CityCell::OFFICE_BUILDING);
    class_<CityBlueprint>("CityBlueprint")
            .def("getSizeNS", &CityBlueprint::getSizeNS)
            .def("getSizeWE", &CityBlueprint::getSizeWE)
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
