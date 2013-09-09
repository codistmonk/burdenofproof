// NOLINT(legal/copyright)
#ifndef CHARACTER_HPP_
#define CHARACTER_HPP_

#include <cassert>
#include <list>
#include <vector>
#include <memory>
#include "Persona.hpp"

namespace burdenofproof {

class Character {
 public:
    Character();
    explicit Character(int id) : m_actualPersona(nullptr),
                                 m_routinePersona(nullptr),
                                 m_id(id) {}

    inline int getId() const {return m_id;}

    inline void setId(int n) {m_id = n;}

    inline Persona const & getActualPersona() const {
        assert(m_actualPersona);
        return *m_actualPersona;
    }

    inline Persona const & getRoutinePersona() const {
        assert(m_routinePersona);
        return *m_routinePersona;
    }

    std::vector<float> const & getPosition(Time const & time) const;

    std::vector<float> const & getHome(Time const & time) const;

    std::vector<float> const & getWorkPlace(Time const & time) const;

    void setPosition(Time const & time,
                     maths::Vec3f const & pos);

    void setHome(Time const & time,
                     maths::Vec3f const & pos);

    ~Character();

 private:
//    std::list<Persona*> m_personas;
    std::shared_ptr< Persona >            m_actualPersona;
    std::shared_ptr< RoutinePersona >     m_routinePersona;
    int                                   m_id;
    static int  m_counter;
};

struct CharacterComparator {
    inline bool operator()(Character const & c1,
                           Character const & c2) const {
        return c1.getId() < c2.getId();
    }
};

}  // namespace burdenofproof
#endif  // CHARACTER_HPP_
