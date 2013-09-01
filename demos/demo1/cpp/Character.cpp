// NOLINT(legal/copyright)
#include "Character.hpp"

Character::Character() {
    m_id = Character::m_counter++;
}

int Character::m_counter = 0;
