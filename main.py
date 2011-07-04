# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from common.lib import *
from person.list import *
from person.form import *
from appointment.form import *
from appointment.dict import *

class MainWindow(QMainWindow): 
    def __init__(self, parent=None): 
        QMainWindow.__init__(self, parent)

        self.setWindowTitle(u"Hospital")

        tb = QToolBar(u'Главное');

        patientButton = LToolButtonMenu()
        patientButton.addMenuAction(QIcon(os.path.join('pic', 'users_32.png')),    u'Список пациентов', self.PatientList, True)
        patientButton.addMenuAction(QIcon(os.path.join('pic', 'user_add_32.png')), u'Новый пациент',    self.PatientForm, False)

        tb.addWidget(patientButton)

        tb.addAction(QIcon(os.path.join('pic', 'book_32.png')),             u'Истории болезни')
        tb.addAction(QIcon(os.path.join('pic', 'window_app_list_32.png')),  u'Лист назначений',       self.AppointmentForm)
        tb.addAction(QIcon(os.path.join('pic', 'page_table_32.png')),       u'Справочник назначений', self.AppointmentDictList)
                                                                              		
        self.addToolBar(tb)

    def PatientList(self):
        pl = WindowPersonList(self)
        pl.show()

    def PatientForm(self):
        pf = WindowPersonCard(self)
        pf.show()

    def AppointmentForm(self):
        af = WindowAppointmentForm(0, self)
        af.show()

    def AppointmentDictList(self):
        adl = WindowAppointmentDictList(self)
        adl.show()

if __name__ == "__main__":
   app = QApplication(sys.argv)
   win = MainWindow()
   win.show()
   sys.exit(app.exec_())                            
