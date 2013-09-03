// NOLINT(legal/copyright)

#ifndef GENDER_HPP_
#define GENDER_HPP_

#include <string>

namespace burdenofproof {

enum class Gender : int8_t {
    MALE,
    FEMALE
};

std::string const & toString(Gender const & gender);

}  // namespace burdenofproof

#endif  // GENDER_HPP_
