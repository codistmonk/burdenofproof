#include <fstream>

#include "Utils.hpp"
#include "Maths.hpp"

using namespace utils;

NameFactory::NameFactory()
{
  std::string line;
  std::ifstream femaleNamesFile("../../name/word_list_moby_given_names_english_female.flat.txt",std::ios::in);
  while(femaleNamesFile >> line)
    m_femaleFirstNames.push_back(std::move(line)); //std::move might be dangerous
  m_femaleFirstNameCount = m_femaleFirstNames.size();
  SHOW(m_femaleFirstNameCount);

  
  std::ifstream maleNamesFile("../../name/word_list_moby_given_names_english_male.flat.txt",std::ios::in);
  while(maleNamesFile >> line)
    m_maleFirstNames.push_back(std::move(line)); //std::move might be dangerous
  m_maleFirstNameCount = m_maleFirstNames.size();
  SHOW( m_maleFirstNameCount);
  
  std::ifstream namesFile("../../name/word_list_moby_given_names_english.flat.txt",std::ios::in);
  while(namesFile >> line)
    m_lastNames.push_back(std::move(line)); //std::move might be dangerous
  m_NameCount = m_lastNames.size();
  SHOW(m_NameCount);
}

NameFactory::~NameFactory()
{

}


const std::string& NameFactory::randomMaleName(){
  static maths::RandomIntGenerator rnd(0,m_maleFirstNameCount-1);
  return m_maleFirstNames[rnd()];
}

const std::string& NameFactory::randomFemaleName(){
  static maths::RandomIntGenerator rnd(0,m_femaleFirstNameCount-1);
  return m_femaleFirstNames[rnd()];
}

const std::string& NameFactory::randomLastName(){
  static maths::RandomIntGenerator rnd(0,m_NameCount-1);
  return m_lastNames[rnd()];
}