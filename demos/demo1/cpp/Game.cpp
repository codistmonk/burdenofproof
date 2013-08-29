#include "Game.hpp"
#ifdef __APPLE__
#undef _GLIBCXX_USE_INT128
#endif
#include <boost/python.hpp>

using namespace boost::python;

namespace burdenofproof
{

Game::Game(int seed): time(0LL) {}

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
    class_<Game>("Game")
        .def("getTime", &Game::getTime)
        .def("update", &Game::update)
    ;
}

} // namespace burdenofproof
