// NOLINT(legal/copyright)
#ifndef PROPERTYCHRONOLOGY_HPP_
#define PROPERTYCHRONOLOGY_HPP_

#include <boost/filesystem.hpp>
#include <cstdint>
#include <string>
#include <set>
#include "Temporalvalue.hpp"
#include "Utils.hpp"

template< typename T >
class PropertyChronology {
 public:
    PropertyChronology() {}

    explicit PropertyChronology(boost::filesystem::path const & file);

    explicit PropertyChronology(PropertyChronology< T > const & pc) :
        m_temporalValues(pc.m_temporalValues) {}

    explicit PropertyChronology(PropertyChronology< T > && pcRvalue) :
        m_temporalValues(std::move(pcRvalue.m_temporalValues)) {}

    PropertyChronology & operator=(PropertyChronology<T> const& pc);

    PropertyChronology & operator=(PropertyChronology<T> && pcRvalue);

    virtual ~PropertyChronology();

    virtual  T getValue(boost::posix_time::ptime const & time) const = 0;

    template< typename U >
    friend std::ostream & operator<<(std::ostream & o,
                              PropertyChronology< U > const & pc);

 protected:
    std::set< TemporalValue< T >, TemporalValueComparator< T > >
    m_temporalValues;
};

template< typename T >
PropertyChronology< T >::PropertyChronology(
        boost::filesystem::path const & path) {
    using boost::filesystem::exists;
    using boost::filesystem::is_regular_file;
    using std::string;

    if (exists(path)) {
        if (is_regular_file(path)) {
            string line;
            std::ifstream file(path.string());
            while (!file.eof()) {
                std::getline(file, line);
                if (!line.empty()) {
                    m_temporalValues.insert(TemporalValue< T >(line));
                }
            }
        }
    }
}

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

template< typename U >
std::ostream & operator<<(std::ostream & o,
                          PropertyChronology< U > const & pc) {
    auto it =  pc.m_temporalValues.cbegin();
    for ( ; it != pc.m_temporalValues.cend(); ++it) {
        o << *it << std::endl;
    }
    return o;
}

template< typename T >
PropertyChronology< T >::~PropertyChronology() {}

#endif  // PROPERTYCHRONOLOGY_HPP_
