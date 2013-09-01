// NOLINT(legal/copyright)
#ifndef PIECEWISELINEARCHRONOLOGY_HPP_
#define PIECEWISELINEARCHRONOLOGY_HPP_

#include "Propertychronology.hpp"

template< typename T >
class PiecewiseLinearChronology : public PropertyChronology< T > {
 public:
    PiecewiseLinearChronology();

    ~PiecewiseLinearChronology();

    inline T getValue(std::int64_t time) const override;
};

template< typename T >
PiecewiseLinearChronology< T >::PiecewiseLinearChronology() {}

template< typename T >
PiecewiseLinearChronology< T >::~PiecewiseLinearChronology() {}

template< typename T >
// TODO(DaleCooper): think about this method
T PiecewiseLinearChronology< T >::getValue(std::int64_t const t) const {
    auto exactIt = PropertyChronology<T>::m_temporalValues.find(t);

    if (exactIt != PropertyChronology<T>::m_temporalValues.end()) {
        return (*exactIt).getValue();
    }

    auto it1 =--PropertyChronology<T>::m_temporalValues.lower_bound(t);
    auto it2 =PropertyChronology<T>::m_temporalValues.upper_bound(t);

    auto& t1 = (*it1).getTime();
    auto& t2 = (*it2).getTime();

    auto& v1 = (*it1).getValue();
    auto& v2 = (*it2).getValue();

    // TODO(DaleCooper) WARNING INTEGER DIVISION
    return (v1*(t2-t)+v2*(t-t1))/(t2-t1);
}

#endif  // PIECEWISELINEARCHRONOLOGY_HPP_
