// NOLINT(legal/copyright)
#ifndef PERSONA_HPP_
#define PERSONA_HPP_
#include <boost/filesystem.hpp>
#include <boost/date_time/posix_time/ptime.hpp>
#include <cstdint>
#include <memory>
#include <cassert>
#include <vector>
#include <string>
#include "Propertychronology.hpp"
#include "Piecewiseconstantchronology.hpp"
#include "Piecewiselinearchronology.hpp"
#include "Gender.hpp"
#include "Maths.hpp"



namespace burdenofproof {

    class Character;

class Persona {
 public:
    explicit Persona(Character const * character);

    explicit Persona(Persona const &);

    inline Character const &  getCharacter() const {
        assert(m_character != nullptr);
        return *m_character;
    }

    inline PropertyChronology< maths::Vec3f > const & getPosition() const {
        assert(m_position);
        return *m_position;
    }

    inline PropertyChronology< maths::Vec3f > const & getHome() const {
        assert(m_home);
        return *m_home;
    }

    inline PropertyChronology< maths::Vec3f > const & getWorkPlace() const {
        assert(m_workPlace);
        return *m_workPlace;
    }

    void setHome(const Time &time,
                    const maths::Vec3f &pos);

    void setPosition(const Time &time,
                     const maths::Vec3f &pos);

    void setWorkPlace(const Time &time,
                     const maths::Vec3f &pos);

 private:
    Persona();
    friend std::ostream & operator<<(std::ostream & o, Persona const & p);

 protected:
    std::shared_ptr< PropertyChronology< maths::Vec3f > >   m_position;
    std::shared_ptr< PropertyChronology< maths::Vec3f > >   m_home;
    std::shared_ptr< PropertyChronology< maths::Vec3f > >   m_workPlace;
    Character const * m_character;
};

class RoutinePersona : public Persona {
    typedef Persona Super;
 public:
    explicit RoutinePersona(Character const * character)
        : Super(character) {
        m_position.reset(
                    new PeriodicPiecewiseLinearChronology< maths::Vec3f >());
    }
};

}  // namespace burdenofproof
#endif  // PERSONA_HPP_
