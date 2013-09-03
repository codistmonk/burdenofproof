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
 private:
    int m_min;
    int m_max;
};

template< typename T, int S >
class Vector {
 public:
    Vector() {}

    Vector(Vector< T, S > const & v) {
        std::copy(v.m_data, v.m_data + S, m_data);
    }

    Vector& operator=(Vector const & v);

    Vector& operator=(Vector && vRvalue);

    inline int size() const {
        return S;
    }

    inline T const & operator[](int const n) const {
        return m_data[n];
    }

    inline T & operator[](int const n) {
        return m_data[n];
    }

    inline Vector< T, S > operator*(T const & t) const;

    inline Vector< T, S > operator+(Vector< T, S > const & v) const;

    inline Vector< T, S > operator/(T const & t) const;

    template<typename U, int t>
    friend inline std::ostream & operator<<(std::ostream & o,
                                            Vector< U, t > const & v);

 private:
    T m_data[S];
};


template< typename T, int S >
Vector< T, S > & Vector< T, S >::operator=(Vector const& v) {
    if (this != &v) {
        std::copy(v.m_data.begin(), v.m_data.end(), m_data.begin());
    }

    return *this;
}

template< typename T, int S >
Vector< T, S >& Vector< T, S >::operator=(Vector && vRvalue) {
    if (this != &vRvalue) {
        m_data(std::move(vRvalue.m_data));
    }

    return *this;
}

template< typename T, int S >
Vector< T, S > Vector< T, S >::operator*(T const & t) const {
    Vector< T, S > result(*this);

    for (int i = 0; i < S; ++i) {
        result[i] *= t;
    }

    return result;
}

template< typename T, int S >
Vector< T, S > Vector< T, S >::operator/(T const & t) const {
    Vector< T, S > result(*this);

    for (int i = 0; i < S; ++i) {
        result[i] /= t;
    }

    return result;
}

template< typename T, int S >
Vector< T, S > Vector< T, S >::operator+(Vector< T, S > const & v) const {
    Vector< T, S > result(*this);

    for (int i = 0; i < S; ++i) {
        result[i] += v[i];
    }

    return result;
}

template<typename U, int t>
std::ostream & operator<<(std::ostream & o, Vector< U, t > const & v) {
    o << "(";

    for (int i = 0 ; i < t - 1; ++i) {
        o << v[i] << ", ";
    }

    o << v[t-1] << ")";

    return o;
}

typedef Vector< float, 3 > vec3f;

}  // namespace maths

#endif  // MATHS_HPP_
