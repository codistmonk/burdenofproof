// NOLINT(legal/copyright)
#include "Game.hpp"
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/filesystem.hpp>
#include <boost/python.hpp>
#include <string>

using boost::posix_time::ptime;
using boost::posix_time::time_duration;
using boost::posix_time::milliseconds;
using boost::filesystem::path;
using boost::posix_time::from_iso_string;
using std::string;
using maths::vec3f;

namespace burdenofproof {

static std::string pathJoin(std::string const & path1,
    std::string const & path2) {
    return path1.size() == 0 ? path2 : path1 + "/" + path2;
}

Game::Game(std::string const & scriptPath, int const seed)
    : m_scriptPath(scriptPath),
      m_time(),
      m_cityBlueprint(pathJoin(scriptPath, BLUEPRINTPATH)),
      m_population() {
//            m_updateThread = std::thread(&Game::update,
//                                         this,
//                                         Time_Duration(milliseconds(100)));
    TemporalValue<string> tpStr(
        path(pathJoin(scriptPath, "temporalValues/string.txt")));
    SHOW(tpStr);
    TemporalValue<vec3f> tpVec3f(
        path(pathJoin(scriptPath, "temporalValues/vec3f.txt")));
    SHOW(tpVec3f);
    TemporalValue<Gender> tpG(
        path(pathJoin(scriptPath, "temporalValues/gender.txt")));
    SHOW(tpG);
    PiecewiseConstantChronology<string> pcStr(
        path(pathJoin(scriptPath, "propertyChronologies/strings.txt")));
    SHOW(pcStr);
    PiecewiseLinearChronology<float> pcFloats(
        path(pathJoin(scriptPath, "propertyChronologies/floats.txt")));
    SHOW(pcFloats);
    SHOW(std::to_string(pcFloats.getValue(
        ptime(from_iso_string("20120903T060000")))));
    Persona personaLambda(
                path(pathJoin(m_scriptPath, "personas/p1.txt")),
                nullptr);
    SHOW(personaLambda);
}

void Game::update(const Time_Duration & duration) {
    m_time += duration;

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
            .value("OFFICE_BUILDING", CityCell::OFFICE_BUILDING)
            ;  // NOLINT(whitespace/semicolon)

    class_<CityBlueprint>("CityBlueprint")
            .def("getSizeNS", &CityBlueprint::getSizeNS)
            .def("getSizeWE", &CityBlueprint::getSizeWE)
            .def("getCell", &CityBlueprint::getCell)
            .def(boost::python::self_ns::str(self))
            ;  // NOLINT(whitespace/semicolon)

    class_<Character>("Character")
            .def(init<>())
            .def("getRoutinePersona",
                 &Character::getRoutinePersona,
                 return_internal_reference<1>())
            .def("getActualPersona",
                 &Character::getActualPersona,
                 return_internal_reference<1>())
            ;  // NOLINT(whitespace/semicolon)

    class_<Persona>("Persona", init<Character*>())
            .def("getPosition",
                 &Persona::getPosition,
                 return_internal_reference<1>())
           ;  // NOLINT(whitespace/semicolon)

    class_<Population>("Population")
            .def(init<>())
            .def("getCharacterCount", &Population::getCharacterCount)
            .def("getCharacter",
                 &Population::getCharacter,
                 return_internal_reference<1>())
            ;  // NOLINT(whitespace/semicolon)

    class_<Game, boost::noncopyable>("Game")
            .def(init< std::string >())
            .def("getTime", &Game::getTime)
            .def("update", &Game::update)
            .def("getCityBlueprint",
                 &Game::getCityBlueprint,
                 return_internal_reference<1>())
            .def("getPopulation",
                 &Game::getPopulation,
                 return_internal_reference<1>())
            ;  // NOLINT(whitespace/semicolon)
}

}  // namespace burdenofproof
