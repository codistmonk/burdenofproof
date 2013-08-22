#include <iostream>
#include "MVC_Observable.hpp"
#include "MVC_Observer.hpp"
#include <algorithm>
using std::cout;
using std::endl;


MVC_OBSERVABLE::~MVC_OBSERVABLE() {
    cout << "MVC_observable dtor" << endl;
}



void MVC_OBSERVABLE::addObserver(MVC_OBSERVER* const obs) {
    m_observersList.insert(obs);
}


void MVC_OBSERVABLE::removeObserver(MVC_OBSERVER* const obs) {
    m_observersList.erase(obs);
}


void MVC_OBSERVABLE::notify() const{
//    std::cout << "m_observersList size: " << m_observersList.size() << std::endl;
    for(MVC_OBSERVER* obs : m_observersList){
        if(obs)
            obs->update();
    }
}


//MVC_OBSERVABLE::MVC_OBSERVABLE(const MVC_OBSERVABLE &observable)
//{
////    m_observersList = observable.m_observersList;
//    std::copy(observable.m_observersList.begin(),observable.m_observersList.end(),std::inserter(m_observersList,m_observersList.begin()));
//    std::cout << "MVC_OBSERVABLE copy constructor called" << std::endl;
//}
