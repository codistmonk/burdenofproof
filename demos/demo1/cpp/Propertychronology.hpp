// NOLINT(legal/copyright)
#ifndef PROPERTYCHRONOLOGY_HPP_
#define PROPERTYCHRONOLOGY_HPP_

#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/date_time/posix_time/ptime.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <cstdint>
#include <string>
#include <sstream>
#include <set>
#include <list>
#include "Temporalvalue.hpp"
#include "Utils.hpp"

namespace burdenofproof {

template< typename T >
class PropertyChronology {
 public:
    virtual  T getValue(Time const & time) const = 0;

    virtual void addValue(Time const & time,
                          T const & val) = 0;

    virtual ~PropertyChronology() {}

 protected:
    std::set< TemporalValue< T >,
              TemporalValueComparator< T > > m_Tvalues;
};

//    template< typename T >
//    PropertyChronology< T >::PropertyChronology(
//            boost::filesystem::path const & path) {
//        using boost::filesystem::exists;
//        using boost::filesystem::is_regular_file;
//        using std::string;

//        this->constructFromString(utils::fileToStdString(path));
//    }

//    template<typename T>
//    void PropertyChronology< T >::constructFromString(
//            const std::string & str) {
//        using std::string;
//        using std::vector;
//        using boost::algorithm::split;
//        using boost::algorithm::is_any_of;
//        std::list<string> strList;

//        split(strList, str, is_any_of("\n"));
//        strList.remove_if([&](string const &str) { return str.empty();});
//        for (string const & str : strList) {
//            m_temporalValues.insert(TemporalValue< T >(str));
//        }
//    }

//    template< typename T >
//    PropertyChronology< T > & PropertyChronology< T >::operator=(
//        PropertyChronology< T > const & pc) {
//        if (this != &pc) {
//            m_temporalValues = pc.m_temporalValues;
//        }

//        return *this;
//    }

//    template< typename T >
//    PropertyChronology< T > & PropertyChronology< T >::operator=(
//        PropertyChronology< T > && pcRvalue) {
//        if (this != &pcRvalue) {
//            m_temporalValues = std::move(pcRvalue.m_temporalValues);
//        }

//        return *this;
//    }

//    template< typename U >
//    std::ostream & operator<<(std::ostream & o,
//                              PropertyChronology< U > const & pc) {
//        auto it =  pc.m_temporalValues.cbegin();
//        for ( ; it != pc.m_temporalValues.cend(); ++it) {
//            o << *it << std::endl;
//        }
//        return o;
//    }

//    template< typename T >
//    PropertyChronology< T >::~PropertyChronology() {}

}  // namespace burdenofproof
#endif  // PROPERTYCHRONOLOGY_HPP_
