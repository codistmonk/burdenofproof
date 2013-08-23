#include "MVC_View.hpp"
#include "MVC_Controller.hpp"
#include "MVC_Model.hpp"

MVC_VIEW::MVC_VIEW(MVC_MODEL* const model, MVC_CONTROLLER* const ctrler) : MVC_OBSERVER(model) {
    model->addObserver(this);
    m_controller = ctrler;
}

MVC_VIEW::~MVC_VIEW() {}
