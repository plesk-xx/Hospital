# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import cPickle
import pickle

import sqlite3

from common.lib import *
from appointment.dict import *

import datetime

class AppointmentTimePeriod(QComboBox):
    def __init__(self, currentindex=0, parent=None): 
        QComboBox.__init__(self, parent)

        query = """SELECT id, name   
                     FROM periodtime_dict  
                    ORDER BY id ASC """ 
        
        connection = sqlite3.connect(os.path.join('db', 'dictionares.db'))

        connection.row_factory = sqlite3.Row
        cur = connection.cursor()
        cur.execute(query)

        for row in cur:
            self.addItem(row["name"])

        connection.close()
        self.setCurrentIndex(currentindex)

class AppointmentTimePeriod2(QWidget):
    def __init__(self, currentindex=-1, parent=None): 
        QWidget.__init__(self, parent)

        self.combobox = QComboBox()

        self.combobox.addItem(u"")
        self.combobox.addItem(u"утром")
        self.combobox.addItem(u"днем")
        self.combobox.addItem(u"вечером")
        self.combobox.addItem(u"точно")

        self.time = QTimeEdit()

        layout = QHBoxLayout()
        layout.addWidget(self.combobox)
        layout.addWidget(self.time)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)

        self.connect(self.combobox, SIGNAL("currentIndexChanged(int)"), self.combobox_changer)

        self.combobox.setCurrentIndex(currentindex)

    def combobox_changer(self, i):
        self.time.setHidden(self.combobox.currentIndex()<>4)

        if self.combobox.currentIndex() == 0:
           self.combobox.setCurrentIndex(-1)

class AppointmentAboutEating(QComboBox):
    def __init__(self, currentindex=-1, parent=None): 
        QComboBox.__init__(self, parent)

        self.addItem(u"")
        self.addItem(u"до еды")
        self.addItem(u"после еды")
        self.addItem(u"натощак")
        self.addItem(u"с пищей")

        self.setCurrentIndex(currentindex)

        self.connect(self, SIGNAL("currentIndexChanged(int)"), self.changer)

    def changer(self, i):
        if self.currentIndex() == 0:
           self.setCurrentIndex(-1)


class AppointmentDates(QWidget):
    def __init__(self, spacing=0, parent=None): 
        QWidget.__init__(self, parent)

        self.singly = False

        self.count = QSpinBox()
        self.count.setSuffix(QString(u" дн."))
        self.count.setMinimum(1)

        self.d_from  = LDateEdit()
        self.d_till  = LDateEdit()

        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel(u"с "))
        layout1.addWidget(self.d_from)
        layout1.addWidget(QLabel(u" по "))
        layout1.addWidget(self.d_till)
        layout1.addWidget(QLabel(u" ("))
        layout1.addWidget(self.count)
        layout1.addWidget(QLabel(u")"))
        layout1.setContentsMargins(0,0,0,0)
        layout1.addStretch(1)
        self.setLayout(layout1)

        self.connect(self.d_from, SIGNAL("dateChanged(QDate)"), self.calcdate)
        self.connect(self.d_till, SIGNAL("dateChanged(QDate)"), self.calcdate)
        self.connect(self.count,  SIGNAL("valueChanged(int)"),  self.calcint)

        self.d_from.setDateFromString(datetime.datetime.now().strftime('%d.%m.%Y'), '%d.%m.%Y')
        self.d_till.setDateFromString(datetime.datetime.now().strftime('%d.%m.%Y'), '%d.%m.%Y')

    def setSingly(self, flag):
        self.singly = flag

        self.count.setDisabled(flag)
        self.d_till.setDisabled(flag)

        self.d_till.setDate(self.d_from.date())


    def calcdate(self, dt):
        if self.d_from.date().toPyDate() < datetime.date.today():
           self.d_from.setDateFromString(datetime.datetime.now().strftime('%d.%m.%Y'), '%d.%m.%Y')

        if self.d_from.date() > self.d_till.date() or self.singly:
           self.d_till.setDate(self.d_from.date())

        td = self.d_till.date().toPyDate() - self.d_from.date().toPyDate()
        self.count.setValue(int(td.days) + 1)

    def calcint(self, i):
        self.d_till.setDate(self.d_from.date().toPyDate() + datetime.timedelta(days=(self.count.value()-1)))


class AppointmentSingly(QWidget):
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addStretch(1)
        self.setLayout(layout)


class AppointmentManytimes(QWidget):
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)

        self.buttonGroup = QButtonGroup()

        self.by_count = QWidget()

        self.by_count.selected = QRadioButton()
        self.by_count.selected.setText(QString(u"по количеству: "))
        self.buttonGroup.addButton(self.by_count.selected)

        self.by_count.widget = QWidget()

        self.by_count.count  = QSpinBox()
        self.by_count.count.setSuffix(QString(u" р. в"))
        self.by_count.count.setMinimum(1)

        self.by_count.period = AppointmentTimePeriod(2)

        layout11 = QHBoxLayout()
        layout11.addWidget(self.by_count.count )
        layout11.addWidget(self.by_count.period)
        layout11.addStretch(1)
        layout11.setContentsMargins(0,0,0,0)
        self.by_count.widget.setLayout(layout11)

        layout12 = QHBoxLayout()
        layout12.addSpacing(30)
        layout12.addWidget(self.by_count.selected)
        layout12.addWidget(self.by_count.widget  )
        layout12.addStretch(1)
        layout12.setContentsMargins(0,0,0,0)
        self.by_count.setLayout(layout12)

        self.by_time  = QWidget()

        self.by_time.selected = QRadioButton()
        self.by_time.selected.setText(QString(u"по времени: "))
        self.buttonGroup.addButton(self.by_time.selected)

        self.by_time.widget = QWidget()
        self.by_time.count  = QSpinBox()
        self.by_time.count.setMinimum(1)
        self.by_time.period = AppointmentTimePeriod()

        layout21 = QHBoxLayout()
        layout21.addWidget(QLabel(u" каждые"))
        layout21.addWidget(self.by_time.count   )
        layout21.addWidget(self.by_time.period  )
        layout21.addStretch(1)
        layout21.setContentsMargins(0,0,0,0)
        self.by_time.widget.setLayout(layout21)

        layout22 = QHBoxLayout()
        layout22.addSpacing(30)
        layout22.addWidget(self.by_time.selected)
        layout22.addWidget(self.by_time.widget  )
        layout22.addStretch(1)
        layout22.setContentsMargins(0,0,0,0)
        self.by_time.setLayout(layout22)

        layout = QVBoxLayout()
        layout.addWidget(self.by_count)
        layout.addWidget(self.by_time )
        layout.setContentsMargins(0,0,0,0)
        layout.addStretch(1)
        self.setLayout(layout)

        self.connect(self.by_count.selected, SIGNAL("toggled(bool)"), self.selected_toggled)
        self.connect(self.by_time.selected,  SIGNAL("toggled(bool)"), self.selected_toggled)

        self.by_count.selected.setChecked(True)

    def selected_toggled(self, b):
        self.by_count.widget.setDisabled(self.by_time.selected.isChecked())
        self.by_time.widget.setDisabled(self.by_count.selected.isChecked())


class AppointmentAppointment(QGroupBox):
    def __init__(self, parent=None): 
        QGroupBox.__init__(self, parent)
        self.parent = parent

        self.setTitle(u"Назначение")

        self.id     = 0
        self.widget = QLineEdit()
        self.widget.setMaxLength(120)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.widget)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

class AppointmentDosage(QGroupBox):
    def __init__(self, parent=None): 
        QGroupBox.__init__(self, parent)

        self.setTitle(u"Дозировка")

        self.widget = QComboBox()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.widget)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class AppointmentPeriodicity(QGroupBox):
    def __init__(self, parent=None): 
        QGroupBox.__init__(self, parent)

        self.setTitle(u"Периодичность")

        self.buttonGroup = QButtonGroup()

        self.dates   = AppointmentDates()

        self.singly   = QWidget()
        self.singly.selected = QRadioButton()
        self.singly.selected.setText(QString(u"однократно"))
        self.buttonGroup.addButton(self.singly.selected)
        self.singly.widget   = AppointmentSingly()

        self.manytimes   = QWidget()
        self.manytimes.selected = QRadioButton()
        self.manytimes.selected.setText(QString(u"многократно"))
        self.buttonGroup.addButton(self.manytimes.selected)
        self.manytimes.widget   = AppointmentManytimes()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.dates)
        self.layout.addWidget(self.singly.selected)
        self.layout.addWidget(self.singly.widget)
        self.layout.addWidget(self.manytimes.selected)
        self.layout.addWidget(self.manytimes.widget)
        self.layout.addStretch(1)

        self.setLayout(self.layout)


class AppointmentComment(QGroupBox):
    def __init__(self, parent=None): 
        QGroupBox.__init__(self, parent)

        self.setTitle(u"Комментарий")

        self.widget = QTextEdit()
        self.widget.setMinimumHeight(40)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.widget)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class WidgetAppointment(QWidget):
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)

        self.setAcceptDrops(True)

        self.appointment = AppointmentAppointment()
        self.dosage      = AppointmentDosage()
        self.periodicity = AppointmentPeriodicity()
        self.comment     = AppointmentComment()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.appointment)
        self.layout.addWidget(self.dosage)
        self.layout.addWidget(self.periodicity)
        self.layout.addWidget(self.comment)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

        self.connect(self.periodicity.singly.selected,    SIGNAL("toggled(bool)"), self.selected_toggled)
        self.connect(self.periodicity.manytimes.selected, SIGNAL("toggled(bool)"), self.selected_toggled)

        self.periodicity.manytimes.selected.setChecked(True)

    def selected_toggled(self, b):
        self.periodicity.dates.setSingly(self.periodicity.singly.selected.isChecked())

        self.periodicity.manytimes.widget.setDisabled(self.periodicity.singly.selected.isChecked())
        self.periodicity.singly.widget.setDisabled(self.periodicity.manytimes.selected.isChecked())

    def initAppointmet(self, appointmet_dict_row):
        self.appointment.id = appointmet_dict_row["id"]
        self.appointment.widget.setText(appointmet_dict_row["name"])

        self.dosage.widget.clear()
        if appointmet_dict_row["dosage"] is not None:
           for item in appointmet_dict_row["dosage"].split(";"):
               self.dosage.widget.addItem(item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/pubmedrecord"):
           self.set_bg(True)
           event.accept()
        else:
           event.reject()

    def dragLeaveEvent(self, event):
        self.set_bg(False)
        event.accept()

    def dropEvent(self, event):
        self.set_bg(False)
        data = event.mimeData()
        bstream = data.retrieveData("application/pubmedrecord", QVariant.ByteArray)
        appointmet_dict_row = pickle.loads(bstream.toByteArray())
        event.accept()
        self.initAppointmet(appointmet_dict_row)

    def set_bg(self, active = False):
        if active:
            self.appointment.widget.setStyleSheet("QLineEdit {background: yellow;}")
        else:
            self.appointment.widget.setStyleSheet("QLineEdit {background: white;}")


class WindowAppointmentForm(QMainWindow): 
    def __init__(self, appointmentid, parent=None): 
        QMainWindow.__init__(self, parent)

        self.setWindowTitle(u"Карточка назначения")

        self.widget = WidgetAppointment()
        self.status = QString(u"")
        self.initData(appointmentid)

        if not readonly:
           self.dict   = QDockWidget(QString(u"Справочник назначений"))
           self.dict.setWidget(AppointmentDictListWithSearchLine())
           self.dict.setFeatures(QDockWidget.DockWidgetVerticalTitleBar|QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetFloatable)

        self.setCentralWidget(self.widget)
        if not readonly:
           self.addDockWidget(Qt.RightDockWidgetArea, self.dict)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage(self.status)

    def initData(self, appointmentid):
        if appointmentid == 0:
           self.status = QString(u"Статус назначения: новое")
        else:
           connection = sqlite3.connect(os.path.join('db', 'hospital.db'))
           cur = connection.cursor()

           query = """SELECT d.id, d.name, a.dosage, a.type, a.datefrom, 
                             a.datetill, a.count, a.period, a.comment
                        FROM appointments as a, appointments_dict as d
                       WHERE d.type = 1
                         AND a.appointmenttypeid = d.id
                         AND a.personid = ?""" 
           cur.execute(query, (appointmentid,))

           for row in cur:
               w = self.widget
               w.appointment.id = row["id"]
               w.appointment.widget.setText(row["name"])
               w.appointment.widget.setDisabled(True)

               w.dosage.widget.clear()
               if row["dosage"] is not None:
                  w.dosage.widget.addItem(row["dosage"])
               w.dosage.widget.setDisabled(True)

               p = w.periodicity
               p.dates.d_from.setDate(row["datefrom"], '%Y-%m-%d')
               p.dates.d_till.setDate(row["dateyill"], '%Y-%m-%d')

               p.singly.selected.setChecked(row["type"] == 0)

               m = p.manytimes
               m.selected.setChecked(row["type"] <> 0)

               if   row["type"] == 1:
                    m.widget.by_count.selected(True)
                    m.widget.by_count.count.setValue(row["count"])
                    m.widget.by_count.period.setCurrentIndex(row["period"])
               elif row["type"] == 2:
                    m.widget.by_time.selected(True)
                    m.widget.by_time.count.setValue(row["count"])
                    m.widget.by_time.period.setCurrentIndex(row["period"])

               w.comment.widget.setText(row["comment"])


           connection.close()
