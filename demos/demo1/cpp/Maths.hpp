#ifndef MATHS_HPP
#define MATHS_HPP

#include <random>
#include <type_traits>

namespace maths{

  template<typename T, typename DistribType>
  class RandomGenerator{
  public:
    RandomGenerator() {};
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
  
};





















#endif
