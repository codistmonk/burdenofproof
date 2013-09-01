// NOLINT(legal/copyright)
#ifndef MATHS_HPP_
#define MATHS_HPP_

#ifndef _MSC_VER
#include <initializer_list>
#endif
#include <random>
#include <memory>
#include <algorithm>

namespace maths{

template<typename T, typename DistribType>
class RandomGenerator{
public:
    RandomGenerator() {}
    inline T operator()() {return  m_distribution(m_randomEngine);}
protected:
    std::mt19937			m_randomEngine;
    DistribType  			m_distribution;
};


class RandomNormalFloatGenerator : public RandomGenerator<float, std::normal_distribution<float>> {
public:
    RandomNormalFloatGenerator(const float mean = 0.0f, const float stddev = 1.0f) : RandomGenerator< float, std::normal_distribution< float > >(), m_mean(mean), m_stddev(stddev) {m_distribution = std::normal_distribution<float>(mean,stddev);}
private:
    float 				m_mean;
    float 				m_stddev;
};

class RandomIntGenerator : public RandomGenerator<int, std::uniform_int_distribution<int>>{
public:
    RandomIntGenerator(int min = 0, int max = 100) : RandomGenerator< int, std::uniform_int_distribution< int > >(), m_min(min), m_max(max) { m_distribution =std::uniform_int_distribution<int>(min,max); }
private:
    int 	m_min;
    int		m_max;
};

#ifndef _MSC_VER

template<typename T, int s>
class Vector
{
public:
    Vector() {}
    Vector(std::initializer_list<T> const& il) {std::copy_n(il.begin(),s,m_data.begin());}
    Vector(Vector<T,s> const & v) {std::copy(v.m_data.begin(),v.m_data.end(),m_data.begin());}
    Vector(Vector<T,s> && vRvalue) : m_data(std::move(vRvalue.m_data)){}
    Vector& operator=(Vector const& v);
    Vector& operator=(Vector && vRvalue);
    constexpr int size() const {return s;}
    inline T const& operator[](int n) const {return m_data[n];}
    inline T& operator[](int n) {return m_data[n];}
    inline Vector<T,s> operator*(T const & t) const ;
    inline Vector<T,s> operator+(Vector<T,s> const & v) const;
    inline Vector<T,s> operator/(T const & t) const;
private:
    std::array<T,s>  m_data;
};


template<typename T, int s>
Vector<T,s>& Vector<T,s>::operator=(Vector const& v) {
    if(this!=&v)
        std::copy(v.m_data.begin(),v.m_data.end(),m_data.begin());
    return *this;
}

template<typename T, int s>
Vector<T,s>& Vector<T,s>::operator=(Vector && vRvalue) {
    if(this!=&vRvalue)
        m_data(std::move(vRvalue.m_data));
    return *this;
}

template<typename T, int s>
Vector<T,s> Vector<T,s>::operator *(T const& t) const {
    Vector<T,s> RES(*this);
    for(int i=0; i < s; ++i)
        RES[i]*=t;
    return RES;
}

template<typename T, int s>
Vector<T,s> Vector<T,s>::operator /(T const& t) const {
    Vector<T,s> RES(*this);
    for(int i=0; i < s; ++i)
        RES[i]/=t;
    return RES;
}

template<typename T, int s>
Vector<T,s> Vector<T,s>::operator +(Vector<T,s> const& v) const {
    Vector<T,s> RES(*this);
    for(int i=0; i < s; ++i)
        RES[i]+=v[i];
    return RES;
}


typedef Vector<float,3> vec3f;

#endif  // _MSC_VER

}  // namespace maths

#endif  // MATHS_HPP_
