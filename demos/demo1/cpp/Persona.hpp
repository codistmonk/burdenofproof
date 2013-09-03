// NOLINT(legal/copyright)
#ifndef PERSONA_HPP_
#define PERSONA_HPP_

#include <cstdint>
#include <string>
#include "Propertychronology.hpp"
#include "Piecewiseconstantchronology.hpp"
#include "Piecewiselinearchronology.hpp"
#include "Maths.hpp"

class Character;

class Persona {
 public:
    explicit Persona(Character const & character);

    inline Character const &  getCharacter() const {
        return m_character;
    }

    inline PropertyChronology< std::string > const & getFirstName() const {
        return m_firstName;
    }

    inline PropertyChronology< std::string > const & getMiddleName() const {
        return m_middleName;
    }

    inline PropertyChronology< std::string > const & getLastName() const {
        return m_lastName;
    }

    inline PropertyChronology< std::int64_t > const & getBirthDay() const {
        return m_birthDay;
    }

    inline PropertyChronology< std::int64_t > const & getDeathDay() const {
        return m_deathDay;
    }

    inline PropertyChronology< Gender > const & getGender() const {
        return m_gender;
    }

    inline PropertyChronology< float > const & getMurderousInstinct() const {
        return m_murderousInstinct;
    }

    inline PropertyChronology< maths::vec3f > const & getPosition() const {
        return m_position;
    }

 private:
    PiecewiseConstantChronology< std::string >  m_firstName;
    PiecewiseConstantChronology< std::string >  m_middleName;
    PiecewiseConstantChronology< std::string >  m_lastName;
    PiecewiseConstantChronology< std::int64_t > m_birthDay;
    PiecewiseConstantChronology< std::int64_t > m_deathDay;
    PiecewiseConstantChronology< Gender >       m_gender;
    PiecewiseLinearChronology< float >          m_murderousInstinct;
    PiecewiseLinearChronology< maths::vec3f >   m_position;
    Character const & m_character;
};

#endif  // PERSONA_HPP_
