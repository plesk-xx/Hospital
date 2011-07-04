# -*- coding: utf-8 -*-
import os, sys
import codecs

import datetime

import sqlite3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from common.lib import *
from common.const import *
from person.form import *
from medcard.list import *


def GetFullName(name1, name2, name3):
    def addName(fullname, name):
        if name is not None and name <> "":
           if len(fullname) <> 0:
              fullname += " "
           fullname += name
        return fullname
    return addName(addName(addName("", name1), name2), name3)

class PersonList(LTableWidget): 
    def __init__(self, parent=None): 
        LTableWidget.__init__(self, parent)

        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.addColumn(name=u'name1',     title=u'Фамилия',           datatype=DT_STRING, editable=False)
        self.addColumn(name=u'name2',     title=u'Имя',               datatype=DT_STRING, editable=False)
        self.addColumn(name=u'name3',     title=u'Отчество',          datatype=DT_STRING, editable=False)
        self.addColumn(name=u'usnumber',  title=u'Амбулаторная карта',datatype=DT_STRING, editable=False)
        self.addColumn(name=u'id',        title=u'ID пациента',       datatype=DT_INTEGER, alignment=Qt.AlignRight, editable=False)
        self.addColumn(name=u'medcardid', title=u'ID амб. карты',     datatype=DT_INTEGER, alignment=Qt.AlignRight, editable=False)

        sql = """SELECT ifnull(p.name1, '') name1, ifnull(p.name2, '') name2,     
                        ifnull(p.name3, '') name3, ifnull(m.usnumber, '') usnumber,  
                        ifnull(p.id, 0) id, ifnull(m.medcardid, 0) medcardid
                   FROM      person as p                              
                   LEFT JOIN medcard as m                             
                     ON p.id = m.personid                             
                  ORDER BY p.id """ 
        
        self.loadDatastore(sqlite3.connect(os.path.join('db', 'hospital.db')), sql)
        
        self.connect(self, SIGNAL('itemDoubleClicked(QTableWidgetItem *)'), self.doubleClick)
        
    def doubleClick(self, item):
        pc = WindowPersonCard(self, int(self.item(item.row(), self.getColumnNum(name="id")).text()))
        pc.show()

class WindowPersonList(QMainWindow): 
    def __init__(self, parent=None): 
        QMainWindow.__init__(self, parent)

        self.setWindowTitle(u"Пациенты")

        self.setMinimumWidth(600)
        self.setMinimumHeight(600)

        tb = QToolBar(u'Главное');
        tb.addAction(QIcon(os.path.join('pic', 'user_add_32.png')),   u'Новый', self.action_create)
        tb.addAction(QIcon(os.path.join('pic', 'user_close_32.png')), u'Удалить')
        tb.addSeparator()
        tb.addAction(QIcon(os.path.join('pic', 'book_bookmarks_32.png')), u'История болезни', self.action_medcard)

        self.addToolBar(tb)

        self.widget = PersonList()

        self.setCentralWidget(self.widget)

    def action_create(self):
        pc = WindowPersonCard(self)
        pc.show()

    def action_medcard(self):
        ml = WindowMedcardList(self)
        ml.show()

