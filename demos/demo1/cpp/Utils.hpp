#ifndef UTILS_HPP
#define UTILS_HPP

#include <iostream>
#include <deque>
#include <string>
#include <utility>

#define DEBUG std::cout << __FILE__ << ":" << __LINE__ << std::endl
#define SHOW(a) std::cout << #a << ": " << (a) << std::endl

namespace utils{
  
class NameFactory{
  
public:
  NameFactory();
  virtual ~NameFactory();
  const std::string& 		randomMaleName();
  const std::string&		randomFemaleName();
  const std::string&		randomLastName();
private:
  std::deque<std::string>	m_maleFirstNames;
  std::deque<std::string>	m_femaleFirstNames;
  std::deque<std::string>	m_lastNames;
  unsigned int 			m_maleFirstNameCount;
  unsigned int 			m_femaleFirstNameCount;
  unsigned int 			m_NameCount;
};


};











#endif
