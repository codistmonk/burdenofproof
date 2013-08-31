#ifndef TEMPORALVALUE_HPP
#define TEMPORALVALUE_HPP

#include <cstdint>

template<typename T>
class TemporalValue
{
public:
    TemporalValue(T const& value, std::int64_t const& time);
    virtual ~TemporalValue();
    TemporalValue(std::int64_t const & time);
    inline std::int64_t const&  getTime() const {return m_time;}
    inline T const& getValue() const {return *m_value;}
    inline bool operator<(TemporalValue<T> const & tv) const {return m_time < tv.m_time;}
//    inline bool operator<(std::int64_t const& time) const {return m_time < time;}
private:
    T* m_value;
    std::int64_t m_time;
};

#endif // TEMPORALVALUE_HPP

template<typename T>
TemporalValue<T>::TemporalValue(T const& value, const std::int64_t &time) : m_value(new T(value)), m_time(time)
{
}

template<typename T>
TemporalValue<T>::TemporalValue(std::int64_t const & time) : m_value(nullptr) , m_time(time)
{
}

template<typename T>
TemporalValue<T>::~TemporalValue()
{
    if(m_value)
        delete m_value;
}


/********************************************************************************************/

template<typename T>
struct TemporalValueComparator{
    inline bool operator()(TemporalValue<T> const& tp1, TemporalValue<T> const& tp2) const{ return tp1 < tp2;}
//    inline bool operator()(TemporalValue<T> const& tp1, std::int64_t const& time) const { return tp1 < time;}
//    inline bool operator()(std::int64_t const& time, TemporalValue<T> const& tp1) const { return tp1 < time;}
};
