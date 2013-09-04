// NOLINT(legal/copyright)
#include "Persona.hpp"

Persona::Persona(const Character *character) : m_character(character) {}

Persona::Persona(Persona const & p) : m_firstName(p.m_firstName),
    m_middleName(p.m_middleName),
    m_lastName(p.m_lastName),
    m_birthDay(p.m_birthDay),
    m_deathDay(p.m_deathDay),
    m_gender(p.m_gender),
    m_murderousInstinct(p.m_murderousInstinct),
    m_position(p.m_position),
    m_character(p.m_character) {}
