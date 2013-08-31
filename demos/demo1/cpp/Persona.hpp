#ifndef PERSONA_HPP
#define PERSONA_HPP

#include <cstdint>
#include <string>
#include <array>
#include "Propertychronology.hpp"
#include "Piecewiseconstantchronology.hpp"
#include "Piecewiselinearchronology.hpp"
#include "Maths.hpp"

enum class Gender : int8_t {MALE, FEMALE};

class Character;

class Persona
{
public:
    Persona(Character const& character);
    inline Character const&  getCharacter() const {return m_character;}
#ifndef _MSC_VER
    inline PropertyChronology<std::string> const & getFirstName() const {return m_firstName;}
    inline PropertyChronology<std::string> const & getMiddleName() const {return m_middleName;}
    inline PropertyChronology<std::string> const & getLastName() const {return m_lastName;}
    inline PropertyChronology<std::int64_t> const & getBirthDay() const {return m_birthDay;}
    inline PropertyChronology<std::int64_t> const & getDeathDay() const {return m_deathDay;}
    inline PropertyChronology<Gender> const & getGender() const {return m_gender;}
    inline PropertyChronology<float> const & getMurderousInstinct() const {return m_murderousInstinct;}
    inline PropertyChronology<maths::vec3f> const & getPosition() const {return m_position;}
#endif  // _MSC_VER
private:
#ifndef _MSC_VER
    PiecewiseConstantChronology<std::string> m_firstName;
    PiecewiseConstantChronology<std::string> m_middleName;
    PiecewiseConstantChronology<std::string> m_lastName;
    PiecewiseConstantChronology<std::int64_t> m_birthDay;
    PiecewiseConstantChronology<std::int64_t> m_deathDay;
    PiecewiseConstantChronology<Gender>       m_gender;
    PiecewiseLinearChronology<float>          m_murderousInstinct;
    PiecewiseLinearChronology<maths::vec3f>   m_position;
#endif  // _MSC_VER
    Character const& m_character;
};

#endif  // PERSONA_HPP
