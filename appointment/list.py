# -*- coding: utf-8 -*-
import os, sys
import codecs

import sqlite3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import cPickle
import pickle

from common.lib import *
from common.const import *

class AppointmentList(LTableWidget): 
    def __init__(self, personid, parent=None): 
        LTableWidget.__init__(self, parent)

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.addColumn(name=u'id',   title=u'ID',           datatype=DT_INTEGER, alignment=Qt.AlignRight, editable=False)
        self.addColumn(name=u'name', title=u'Наименование', datatype=DT_STRING,  alignment=Qt.AlignLeft , editable=editable)
        self.addColumn(name=u'dosage', title=u'Дозировка', datatype=DT_STRING,  alignment=Qt.AlignLeft, editable=editable)


        sql = """SELECT id, name, dosage   
                   FROM appointments  
                  WHERE type = 1           
                  ORDER BY name ASC """ 
        
        self.loadDatastore(sqlite3.connect(os.path.join('db', 'hospital.db')), sql)

        if editable:
           self.connect(self, SIGNAL('itemDoubleClicked(QTableWidgetItem *)'),                     self.ev_itemDoubleClicked)
           self.connect(self, SIGNAL('currentItemChanged(QTableWidgetItem *,QTableWidgetItem *)'), self.ev_currentItemChanged)
        


class WindowAppointmentList(QMainWindow): 
    def __init__(self, parent=None): 
        QMainWindow.__init__(self, parent)

        self.setWindowTitle(u"Справочник назначений")

        self.setMinimumWidth(600)
        self.setMinimumHeight(600)

        self.widget = AppointmentDictListWithSearchLine(True)

        self.setCentralWidget(self.widget)
