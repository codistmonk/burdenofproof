#ifndef MAIN_VIEW_HPP
#define MAIN_VIEW_HPP

#include "ui_mainWindow.h"

class MainWindow final : public QMainWindow {
  Q_OBJECT
  
public:
  MainWindow() ;
  virtual ~MainWindow();
private:
//   void init();
  
private:
  Ui::MainWindow	m_mainUI;
};














#endif