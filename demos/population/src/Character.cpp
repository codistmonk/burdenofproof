#include <Character.hpp>

unsigned int Character::m_counter{0u};

Character::Character() : m_idNumber{m_counter++}
{

}

Persona::Persona(Persona_Type pt) : m_personaType{pt}
{

}
