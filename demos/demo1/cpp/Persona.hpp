// NOLINT(legal/copyright)
#ifndef PERSONA_HPP_
#define PERSONA_HPP_
#include <boost/filesystem.hpp>
#include <boost/date_time/posix_time/ptime.hpp>
#include <cstdint>
#include <cassert>
#include <vector>
#include <string>
#include "Propertychronology.hpp"
#include "Piecewiseconstantchronology.hpp"
#include "Piecewiselinearchronology.hpp"
#include "Maths.hpp"

class Character;

class Persona {
 public:
    explicit Persona(Character const * character);
    explicit Persona(boost::filesystem::path const & path,
                     Character const * character) :
        m_character(character) {
        this->buildFromString(utils::fileToStdString(path));
    }

    explicit Persona(std::string const & str,
                     Character const * character) :
        m_character(character) {
        this->buildFromString(str);
    }

    explicit Persona(Persona const &);
    inline Character const *  getCharacter() const {
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

    inline PropertyChronology< Time > const & getBirthDay() const {
        return m_birthDay;
    }

    inline PropertyChronology< Time > const & getDeathDay() const {
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
    Persona();
    void buildFromString(std::string const & str);
    void buildFromStringVector(std::vector<std::string> const & strVec);
    friend std::ostream & operator<<(std::ostream & o, Persona const & p);

 private:
    PiecewiseConstantChronology< std::string >  m_firstName;
    PiecewiseConstantChronology< std::string >  m_middleName;
    PiecewiseConstantChronology< std::string >  m_lastName;
    PiecewiseConstantChronology< Time > m_birthDay;
    PiecewiseConstantChronology< Time > m_deathDay;
    PiecewiseConstantChronology< Gender >       m_gender;
    PiecewiseLinearChronology< float >          m_murderousInstinct;
    PiecewiseLinearChronology< maths::vec3f >   m_position;
    Character const * m_character;
};

#endif  // PERSONA_HPP_
