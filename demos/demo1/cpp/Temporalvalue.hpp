// NOLINT(legal/copyright)
#ifndef TEMPORALVALUE_HPP_
#define TEMPORALVALUE_HPP_

#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include <cstdint>
#include <cassert>
#include <fstream>  // NOLINT(readability/streams)
#include <memory>
#include <vector>
#include <string>
#include "Utils.hpp"
#include "Gender.hpp"

typedef boost::posix_time::ptime    Time;
typedef boost::posix_time::time_duration    Time_Duration;
typedef boost::filesystem::path     Path;

class vec3f;

template< typename T >
class TemporalValue {
 public:
    TemporalValue() : m_value(new T()), m_time() {}

    explicit TemporalValue(Time const &  time) :
        m_value(nullptr),
        m_time(time) {}

    TemporalValue(T const & value, Time const & time);

    explicit TemporalValue(Path const & path);

    explicit TemporalValue(std::string const & str) {
        this->constructFromString(str);
    }

    explicit TemporalValue(TemporalValue<T> const & tv)
        : m_value(tv.m_value), m_time(tv.m_time) {}

    explicit TemporalValue(TemporalValue<T> && tvRvalue)
        : m_value(std::move(tvRvalue.m_value)), m_time(tvRvalue.m_time) {}

    TemporalValue& operator=(TemporalValue const& tv);

    TemporalValue& operator=(TemporalValue &&tvRvalue);

    virtual ~TemporalValue();

    inline Time const & getTime() const {
        return m_time;
    }

    inline T const & getValue() const {
        return *m_value;
    }

    inline void setTime(Time const & t) {
        m_time = t;
    }

    inline bool operator<(TemporalValue<T> const & tv) const {
        return (*m_value) < (*(tv.m_value));
    }

    template< typename U >
    friend std::ostream & operator<<(std::ostream & o,
                                     TemporalValue< U > const & tp);

 private:
    T parseValue(std::string const & str);
    void constructFromString(std::string const & str);

 private:
    std::shared_ptr< T > m_value;

    Time m_time;
};

template< typename T >
TemporalValue<T>::TemporalValue(T const & value, Time const & time)
    : m_value(new T(value)), m_time(time) {}

template< typename T >
TemporalValue<T>::TemporalValue(Path const & path) {
    using boost::filesystem::exists;
    using boost::filesystem::is_regular_file;
    using std::string;

    assert(exists(path));
    assert(is_regular_file(path));

    string line;
    std::ifstream file(path.string());
    std::getline(file, line);
    this->constructFromString(line);
}

template< typename T >
void TemporalValue< T >::constructFromString(std::string const & str) {
    using boost::algorithm::split;
    // Parse time string of form YYYYMMDDThhmmss where T is delimeter between date and time NOLINT(whitespace/line_length)
    using boost::posix_time::from_iso_string;
    using boost::is_any_of;
    using std::vector;
    using std::string;
    using boost::posix_time::from_iso_string;
    vector<string> splitVec(2);
    split(splitVec, str, is_any_of(";"));
    m_time = from_iso_string(splitVec[0]);
    m_value = std::shared_ptr< T >(new T(parseValue(splitVec[1])));
}

template< typename T >
TemporalValue< T > & TemporalValue< T >::operator=(TemporalValue const & tv) {
    if (this != &tv) {
        m_value = tv.m_value;
        m_time = tv.m_time;
    }

    return *this;
}

template< typename T >
TemporalValue< T > & TemporalValue< T >::operator=(TemporalValue && tvRvalue) {
    if (this != &tvRvalue) {
        m_value = std::move(tvRvalue.m_value);
        m_time = tvRvalue.m_time;
    }

    return *this;
}

template< typename T >
TemporalValue< T >::~TemporalValue() {}

template< typename T >
struct TemporalValueComparator {
    inline bool operator()(TemporalValue< T > const & tp1,
                           TemporalValue< T > const & tp2) const {
        return tp1.getTime() < tp2.getTime();
    }
};

template< typename U >
std::ostream & operator<<(std::ostream & o,
                          TemporalValue< U > const & tp) {
    using boost::posix_time::to_simple_string;

    o << "ptime : " << to_simple_string(tp.getTime())
      << " , value = " << tp.getValue();

    return o;
}

using burdenofproof::Gender;

template<>
std::ostream & operator<<(std::ostream & o,
                          TemporalValue< Gender > const & tp);

template<>
std::ostream & operator<<(std::ostream & o,
                          TemporalValue< float > const & tp);

template<>
Time TemporalValue< Time >::parseValue(std::string const & str);

template<>
std::string TemporalValue< std::string >::parseValue(std::string const & str);

template<>
Gender TemporalValue< Gender >::parseValue(std::string const & str);

template<>
float TemporalValue< float >::parseValue(std::string const & str);

template<>
vec3f TemporalValue< vec3f >::parseValue(std::string const & str);

#endif  // TEMPORALVALUE_HPP_
