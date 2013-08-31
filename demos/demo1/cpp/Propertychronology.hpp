#ifndef PROPERTYCHRONOLOGY_HPP
#define PROPERTYCHRONOLOGY_HPP

#include <cstdint>
#include <map>
#include <set>
#include "Temporalvalue.hpp"


template<typename T>
class PropertyChronology
{
public:
    PropertyChronology();
    virtual ~PropertyChronology();
    virtual  T getValue(std::int64_t time) const = 0;
protected:
    std::set<TemporalValue<T>/*, TemporalValueComparator<T> */>  m_temporalValues;
};


template<typename T>
PropertyChronology<T>::PropertyChronology()
{

}

template<typename T>
PropertyChronology<T>::~PropertyChronology()
{

}

/*************************************************************************************/



#endif // PROPERTYCHRONOLOGY_HPP
