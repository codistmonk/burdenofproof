// NOLINT(legal/copyright)
#include "Game.hpp"
#include <boost/python.hpp>
#include <string>

namespace burdenofproof {

static std::string pathJoin(std::string const & path1,
    std::string const & path2) {
    return path1.size() == 0 ? path2 : path1 + "/" + path2;
}

Game::Game(std::string const & scriptPath, int const seed)
    : m_scriptPath(scriptPath), m_time(0LL),
      m_cityBlueprint(pathJoin(scriptPath, BLUEPRINTPATH)), m_population() {}

void Game::update(int64_t const milliseconds) {
    m_time += milliseconds;

    // TODO(?) update population
}

using boost::python::class_;
using boost::python::enum_;
using boost::python::self;
using boost::python::init;
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
            .def(init< std::string >())
            .def("getTime", &Game::getTime)
            .def("update", &Game::update)
            .def("getCityBlueprint",
                &Game::getCityBlueprint,
                return_internal_reference<1>());
}

}  // namespace burdenofproof
