#ifndef PROPERTYCHRONOLOGY_HPP
#define PROPERTYCHRONOLOGY_HPP

#include <cstdint>
#include <set>
#include "Temporalvalue.hpp"


template<typename T>
class PropertyChronology
{
public:
    PropertyChronology();
    virtual ~PropertyChronology() = 0;
    virtual const T& getValue(std::int64_t time);
protected:
    std::set<TemporalValue<T> >  m_temporalValues;
};


template<typename T>
PropertyChronology<T>::PropertyChronology()
{
}


/*************************************************************************************/



#endif // PROPERTYCHRONOLOGY_HPP
