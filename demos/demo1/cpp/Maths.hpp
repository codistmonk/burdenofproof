// NOLINT(legal/copyright)
#ifndef MATHS_HPP_
#define MATHS_HPP_

#ifndef _MSC_VER
#include <initializer_list>
#endif
#include <random>
#include <iostream>  // NOLINT(readability/streams)
#include <string>
#include <memory>
#include <vector>
#include <algorithm>

namespace maths {

template< typename T, typename DistribType >
class RandomGenerator {
 public:
    RandomGenerator() {}

    inline T operator()() {
        return  m_distribution(m_randomEngine);
    }
 protected:
    std::mt19937 m_randomEngine;

    DistribType  m_distribution;
};

class RandomNormalFloatGenerator : public RandomGenerator< float,
        std::normal_distribution< float > > {
 public:
    RandomNormalFloatGenerator(float const mean = 0.0f,
        float const stddev = 1.0f) :
        RandomGenerator< float, std::normal_distribution< float > >(),
        m_mean(mean), m_stddev(stddev) {
            m_distribution = std::normal_distribution< float >(mean, stddev);
        }
    float getMean() const {return m_mean;}
    float getStdDev() const {return m_stddev;}
 private:
    float m_mean;

    float m_stddev;
};

class RandomIntGenerator : public RandomGenerator< int,
        std::uniform_int_distribution< int > > {
 public:
    RandomIntGenerator(int const min = 0, int const max = 100) :
        RandomGenerator< int, std::uniform_int_distribution< int > >(),
        m_min(min),
        m_max(max) {
            m_distribution = std::uniform_int_distribution< int >(min, max);
        }
    int getMin() const {return m_min;}
    int getMax() const {return m_max;}

 private:
    int m_min;
    int m_max;
};

template< typename T, size_t size >
class Vector {
 public:
    Vector() : m_data(size) {}

    Vector(Vector< T, size > const & v) {
        std::copy(v.m_data.begin(), v.m_data.end(), m_data.begin());
    }

    #ifndef _MSC_VER
    explicit Vector(std::initializer_list< T > const & il) {
        std::copy_n(il.begin(),
                    std::min(size, il.size()),
                    m_data.begin());
        std::abort();
    }

    Vector< T, size > & operator=(std::initializer_list< T > const & il) {
        std::copy_n(il.begin(),
                    std::min(size, il.size()),
                    m_data.begin());
        std::abort();
    }

    #endif

    Vector& operator=(Vector const & v);

    Vector& operator=(Vector && vRvalue);

    inline int getSize() const {
        return size;
    }

    inline T const & operator[](std::size_t const n) const {
        return m_data[n];
    }

    inline T & operator[](std::size_t const n) {
        return m_data[n];
    }

    inline std::vector<float> const & getData() const {return m_data;}

    inline Vector< T, size > operator*(T const & t) const;

    inline Vector< T, size > operator+(Vector< T, size > const & v) const;

    inline Vector< T, size > operator/(T const & t) const;

    template<typename U, size_t t>
    friend inline std::ostream & operator<<(std::ostream & o,
                                            Vector< U, t > const & v);

 private:
    std::vector< T > m_data;
};

template< typename T, size_t size >
Vector< T, size > & Vector< T, size >::operator=(Vector const& v) {
    if (this != &v) {
        std::copy(v.m_data.begin(), v.m_data.end(), m_data.begin());
    }

    return *this;
}

template< typename T, size_t size >
Vector< T, size >& Vector< T, size >::operator=(Vector && vRvalue) {
    if (this != &vRvalue) {
        m_data(std::move(vRvalue.m_data));
    }

    return *this;
}

template< typename T, size_t size >
Vector< T, size > Vector< T, size >::operator*(T const & t) const {
    Vector< T, size > result(*this);

    for (int i = 0; i < this->getSize(); ++i) {
        result[i] *= t;
    }

    return result;
}

template< typename T, size_t size >
Vector< T, size > Vector< T, size >::operator/(T const & t) const {
    Vector< T, size > result(*this);

    for (int i = 0; i < this->getSize(); ++i) {
        result[i] /= t;
    }

    return result;
}

template< typename T, size_t size >
Vector< T, size > Vector< T, size >::operator+(
        Vector< T, size > const & v) const {
    Vector< T, size > result(*this);

    for (int i = 0; i < this->getSize(); ++i) {
        result[i] += v[i];
    }

    return result;
}

template<typename U, size_t t>
std::ostream & operator<<(std::ostream & o, Vector< U, t > const & v) {
    o << "(";

    for (int i = 0 ; i < v.getSize()-1; ++i) {
        o << std::to_string(v[i]) << ", ";
    }

    o << std::to_string(v[t - 1]) << ")";

    return o;
}

typedef Vector< float, 3 > vec3f;

}  // namespace maths

#endif  // MATHS_HPP_
