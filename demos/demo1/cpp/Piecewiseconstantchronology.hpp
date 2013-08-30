#ifndef PIECEWISECONSTANTCHRONOLOGY_HPP
#define PIECEWISECONSTANTCHRONOLOGY_HPP

#include "Propertychronology.hpp"

template<typename T>
class PiecewiseConstantChronology : public PropertyChronology<T>{
public:
    PiecewiseConstantChronology();
    ~PiecewiseConstantChronology();
    inline const T& getValue(std::int64_t time) const override;
private:
};

template<typename T>
PiecewiseConstantChronology<T>::PiecewiseConstantChronology(){

}

template<typename T>
PiecewiseConstantChronology<T>::~PiecewiseConstantChronology(){

}

template<typename T>
const T& PiecewiseConstantChronology<T>::getValue(std::int64_t time) const{
    return *PropertyChronology<T>::m_temporalValues.lower_bound(time);

}

#endif // PIECEWISECONSTANTCHRONOLOGY_HPP
