#ifndef PIECEWISECONSTANTCHRONOLOGY_HPP
#define PIECEWISECONSTANTCHRONOLOGY_HPP

#include "Propertychronology.hpp"

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

#endif // PIECEWISECONSTANTCHRONOLOGY_HPP
