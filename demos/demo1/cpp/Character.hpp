#ifndef CHARACTER_HPP
#define CHARACTER_HPP

#include <list>

#include "Persona.hpp"

class Character
{
public:
    Character();
    inline int getId() const {return m_id;}
#ifndef _MSC_VER
    inline Persona const & getActuelPersona() const { return *m_actualPersona;}
    inline Persona const & getRoutinePersona() const { return *m_routinePersona;}
#endif  // _MSC_VER
private:
#ifndef _MSC_VER
    std::list<Persona> m_personas;
    Persona*           m_actualPersona;
    Persona*           m_routinePersona;
#endif  // _MSC_VER
    static int m_counter;
    int m_id;
};

#endif // CHARACTER_HPP
