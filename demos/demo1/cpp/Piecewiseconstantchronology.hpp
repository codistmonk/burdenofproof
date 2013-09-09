// NOLINT(legal/copyright)
#ifndef PIECEWISECONSTANTCHRONOLOGY_HPP_
#define PIECEWISECONSTANTCHRONOLOGY_HPP_

#include <string>
#include "Propertychronology.hpp"

namespace burdenofproof {

template< typename T >
class PeriodicPiecewiseConstantChronology : public PropertyChronology< T > {
    typedef PropertyChronology< T > Super;
 public:
    PeriodicPiecewiseConstantChronology() {}

    inline ~PeriodicPiecewiseConstantChronology() {}

    virtual inline void addValue(Time const & time,
                          T const & val) override {
        Super::m_Tvalues.insert(
                    TemporalValue< T >(val, MIN_TIME + time.time_of_day()));
    }

    virtual T getValue(boost::posix_time::ptime const & time) const override;
};

template< typename T >
T PeriodicPiecewiseConstantChronology< T >::getValue(Time const & t) const {
    static TemporalValue< T > TPForFastGetValue;
    TPForFastGetValue.setTime(MIN_TIME + t.time_of_day());
    assert(Super::m_Tvalues.lower_bound(TPForFastGetValue)
            != Super::m_Tvalues.end());

    return (*Super::m_Tvalues
            .lower_bound(TPForFastGetValue))
            .getValue();
}

template< typename T >
class AbsolutePiecewiseConstantChronology : public PropertyChronology< T > {
    typedef PropertyChronology< T > Super;
 public:
    AbsolutePiecewiseConstantChronology() {}

    inline ~AbsolutePiecewiseConstantChronology() {}

    virtual inline void addValue(Time const & time,
                          T const & val) override {
        Super::m_Tvalues.insert(TemporalValue< T >(val, time));
    }

    virtual T getValue(boost::posix_time::ptime const & time) const override;
};

template< typename T >
T AbsolutePiecewiseConstantChronology< T >::getValue(Time const & t) const {
    static TemporalValue< T > TPForFastGetValue;
    TPForFastGetValue.setTime(t);
    assert(Super::m_Tvalues.lower_bound(TPForFastGetValue)
            != Super::m_Tvalues.end());

    return (*Super::m_Tvalues
            .lower_bound(TPForFastGetValue))
            .getValue();
}
}  // namespace burdenofproof

#endif  // PIECEWISECONSTANTCHRONOLOGY_HPP_
