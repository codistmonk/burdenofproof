// NOLINT(legal/copyright)
#ifndef TEMPORALVALUE_HPP_
#define TEMPORALVALUE_HPP_

#include <boost/date_time/posix_time/posix_time.hpp>
#include <cstdint>
#include <memory>

typedef boost::posix_time::ptime    Time;
typedef boost::posix_time::time_duration    Time_Duration;

template< typename T >
class TemporalValue {
 public:
    TemporalValue() : m_value(nullptr), m_time(0LL) {}

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

 private:
    std::shared_ptr< T > m_value;

    Time m_time;
};

template< typename T >
TemporalValue<T>::TemporalValue(T const & value, Time const & time)
    : m_value(new T(value)), m_time(time) {}

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

#endif  // TEMPORALVALUE_HPP_
