// NOLINT(legal/copyright)
#include <boost/algorithm/string.hpp>
#include <string>
#include <vector>
#include "Temporalvalue.hpp"
#include "Maths.hpp"
#include "Utils.hpp"

using boost::algorithm::split;
using boost::algorithm::to_upper_copy;
using boost::is_any_of;
using boost::posix_time::to_simple_string;
using maths::Vec3f;
using std::stof;
using std::string;
using std::vector;

namespace burdenofproof {

//    template<>
//    Time TemporalValue< Time >::parseValue(std::string const & str) {
//        return boost::posix_time::from_iso_string(str);
//    }

//    template<>
//    std::string TemporalValue<std::string>::parseValue(
//    std::string const & str) {
//        return str;
//    }

//    template<>
//    Gender TemporalValue<Gender>::parseValue(std::string const & str) {
//        static string const MALE("MALE");
//        string STR = to_upper_copy(str);
//        return (STR == MALE) ? Gender::MALE : Gender::FEMALE;
//    }

//    template<>
//    float TemporalValue<float>::parseValue(std::string const & str) {
//        return std::stof(str);
//    }

//    template<>
//    vec3f TemporalValue<vec3f>::parseValue(std::string const & str) {
//        vector<string> splitVec(3);
//        split(splitVec, str, is_any_of("|"));
//        vec3f result;

//        for (int i = 0; i < 3; ++i) {
//            result[i] = stof(splitVec[i]);
//        }

//        return result;
//    }

//    template<>
//    std::ostream & operator<<(std::ostream & o,
//                              TemporalValue< Gender > const & tp) {
//        o << "ptime : " << to_simple_string(tp.getTime())
//          << " , value = " << burdenofproof::toString(tp.getValue());

//        return o;
//    }

//    template<>
//    std::ostream & operator<<(std::ostream & o,
//                              TemporalValue< float > const & tp) {
//        o << "ptime : " << to_simple_string(tp.getTime())
//          << " , value = " << std::to_string(tp.getValue());

//        return o;
//    }

}  // namespace burdenofproof
