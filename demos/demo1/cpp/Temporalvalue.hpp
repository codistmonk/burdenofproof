// NOLINT(legal/copyright)
#ifndef TEMPORALVALUE_HPP_
#define TEMPORALVALUE_HPP_

#include <cstdint>
#include <memory>

template<typename T>
class TemporalValue {
public:
    TemporalValue() : m_value(nullptr), m_time(0LL) {}
    TemporalValue(T const& value, std::int64_t const& time);
    explicit TemporalValue(std::int64_t const & time);
    TemporalValue(TemporalValue<T> const & tv) : m_value(tv.m_value),
                                                 m_time(tv.m_time) {}
    TemporalValue(TemporalValue<T> && tvRvalue) : m_value(std::move(tvRvalue.m_value)),
                                                  m_time(tvRvalue.m_time) {}
    TemporalValue& operator=(TemporalValue const& tv);
    TemporalValue& operator=(TemporalValue &&tvRvalue);
    virtual ~TemporalValue();
    inline std::int64_t const&  getTime() const {return m_time;}
    inline T const& getValue() const {return *m_value;}
    inline bool operator<(TemporalValue<T> const & tv) const {return m_time < tv.m_time;}
//    inline bool operator<(std::int64_t const& time) const {return m_time < time;}
private:
    std::shared_ptr<T> m_value;
    std::int64_t m_time;
};

template<typename T>
TemporalValue<T>::TemporalValue(T const& value, const std::int64_t &time) : m_value(new T(value)),
                                                                            m_time(time) {
}

template<typename T>
TemporalValue<T>& TemporalValue<T>::operator=(TemporalValue const& tv) {
    if (this != &tv) {
        m_value = tv.m_value;
        m_time = tv.m_time;
    }
    return *this;
}

template<typename T>
TemporalValue<T>& TemporalValue<T>::operator=(TemporalValue && tvRvalue) {
    if (this != &tvRvalue) {
        m_value = std::move(tvRvalue.m_value);
        m_time = tvRvalue.m_time;
    }
    return *this;
}


template<typename T>
TemporalValue<T>::TemporalValue(std::int64_t const & time) : m_value(nullptr) , m_time(time) {
}

template<typename T>
TemporalValue<T>::~TemporalValue() {
}

template<typename T>
struct TemporalValueComparator {
    inline bool operator()(TemporalValue<T> const& tp1, TemporalValue<T> const& tp2) const {return tp1 < tp2;}
//    inline bool operator()(TemporalValue<T> const& tp1, std::int64_t const& time) const { return tp1 < time;}
//    inline bool operator()(std::int64_t const& time, TemporalValue<T> const& tp1) const { return tp1 < time;}
};
#endif  // TEMPORALVALUE_HPP_
