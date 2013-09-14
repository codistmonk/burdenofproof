// NOLINT(legal/copyright)
#include "Hello.hpp"
#include <boost/python.hpp>
#include <iostream>  // NOLINT(readability/streams)

namespace bop {

Hello::Hello() {
    std::cout << "Burden of Proof demo1b" << std::endl;
}

using boost::python::class_;
using boost::python::init;

BOOST_PYTHON_MODULE(bop) {
    class_< Hello >("Hello")
        .def(init<>());
}

}  // namespace bop
