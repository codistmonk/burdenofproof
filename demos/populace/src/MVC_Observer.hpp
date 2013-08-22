#ifndef MVC_OBSERVER_H
#define MVC_OBSERVER_H


class MVC_OBSERVABLE;


class MVC_OBSERVER
{
public : 
  MVC_OBSERVER(const MVC_OBSERVER& observer) = delete;
  MVC_OBSERVER(MVC_OBSERVABLE* const observable = nullptr) : m_observable(observable){}
  virtual void update() = 0;
  virtual ~MVC_OBSERVER() {}
protected:
  MVC_OBSERVABLE* 	m_observable;
};



#endif
