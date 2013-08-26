#include "Game.hpp"
#include <boost/python.hpp>

using namespace boost::python;

BOOST_PYTHON_MODULE(bop)
{
    class_<Game>("Game")
        .def("printText", &Game::printText)
        .def("setText", &Game::setText)
    ;
}
