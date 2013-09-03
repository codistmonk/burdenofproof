// NOLINT(legal/copyright)
#ifndef TEMPORALVALUE_HPP_
#define TEMPORALVALUE_HPP_

#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include <cstdint>
#include <fstream>  // NOLINT(readability/streams)
#include <memory>
#include <vector>
#include <string>

typedef boost::posix_time::ptime    Time;
typedef boost::posix_time::time_duration    Time_Duration;
typedef boost::filesystem::path     Path;

enum class Gender : int8_t { MALE, FEMALE };

template< typename T >
class TemporalValue {
 public:
    TemporalValue() : m_value(nullptr), m_time(0LL) {}

    explicit TemporalValue(Path const & path);

    TemporalValue(T const & value, Time const & time);

    explicit TemporalValue(Time const &  time);

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

    inline bool operator<(TemporalValue<T> const & tv) const {
        return (*m_value) < (*(tv.m_value));
    }
    template< typename U >
    friend std::ostream & operator<<(std::ostream & o,
                                     TemporalValue< U > const & tp);

 private:
    T parseValue(std::string const & str);

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
    using boost::posix_time::from_iso_string;  // Parse time string of form YYYYMMDDThhmmss where T is delimeter between date and time NOLINT(whitespace/line_length)
    using boost::algorithm::split;
    using boost::is_any_of;
    using std::vector;
    using std::string;

    if (exists(path)) {
        if (is_regular_file(path)) {
            string line;
            vector<string> splitVec(2);
            std::ifstream file(path.string());
            std::getline(file, line);
            split(splitVec, line, is_any_of(";"));
            m_time = from_iso_string(splitVec[0]);
            m_value = std::shared_ptr< T >(new T(parseValue(splitVec[1])));
        }
    }
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
TemporalValue< T >::TemporalValue(Time const & time)
    : m_value(nullptr) , m_time(time) {}

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
std::ostream & operator<<(std::ostream & o, TemporalValue< U > const & tp) {
    o << "ptime : " << tp.m_time << " , value = " << tp.getValue();
    return o;
}

#endif  // TEMPORALVALUE_HPP_
