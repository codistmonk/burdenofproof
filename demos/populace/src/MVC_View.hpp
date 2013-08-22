#ifndef MVC_VIEW_H
#define MVC_VIEW_H
#include "MVC_Controller.hpp"

class MVC_VIEW : public MVC_OBSERVER
{
public:
  MVC_VIEW(MVC_MODEL* const model = nullptr, MVC_CONTROLLER* const ctrler = nullptr);
  MVC_VIEW(const MVC_VIEW& view) = delete;
  virtual ~MVC_VIEW() = 0;
protected:
  MVC_CONTROLLER*	m_controller;
};

#endif
