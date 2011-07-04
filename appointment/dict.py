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

class AppointmentDictList(LTableWidget): 
    def __init__(self, editable=False, parent=None): 
        LTableWidget.__init__(self, parent)

        if not editable:
           self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.addColumn(name=u'id',   title=u'ID',           datatype=DT_INTEGER, alignment=Qt.AlignRight, editable=False)
        self.addColumn(name=u'name', title=u'Наименование', datatype=DT_STRING,  alignment=Qt.AlignLeft , editable=editable)
        if editable:
           self.addColumn(name=u'dosage', title=u'Дозировка', datatype=DT_STRING,  alignment=Qt.AlignLeft, editable=editable)


        sql = """SELECT id, name, dosage   
                   FROM appointments_dict  
                  WHERE type = 1           
                  ORDER BY name ASC """ 
        
        self.loadDatastore(sqlite3.connect(os.path.join('db', 'dictionares.db')), sql)

        if editable:
           self.connect(self, SIGNAL('itemDoubleClicked(QTableWidgetItem *)'),                     self.ev_itemDoubleClicked)
           self.connect(self, SIGNAL('currentItemChanged(QTableWidgetItem *,QTableWidgetItem *)'), self.ev_currentItemChanged)
        
    def searchItem(self, text):
        rowNum = 0
        while rowNum < self.rowCount():
            item = self.item(rowNum, 1)
            if unicode(item.text()).upper().startswith(text.upper()):
               return item
            rowNum+=1

        return None

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/pubmedrecord"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
                                               
    def startDrag(self, event):
        mimeData = QMimeData()
        bstream = cPickle.dumps(self.datastore[self.item(self.selectedIndexes()[0].row(), 0).datastoreRowNum])
        mimeData.setData("application/pubmedrecord", bstream)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        result = drag.start(Qt.MoveAction)


class AppointmentDictListWithSearchLine(QWidget): 
    def __init__(self, editable=False, parent=None): 
        QWidget.__init__(self, parent)

        self.searchline = QLineEdit()
        self.list       = AppointmentDictList(editable)

        layout = QVBoxLayout()
        layout.addWidget(self.searchline)
        layout.addWidget(self.list)

        self.setLayout(layout)

        self.connect(self.searchline, SIGNAL('textChanged(const QString&)'), self.searchtextChanged)

    def searchtextChanged(self, text):
        item = None
        if len(text) != 0:
           item = self.list.searchItem(unicode(text))

        self.list.setCurrentItem(item)
        self.list.scrollToItem(item)



class WindowAppointmentDictList(QMainWindow): 
    def __init__(self, parent=None): 
        QMainWindow.__init__(self, parent)

        self.setWindowTitle(u"Справочник назначений")

        self.setMinimumWidth(600)
        self.setMinimumHeight(600)

        self.widget = AppointmentDictListWithSearchLine(True)

        self.setCentralWidget(self.widget)
