#include "MainView.hpp"

MainWindow::MainWindow() : QMainWindow(nullptr,0), m_mainUI(Ui::MainWindow()) {
  m_mainUI.setupUi(this); 
}

MainWindow::~MainWindow(){
}