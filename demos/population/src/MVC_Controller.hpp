#ifndef MVC_CONTROLLER_H
#define MVC_CONTROLLER_H

#include <string>
#include <map>
#include "MVC_Observer.hpp"


class MVC_VIEW;

typedef MVC_OBSERVABLE MVC_MODEL;

class MVC_CONTROLLER : public MVC_OBSERVER
{
public:
  MVC_CONTROLLER() = delete;
  MVC_CONTROLLER(MVC_MODEL* const model) ;
  MVC_CONTROLLER(MVC_CONTROLLER& ctrler) = delete;
  void 			addView(const std::string& s, MVC_VIEW * const view);
  void 			removeView(const std::string& s);
  MVC_VIEW *    getView(const std::string& s) const;
  virtual       ~MVC_CONTROLLER();
  
private:
  virtual void init() = 0;
protected:
  mutable std::map<std::string,MVC_VIEW*>	m_views;
};


#endif
