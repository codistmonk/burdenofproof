#ifndef MVC_OBSERVABLE_H
#define MVC_OBSERVABLE_H
#include <set>
#include "Utils.hpp"

class MVC_OBSERVER;

class MVC_OBSERVABLE
{
public:
  MVC_OBSERVABLE(std::set<MVC_OBSERVER*>const * const list= nullptr) { if(list) m_observersList = std::set<MVC_OBSERVER*>(*list); }
  MVC_OBSERVABLE(const MVC_OBSERVABLE& observable) = delete;
  void addObserver(MVC_OBSERVER* const obs) ;
  void removeObserver(MVC_OBSERVER* const obs) ;
  inline const std::set<MVC_OBSERVER*>& getObserversList() const {return m_observersList;}
  virtual ~MVC_OBSERVABLE() =0;
protected:
  void notify() const;
private:
    std::set<MVC_OBSERVER*>	m_observersList;
};









#endif
