// NOLINT(legal/copyright)
#ifndef UTILS_HPP_
#define UTILS_HPP_

#include <iostream>  // NOLINT(readability/streams)
#include <string>
#include <deque>
#include <utility>

#define STR(x) #x
#define STRINGIFY(x) STR(x)
#define DEBUG std::cout << "(" __FILE__ << ":" << STRINGIFY(__LINE__) << ") "\
                        << std::endl << std::flush
#define SHOW(a) std::cout << "(" __FILE__ << ":" << STRINGIFY(__LINE__) << ") "\
                          << #a << ": " << (a) << std::endl << std::flush

namespace utils {

class NameFactory {
 public:
    NameFactory();

    virtual ~NameFactory();

    std::string const & randomMaleName();

    std::string const & randomFemaleName();

    std::string const & randomLastName();

 private:
    std::deque< std::string > m_maleFirstNames;

    std::deque< std::string > m_femaleFirstNames;

    std::deque< std::string > m_lastNames;

    unsigned int m_maleFirstNameCount;

    unsigned int m_femaleFirstNameCount;

    unsigned int m_NameCount;
};

}  // namespace utils

#endif  // UTILS_HPP_
