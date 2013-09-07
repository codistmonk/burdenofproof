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

Persona::Persona(Character const * character) : m_character(character) {}

void Persona::buildFromStringVector(
        std::vector<std::string> const & voc) {
    using std::string;
    assert(voc.size() == 8);
    m_firstName = PiecewiseConstantChronology< string >(voc[0]);
    m_middleName = PiecewiseConstantChronology< string >(voc[1]);
    m_lastName = PiecewiseConstantChronology< string >(voc[2]);
    m_birthDay = PiecewiseConstantChronology< Time >(voc[3]);
    m_deathDay = PiecewiseConstantChronology< Time >(voc[4]);
    m_gender = PiecewiseConstantChronology< Gender >(voc[5]);
    m_murderousInstinct = PiecewiseLinearChronology< float >(voc[6]);
    m_position = PiecewiseLinearChronology< maths::vec3f >(voc[7]);
}

std::ostream &operator<<(std::ostream &o, const Persona &p) {
    o << "*** Persona Beginning ***" << std::endl;
    o << "First Name : " << p.getFirstName() << std::endl;
    o << "Middle Name : " << p.getMiddleName() << std::endl;
    o << "Last Name : " << p.getLastName() << std::endl;
    o << "Birth Day : " << p.getBirthDay() << std::endl;
    o << "Death Day : " << p.getBirthDay() << std::endl;
    o << "Gender : " << p.getGender() << std::endl;
    o << "Murderous Instinct : " << p.getMurderousInstinct() << std::endl;
    o << "Position : " << p.getPosition() << std::endl;
    o << "*** Persona Ending ***" << std::endl;
    return o;
}

void Persona::buildFromString(std::string const & str) {
    std::vector<std::string> strVec(8);
    split_regex(strVec, str, regex("###"));
    this->buildFromStringVector(strVec);
}

Persona::Persona(Persona const & p) : m_firstName(p.m_firstName),
    m_middleName(p.m_middleName),
    m_lastName(p.m_lastName),
    m_birthDay(p.m_birthDay),
    m_deathDay(p.m_deathDay),
    m_gender(p.m_gender),
    m_murderousInstinct(p.m_murderousInstinct),
    m_position(p.m_position),
    m_character(p.m_character) {}
