// NOLINT(legal/copyright)
#include "Character.hpp"
#include <cassert>
#include <vector>

namespace burdenofproof {

int Character::m_counter = 0;

Character::Character()
    : m_actualPersona(nullptr),
      m_routinePersona(nullptr),
      m_id(Character::m_counter++) {
    m_actualPersona.reset(new Persona(this));
    m_routinePersona.reset(new RoutinePersona(this));
}

std::vector<float> const & Character::getPosition(Time const & time) const {
    if (m_actualPersona) {
        return m_actualPersona->getPosition().getValue(time).getData();
    } else {
        assert(m_routinePersona);
        return m_routinePersona->getPosition().getValue(time).getData();
    }
}

std::vector<float> const & Character::getHome(Time const & time) const {
    if (m_actualPersona) {
        return m_actualPersona->getHome().getValue(time).getData();
    } else {
        assert(m_routinePersona);
        return m_routinePersona->getHome().getValue(time).getData();
    }
}

std::vector<float> const & Character::getWorkPlace(Time const & time) const {
    if (m_actualPersona) {
        return m_actualPersona->getWorkPlace().getValue(time).getData();
    } else {
        assert(m_routinePersona);
        return m_routinePersona->getWorkPlace().getValue(time).getData();
    }
}
void Character::setHome(const Time &time,
                        const maths::Vec3f &pos) {
    if (m_actualPersona) {
        m_actualPersona->setHome(time, pos);
    } else {
        assert(m_routinePersona);
        m_routinePersona->setHome(time, pos);
    }
}

void Character::setPosition(const Time &time,
                            const maths::Vec3f &pos) {
    if (m_actualPersona) {
        m_actualPersona->setPosition(time, pos);
    } else {
        assert(m_routinePersona);
        m_routinePersona->setPosition(time, pos);
    }
}

Character::~Character() {
}

}  // namespace burdenofproof
