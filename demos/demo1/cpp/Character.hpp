#ifndef CHARACTER_HPP
#define CHARACTER_HPP

#include <list>

#include "Persona.hpp"

class Character
{
public:
    Character();
    inline int getId() const {return m_id;}
    inline Persona const & getActuelPersona() const { return *m_actualPersona;}
    inline Persona const & getRoutinePersona() const { return *m_routinePersona;}
private:
    std::list<Persona> m_personas;
    Persona*           m_actualPersona;
    Persona*            m_routinePersona;
    static int m_counter;
    int m_id;
};

#endif // CHARACTER_HPP
