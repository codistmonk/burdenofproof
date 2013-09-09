// NOLINT(legal/copyright)
#include "Persona.hpp"
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string_regex.hpp>
#include <boost/date_time/posix_time/ptime.hpp>
#include <cstdint>
#include <cassert>
#include <string>
#include <vector>

using boost::algorithm::split;
using boost::algorithm::is_any_of;
using boost::algorithm::split_regex;
using boost::regex;

namespace burdenofproof {

Persona::Persona(Character const * character)
    : m_position(nullptr),
      m_home(nullptr),
      m_character(character) {
    m_position.reset(
                new AbsolutePiecewiseLinearChronology< maths::Vec3f >());
    m_home.reset(
                new AbsolutePiecewiseConstantChronology< maths::Vec3f >());
    m_workPlace.reset(
                new AbsolutePiecewiseConstantChronology< maths::Vec3f >());
}

void Persona::setHome(const Time &time, const maths::Vec3f &pos) {
    if (m_home)
         m_home->addValue(time, pos);
}

void Persona::setPosition(const Time &time, const maths::Vec3f &pos) {
    if (m_position)
         m_position->addValue(time, pos);
}

void Persona::setWorkPlace(const Time &time, const maths::Vec3f &pos) {
    if (m_workPlace)
        m_workPlace->addValue(time, pos);
}

std::ostream &operator<<(std::ostream &o, const Persona &p) {
    return o;
}

Persona::Persona(Persona const & p)
    : m_position(p.m_position),
      m_home(p.m_home),
      m_character(p.m_character) {}

}  // namespace burdenofproof
