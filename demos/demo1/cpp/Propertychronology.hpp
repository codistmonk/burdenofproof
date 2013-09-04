// NOLINT(legal/copyright)
#ifndef PROPERTYCHRONOLOGY_HPP_
#define PROPERTYCHRONOLOGY_HPP_

#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/date_time/posix_time/ptime.hpp>
#include <cstdint>
#include <string>
#include <sstream>
#include <set>
#include <list>
#include "Temporalvalue.hpp"
#include "Utils.hpp"

template< typename T >
class PropertyChronology {
 public:
    PropertyChronology() {}

    explicit PropertyChronology(boost::filesystem::path const & file);

    explicit PropertyChronology(
            std::string const & str) { this->constructFromString(str);}

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
    std::set< TemporalValue< T >,
              TemporalValueComparator< T > > m_temporalValues;

 private:
    void constructFromString(std::string const & str);
};

template< typename T >
PropertyChronology< T >::PropertyChronology(
        boost::filesystem::path const & path) {
    using boost::filesystem::exists;
    using boost::filesystem::is_regular_file;
    using std::string;

    this->constructFromString(utils::fileToStdString(path));
}

template<typename T>
void PropertyChronology< T >::constructFromString(
        const std::string & str) {
    SHOW(str);
    using std::string;
    using std::vector;
    using boost::algorithm::split;
    using boost::algorithm::is_any_of;
    std::list<string> strList;

    split(strList, str, is_any_of("\n"));
    strList.remove_if([&](string const &str) { return str.empty();});
    for (string const & str : strList) {
        m_temporalValues.insert(TemporalValue< T >(str));
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
