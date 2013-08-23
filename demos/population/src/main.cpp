#include <iostream>
#include <memory>
#include <QApplication>

#include "Utils.hpp"
#include "MainView.hpp"
#include "Maths.hpp"





int main(int argc, char **argv) {
    QApplication app(argc,argv);
    std::unique_ptr<MainWindow> mw (new MainWindow());
//     maths::RandomNormalFloatGenerator rnd(8,0.01);
//     for(int i = 1 ; i <= 10;++i)
//       SHOW(rnd());
    utils::NameFactory nf;
    
    for(int i=0; i <= 10; ++i)
      std::cout << nf.randomFemaleName() << " " << nf.randomLastName() << std::endl ;
    std::flush(std::cout);
//     maths::RandomIntGenerator rndi(0,10);
//     for(int i=0;i<=100;++i)
//       SHOW(rndi());
    mw->show();
    
    return app.exec();
}
