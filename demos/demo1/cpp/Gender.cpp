// NOLINT(legal/copyright)

#include <string>

#include "Gender.hpp"

namespace burdenofproof {

std::string const & toString(Gender const & gender) {
    static std::string const MALE_STRING("MALE");
    static std::string const FEMALE_STRING("FEMALE");

    switch (gender) {
        case Gender::MALE: return MALE_STRING;
        case Gender::FEMALE: return FEMALE_STRING;
    }
}

}  // namespace burdenofproof
