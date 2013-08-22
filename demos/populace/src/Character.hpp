#ifndef CHARACTER_HPP
#define CHARACTER_HPP

#include <memory>
#include <list>
#include <string>
#include <utility>
enum class Persona_Type {TRUE_PERSONA , PRIVATE_PLANNED_PERSONA , PUBLIC_PLANNED_PERSONA , PUBLIC_FALSE_PERSONA};
enum class Religion{CATHOLIC, PROTESTANT, ORTHODOX, SUNNI_ISLAM,SHIITE_ISLAM,OTHER_ISLAM,HINDUISM,JUAISM,CHINESE,BUDDHISM,NATURE, AGNOSTICISM,ATHEISM,OTHER};
enum class Sexual_Orientation{HOMOSEXUAL,HETEROSEXUAL,TRANSSEXUAL, BISEXUAL};
enum class Emotional_State{CONFIDENT};
enum class Social_Connexion{BROTHER,MOTHER,FATHER,SISTER};
enum class Health{HEALTHY};

class Material{};

class Character;

class Persona{
  typedef std::pair<const Character*,Social_Connexion> CONNEXION;
public:
  Persona(Persona_Type pt = Persona_Type::PUBLIC_FALSE_PERSONA);
  ~Persona();
private:
  Persona_Type	m_personaType;
  std::string*  m_name;
  std::string*  m_address;
  Religion 	m_religion;
  bool		m_sex;
  Sexual_Orientation	m_sexualOrientation;
  int 		m_age;
  Emotional_State	m_emotionalState;
  std::list<Material>	m_material;
  std::list<CONNEXION>  m_socialNetwork;  //should not be construct for each character, rather retrieved from a social network class.
  Health		m_health;
  //TODO continue
};



class Character{
public:
  Character();
private:
  unsigned int		m_idNumber;
  std::list<Persona>	m_personas;
  static unsigned int   m_counter; //for m_idNumber
};





#endif