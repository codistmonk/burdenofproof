#ifndef PERSONA_HPP
#define PERSONA_HPP

#include <cstdint>

#include "Propertychronology.hpp"

enum class Gender : int8_t {MALE, FEMALE};

class Character;

class Persona
{
public:
    Persona();
    Character const&  getCharacter() const {return *m_character;}
private:
    Character* m_character;
};

#endif // PERSONA_HPP
