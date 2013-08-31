#include <fstream>
#include <string>
#include "Utils.hpp"
#include "Maths.hpp"

#define FEMALE_NAMES "../../name/word_list_moby_given_names_english_female.flat.txt"
#define MALE_NAMES "../../name/word_list_moby_given_names_english_male.flat.txt"
#define LAST_NAMES "../../name/word_list_moby_given_names_english.flat.txt"
using utils::NameFactory;

NameFactory::NameFactory() {
  std::string line;
  std::ifstream femaleNamesFile(FEMALE_NAMES, std::ios::in);
  while (femaleNamesFile >> line)
    m_femaleFirstNames.push_back(std::move(line));  // std::move might be dangerous
  m_femaleFirstNameCount = m_femaleFirstNames.size();
  SHOW(m_femaleFirstNameCount);

  std::ifstream maleNamesFile(MALE_NAMES, std::ios::in);
  while (maleNamesFile >> line)
    m_maleFirstNames.push_back(std::move(line));  // std::move might be dangerous
  m_maleFirstNameCount = m_maleFirstNames.size();
  SHOW(m_maleFirstNameCount);

  std::ifstream namesFile(LAST_NAMES, std::ios::in);
  while (namesFile >> line)
    m_lastNames.push_back(std::move(line));  // std::move might be dangerous
  m_NameCount = m_lastNames.size();
  SHOW(m_NameCount);
}

NameFactory::~NameFactory() {
}


const std::string& NameFactory::randomMaleName() {
  static maths::RandomIntGenerator rnd(0, m_maleFirstNameCount-1);
  return m_maleFirstNames[rnd()];
}

const std::string& NameFactory::randomFemaleName() {
  static maths::RandomIntGenerator rnd(0, m_femaleFirstNameCount-1);
  return m_femaleFirstNames[rnd()];
}

const std::string& NameFactory::randomLastName() {
  static maths::RandomIntGenerator rnd(0, m_NameCount-1);
  return m_lastNames[rnd()];
}
