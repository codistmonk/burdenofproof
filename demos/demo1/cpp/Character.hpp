// NOLINT(legal/copyright)
#ifndef CHARACTER_HPP_
#define CHARACTER_HPP_

#include <list>

#include "Persona.hpp"

class Character {
 public:
    Character();
    explicit Character(int id) : m_id(id),
                                 m_actualPersona(nullptr),
                                 m_routinePersona(nullptr) {}

    inline int getId() const {return m_id;}
    inline void setId(int n) {m_id = n;}
    inline Persona const & getActualPersona() const {
        return *m_actualPersona;
    }
    inline Persona const & getRoutinePersona() const {
        return *m_routinePersona;
    }

 private:
    std::list<Persona*>m_personas;
    Persona*           m_actualPersona;
    Persona*           m_routinePersona;
    static int m_counter;
    int m_id;
};

struct CharacterComparator {
    inline bool operator()(Character const & c1,
                           Character const & c2) const {
        return c1.getId() < c2.getId();
    }
};
#endif  // CHARACTER_HPP_
