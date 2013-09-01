// NOLINT(legal/copyright)
#ifndef PROPERTYCHRONOLOGY_HPP_
#define PROPERTYCHRONOLOGY_HPP_

#include <cstdint>
#include <map>
#include <set>
#include "Temporalvalue.hpp"


template< typename T >
class PropertyChronology {
 public:
    PropertyChronology() {}

    explicit PropertyChronology(PropertyChronology< T > const & pc) :
        m_temporalValues(pc.m_temporalValues) {}

    explicit PropertyChronology(PropertyChronology< T > && pcRvalue) :
        m_temporalValues(std::move(pcRvalue.m_temporalValues)) {}

    PropertyChronology & operator=(PropertyChronology<T> const& pc);

    PropertyChronology & operator=(PropertyChronology<T> && pcRvalue);

    virtual ~PropertyChronology();

    virtual  T getValue(std::int64_t time) const = 0;

 protected:
    std::set< TemporalValue< T >/*, TemporalValueComparator< T > */ >
    m_temporalValues;
};


template< typename T >
PropertyChronology< T > & PropertyChronology< T >::operator=(
    PropertyChronology< T > const & pc) {
    if (this != &pc) {
        m_temporalValues = pc.m_temporalValues;
    }

    return *this;
}

template< typename T >
PropertyChronology< T > & PropertyChronology< T >::operator=(
    PropertyChronology< T > && pcRvalue) {
    if (this != &pcRvalue) {
        m_temporalValues = std::move(pcRvalue.m_temporalValues);
    }

    return *this;
}

template< typename T >
PropertyChronology< T >::~PropertyChronology() {}

#endif  // PROPERTYCHRONOLOGY_HPP_
