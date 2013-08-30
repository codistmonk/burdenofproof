#ifndef PIECEWISELINEARCHRONOLOGY_HPP
#define PIECEWISELINEARCHRONOLOGY_HPP

#include "Propertychronology.hpp"

template<typename T>
class PiecewiseLinearChronology : public PropertyChronology<T>{
public:
    PiecewiseLinearChronology();
    ~PiecewiseLinearChronology();
    inline const T& getValue(std::int64_t time) const override;
private:
};

template<typename T>
PiecewiseLinearChronology<T>::PiecewiseLinearChronology(){

}

template<typename T>
PiecewiseLinearChronology<T>::~PiecewiseLinearChronology(){

}

template<typename T>
//TODO: think about this method
const T& PiecewiseLinearChronology<T>::getValue(std::int64_t t) const{

    if(PropertyChronology<T>::m_temporalValues.count(t))
        return PropertyChronology<T>::m_temporalValues.find(t);

    T& v1 =*(--PropertyChronology<T>::m_temporalValues.lower_bound(t));
    T& v2 =*PropertyChronology<T>::m_temporalValues.upper_bound(t);

    //TODO
    return *PropertyChronology<T>::m_temporalValues.lower_bound(t);

}

#endif // PIECEWISELINEARCHRONOLOGY_HPP
