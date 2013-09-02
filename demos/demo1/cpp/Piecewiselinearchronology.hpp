// NOLINT(legal/copyright)
#ifndef PIECEWISELINEARCHRONOLOGY_HPP_
#define PIECEWISELINEARCHRONOLOGY_HPP_

#include "Propertychronology.hpp"

template< typename T >
class PiecewiseLinearChronology : public PropertyChronology< T > {
    typedef PropertyChronology< T > Super;

 public:
    PiecewiseLinearChronology();

    ~PiecewiseLinearChronology();

    inline T getValue(boost::posix_time::ptime const & time) const override;
};

template< typename T >
PiecewiseLinearChronology< T >::PiecewiseLinearChronology() {}

template< typename T >
PiecewiseLinearChronology< T >::~PiecewiseLinearChronology() {}

template< typename T >
// TODO(DaleCooper): think about this method
T PiecewiseLinearChronology< T >::getValue(Time const & t) const {
    TemporalValue<T> const& timeAsTV
            = static_cast<TemporalValue<T> >(t);

    auto exactIt
            = Super::m_temporalValues.find(timeAsTV);

    if (exactIt != Super::m_temporalValues.end()) {
        return (*exactIt).getValue();
    }

    auto it1
            =--Super::m_temporalValues.lower_bound(timeAsTV);
    auto it2
            = Super::m_temporalValues.upper_bound(timeAsTV);

    Time const & t1 = (*it1).getTime();
    Time const & t2 = (*it2).getTime();
    Time_Duration t1Tot2 = t2 - t1;
    Time_Duration t1Tot = t - t1;
    std::int64_t length = t1Tot2.ticks();
    std::int64_t deltaT = t1Tot.ticks();
    T const & v1 = (*it1).getValue();
    T const & v2 = (*it2).getValue();

    // TODO(DaleCooper) WARNING INTEGER DIVISION
    return (v1*(length-deltaT)+v2*deltaT)/static_cast<double>(length);
}

#endif  // PIECEWISELINEARCHRONOLOGY_HPP_
