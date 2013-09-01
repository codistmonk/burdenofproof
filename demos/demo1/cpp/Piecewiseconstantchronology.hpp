// NOLINT(legal/copyright)
#ifndef PIECEWISECONSTANTCHRONOLOGY_HPP_
#define PIECEWISECONSTANTCHRONOLOGY_HPP_

#include "Propertychronology.hpp"

#ifndef _MSC_VER

template<typename T>
class PiecewiseConstantChronology : public PropertyChronology<T>{
public:
    PiecewiseConstantChronology();
    ~PiecewiseConstantChronology();
    virtual T getValue(std::int64_t time) const override;
private:
};

template<typename T>
PiecewiseConstantChronology<T>::PiecewiseConstantChronology(){

}

template<typename T>
PiecewiseConstantChronology<T>::~PiecewiseConstantChronology(){

}

template<typename T>
T PiecewiseConstantChronology<T>::getValue(std::int64_t time) const{
    return (*PropertyChronology<T>::m_temporalValues.lower_bound(time)).getValue();

}

#endif  // _MSC_VER

#endif  // PIECEWISECONSTANTCHRONOLOGY_HPP_
