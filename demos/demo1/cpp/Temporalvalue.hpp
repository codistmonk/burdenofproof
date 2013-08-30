#ifndef TEMPORALVALUE_HPP
#define TEMPORALVALUE_HPP

#include <cstdint>

template<typename T>
class TemporalValue
{
public:
    TemporalValue(const T& value);
    inline std::int64_t const&  getTime() const {return m_time;}
    inline bool operator<(TemporalValue<T> const & tv) {return m_time < tv.getTime();}
private:
    T m_value;
    std::int64_t m_time;
};

#endif // TEMPORALVALUE_HPP

template<typename T>
TemporalValue<T>::TemporalValue(const T& value) : m_value(value)
{
}
