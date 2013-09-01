// NOLINT(legal/copyright)
#ifndef UTILS_HPP_
#define UTILS_HPP_

#include <iostream>
#include <string>
#include <deque>
#include <utility>

#define DEBUG std::cout << __FILE__ << ":" << __LINE__ << std::endl
#define SHOW(a) std::cout << #a << ": " << (a) << std::endl

namespace utils {

    class NameFactory {
    public:
        NameFactory();
        virtual ~NameFactory();
        const std::string&    randomMaleName();
        const std::string&    randomFemaleName();
        const std::string&    randomLastName();
    private:
        std::deque<std::string> m_maleFirstNames;
        std::deque<std::string> m_femaleFirstNames;
        std::deque<std::string> m_lastNames;
        unsigned int      m_maleFirstNameCount;
        unsigned int      m_femaleFirstNameCount;
        unsigned int      m_NameCount;
    };
}  // namespace utils
#endif  // UTILS_HPP_
