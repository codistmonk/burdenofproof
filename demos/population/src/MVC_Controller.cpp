#include <iostream>
#include "MVC_Controller.hpp"
#include "MVC_Model.hpp"
#include "MVC_View.hpp"
#include <algorithm>
MVC_CONTROLLER::MVC_CONTROLLER(MVC_MODEL* const model) :  MVC_OBSERVER(model) {
    model->addObserver(this);
}



MVC_CONTROLLER::~MVC_CONTROLLER() {
    for(auto&  v : m_views){
        removeView(v.first);
    }
}


void MVC_CONTROLLER::addView(const std::string& s, MVC_VIEW * const view){
    m_views[s]=view;
    std::cout << "The view named " << s << " has been inserted" << std::endl;
    
}
void MVC_CONTROLLER::removeView(const std::string& s){
    if(m_views[s]){
        delete m_views[s];
        m_views[s] = nullptr;
//        m_views.erase(s);
    }

    std::cout << "The view named " << s << " has been deleted" << std::endl;
}


MVC_VIEW  * 	MVC_CONTROLLER::getView(const std::string& s) const{
    return m_views[s];
}
