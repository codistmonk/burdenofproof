// NOLINT(legal/copyright)
#ifndef PIECEWISECONSTANTCHRONOLOGY_HPP_
#define PIECEWISECONSTANTCHRONOLOGY_HPP_

#include <string>
#include "Propertychronology.hpp"


template< typename T >
class PiecewiseConstantChronology : public PropertyChronology< T > {
    typedef PropertyChronology< T > Super;
 public:
    PiecewiseConstantChronology() :
        Super() {}

    explicit PiecewiseConstantChronology(
            std::string const & s) : Super(s) {}

    explicit PiecewiseConstantChronology(
            boost::filesystem::path const & path) : Super(path) {}

    ~PiecewiseConstantChronology();

    virtual T getValue(boost::posix_time::ptime const & time) const override;
};


template< typename T >
PiecewiseConstantChronology<T>::~PiecewiseConstantChronology() {}

template< typename T >
T PiecewiseConstantChronology< T >::getValue(Time const & t) const {
    static TemporalValue< T > TPForFastGetValue;
    TPForFastGetValue.setTime(t);
    return (*Super::m_temporalValues
            .lower_bound(TPForFastGetValue))
            .getValue();
}

#endif  // PIECEWISECONSTANTCHRONOLOGY_HPP_
