// NOLINT(legal/copyright)
#include "Character.hpp"
#include <cassert>
#include <vector>

int Character::m_counter = 0;

Character::Character()
    : m_personas(),
      m_actualPersona(nullptr),
      m_routinePersona(nullptr),
      m_id(Character::m_counter++) {}

std::vector<float> const & Character::getPosition(Time const & time) const {
    if (m_actualPersona != nullptr) {
        return m_actualPersona->getPosition().getValue(time).getData();
    } else {
        assert(m_routinePersona != nullptr);
        return m_routinePersona->getPosition().getValue(time).getData();
    }
}
