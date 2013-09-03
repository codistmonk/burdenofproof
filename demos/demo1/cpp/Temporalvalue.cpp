// NOLINT(legal/copyright)
#include <boost/algorithm/string.hpp>
#include <string>
#include <vector>
#include "Temporalvalue.hpp"
#include "Maths.hpp"



using std::string;
using boost::algorithm::split;
using boost::is_any_of;
using std::vector;
using std::stof;
using boost::algorithm::to_upper_copy;
using maths::vec3f;

template<>
std::int64_t TemporalValue<std::int64_t>::parseValue(std::string const & str) {
    return std::stoll(str);
}

template<>
std::string TemporalValue<std::string>::parseValue(std::string const & str) {
    return str;
}

template<>
Gender TemporalValue<Gender>::parseValue(std::string const & str) {
    static string const MALE("MALE");
    string STR = to_upper_copy(str);
    return (STR == MALE)?Gender::MALE:Gender::FEMALE;
}

template<>
float TemporalValue<float>::parseValue(std::string const & str) {
    return std::stof(str);
}

template<>
vec3f TemporalValue<vec3f>::parseValue(std::string const & str) {
    vector<string> splitVec(3);
    split(splitVec, str, is_any_of("|"));
    vec3f result;

    for (int i = 0; i < 3; ++i) {
        result[i] = stof(splitVec[0]);
    }

    return result;
}

template<>
std::ostream & operator<<(std::ostream & o,
                          TemporalValue< Gender > const & tp) {
    o << "ptime : " << tp.getTime() << " , value = " <<
         ((tp.getValue() == Gender::MALE)?"Male":"Female");
    return o;
}
