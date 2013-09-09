// NOLINT(legal/copyright)
#ifndef PIECEWISELINEARCHRONOLOGY_HPP_
#define PIECEWISELINEARCHRONOLOGY_HPP_

#include <string>
#include "Propertychronology.hpp"

namespace burdenofproof {

template< typename T >
class PeriodicPiecewiseLinearChronology : public PropertyChronology< T > {
    typedef PropertyChronology< T > Super;

 public:
    PeriodicPiecewiseLinearChronology() {}

    ~PeriodicPiecewiseLinearChronology();

    virtual inline void addValue(Time const & time,
                          T const & val) override {
        Super::m_Tvalues.insert(TemporalValue< T >(val,
                                            MIN_TIME + time.time_of_day()));
    }

    virtual inline T getValue(Time const & time) const override;
};


template< typename T >
PeriodicPiecewiseLinearChronology< T >::~PeriodicPiecewiseLinearChronology() {}

template< typename T >
T PeriodicPiecewiseLinearChronology< T >::getValue(Time const & time) const {
    static TemporalValue< T > timeAsTV;
    Time t = Time(MIN_TIME + time.time_of_day());

    timeAsTV.setTime(t);

    auto exactIt
            = Super::m_Tvalues.find(timeAsTV);

    if (exactIt != Super::m_Tvalues.end()) {
        return (*exactIt).getValue();
    }

    auto it1
            =--Super::m_Tvalues.lower_bound(timeAsTV);
    auto it2
            = Super::m_Tvalues.upper_bound(timeAsTV);
    assert(it1 != Super::m_Tvalues.end());
    assert(it2 != Super::m_Tvalues.end());

    Time const & t1 = (*it1).getTime();
    Time const & t2 = (*it2).getTime();
    Time_Duration t1Tot2 = t2 - t1;
    Time_Duration t1Tot = t - t1;
    std::int64_t length = t1Tot2.ticks();
    std::int64_t deltaT = t1Tot.ticks();
    T const & v1 = (*it1).getValue();
    T const & v2 = (*it2).getValue();

    if (length != 0LL) {
        return (v1*(length-deltaT)+v2*deltaT)/static_cast<double>(length);
    } else {
        return v1;
    }
}

template< typename T >
class AbsolutePiecewiseLinearChronology : public PropertyChronology< T > {
    typedef PropertyChronology< T > Super;

 public:
    AbsolutePiecewiseLinearChronology() {}

    ~AbsolutePiecewiseLinearChronology();

    virtual inline void addValue(Time const & time,
                          T const & val) override {
        Super::m_Tvalues.insert(TemporalValue< T >(val, time));
    }

    inline virtual T getValue(Time const & time) const override;
};


template< typename T >
AbsolutePiecewiseLinearChronology< T >::~AbsolutePiecewiseLinearChronology() {}

template< typename T >
T AbsolutePiecewiseLinearChronology< T >::getValue(Time const & t) const {
    static TemporalValue< T > timeAsTV;

    timeAsTV.setTime(t);


    auto exactIt
            = Super::m_Tvalues.find(timeAsTV);

    if (exactIt != Super::m_Tvalues.end()) {
        return (*exactIt).getValue();
    }

    auto it1
            =--Super::m_Tvalues.lower_bound(timeAsTV);
    auto it2
            = Super::m_Tvalues.upper_bound(timeAsTV);

    assert(it1 != Super::m_Tvalues.end());
    assert(it2 != Super::m_Tvalues.end());

    Time const & t1 = (*it1).getTime();
    Time const & t2 = (*it2).getTime();
    Time_Duration t1Tot2 = t2 - t1;
    Time_Duration t1Tot = t - t1;
    std::int64_t length = t1Tot2.ticks();
    std::int64_t deltaT = t1Tot.ticks();
    T const & v1 = (*it1).getValue();
    T const & v2 = (*it2).getValue();

    if (length != 0LL) {
        return (v1*(length-deltaT)+v2*deltaT)/static_cast<double>(length);
    } else {
        return v1;
    }
}

}  // namespace burdenofproof

#endif  // PIECEWISELINEARCHRONOLOGY_HPP_
