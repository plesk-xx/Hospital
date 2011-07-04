# -*- coding: utf-8 -*-
import os, sys

import sqlite3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from common.const import *

class LProgressBar(QProgressDialog): 
    def __init__(self, parent=None):
        QProgressDialog.__init__(self, parent)

    def init(self, text, minval, maxval):
        self.show()

        self.setWindowTitle(text)
        self.setMinimum(minval)
        self.setMaximum(maxval)

    def use(self, value):
        self.setValue(value)

class LDateEdit(QDateEdit): 
    def __init__(self, parent=None, s=None, f=None): 
        QDateEdit.__init__(self, parent)

        self.setDisplayFormat("dd.MM.yyyy")
        self.setCalendarPopup(True)

        CalendarWidget = QCalendarWidget()
        CalendarWidget.setFirstDayOfWeek(1)

        self.setCalendarWidget(CalendarWidget)

        if s is not None and f is not None:
           self.setDateFromString(s, f)

    def setDateFromString(self, s, f):
        from datetime import datetime

        if s is not None and len(s) > 0:
           dt = datetime.strptime(s, f)
           self.setDate(QDate(dt.year, dt.month, dt.day))


class LDateEditCheckBox(QWidget): 
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)

        self.date     = LDateEdit()
        self.checkbox = QCheckBox()

        self.date.setEnabled(False)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.date)
        self.layout.addWidget(self.checkbox)
        self.layout.addStretch(1)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.connect(self.checkbox, SIGNAL("toggled(bool)"), self.action_checkbox)

    def setDate(self, s, f):
        if s is not None and len(s) > 0:
           self.date.setDateFromString(s, f)
           self.checkbox.setChecked(True)

    def action_checkbox(self): 
        self.date.setEnabled(self.checkbox.isChecked())

class LCommonList(QTreeWidget): 
    def __init__(self, parent=None): 
        QTreeWidget.__init__(self, parent)

        self.setSortingEnabled(True)

        self.ColumnCard   = []
        self.ColumnLabels = QStringList()
        self.datastore = []

    def addColumn(self, title, datatype, alignment=Qt.AlignHCenter):
        self.ColumnCard.append({"title":title, "datatype": datatype, "alignment": alignment})
        self.ColumnLabels.append(title)

        self.setColumnCount(len(self.ColumnCard))
        self.setHeaderLabels(self.ColumnLabels)

    def loadDatastore(self, connection, query):
        self.datastore = []

        cur = connection.cursor()
        cur.execute(query)

        for i, row in enumerate(cur):
            self.datastore.append(row)

        self.setDatastore()

    def setDatastore(self):
        for row in self.datastore:
            item = QTreeWidgetItem(self)

            for i, column in enumerate(row):
                item.setText(i, unicode(column))
                item.setTextAlignment(i, self.ColumnCard[i]["alignment"])


class LTableWidgetLineEdit(QLineEdit): 
    def __init__(self, item, value=None): 
        QLineEdit.__init__(self)

        self.item = item

        self.setText(value)

        self.connect(self, SIGNAL('returnPressed()'), self.ev_returnPressed)

    def ev_returnPressed(self):
        self.item.setText(self.text())
        self.item.tableWidget().closePersistentEditor(self.item)

class LTableWidgetSpinBox(QSpinBox): 
    def __init__(self, item, value=None): 
        QSpinBox.__init__(self)

        self.item = item

        self.setValue(int(value))

        self.connect(self, SIGNAL('editingFinished()'), self.ev_editingFinished)

    def ev_editingFinished(self):
        self.item.setText(str(self.value()))
        self.item.tableWidget().closePersistentEditor(self.item)


class LTableWidget(QTableWidget): 
    def __init__(self, *args): 
        QTableWidget.__init__(self, *args)

        self.setSortingEnabled(True)

        self.ColumnCard   = []
        self.ColumnLabels = QStringList()
        self.datastore = []

        self.setDragEnabled(True)

        self.connect(self, SIGNAL('itemDoubleClicked(QTableWidgetItem *)'),                     self.ev_itemDoubleClicked)
        self.connect(self, SIGNAL('currentItemChanged(QTableWidgetItem *,QTableWidgetItem *)'), self.ev_currentItemChanged)

    def ev_itemDoubleClicked(self, item):
        if self.ColumnCard[item.column()]["editable"]:
           self.setCellWidget(item.row(), item.column(), eval(self.ColumnCard[item.column()]["classname"]+"(item, item.text())"))
           self.openPersistentEditor(item)

    def ev_currentItemChanged(self, item_old, item_new):
        if item_new is not None:
           if self.ColumnCard[item_new.column()]["editable"]:
              self.closePersistentEditor(item_new)

    def getColumnNum(self, name=None, title=None):
        for i, ColumnCardElement in enumerate(self.ColumnCard):
            if name is not None:
               if ColumnCardElement["name"]  == name: return i
            elif title is not None:
               if ColumnCardElement["title"] == title: return i
        return -1

    def addColumn(self, name, title, datatype, alignment=Qt.AlignHCenter, width=None, editable=False, classname=None):
        v_classname = classname
        if v_classname is None:
           if   datatype == DT_STRING:  v_classname = "LTableWidgetLineEdit"
           elif datatype == DT_INTEGER: v_classname = "LTableWidgetSpinBox"

        self.ColumnCard.append({"name":name, "title":title, "datatype": datatype, "alignment": alignment, "width": width, "editable":editable, "classname":v_classname})
        self.ColumnLabels.append(title)

        self.setColumnCount(len(self.ColumnCard))
        self.setHorizontalHeaderLabels(self.ColumnLabels)

    def loadDatastore(self, connection, query):
        self.datastore = []

        connection.row_factory = sqlite3.Row
        cur = connection.cursor()
        cur.execute(query)

        for row in cur:
            datastore_row = {}
            for i, r in enumerate(row):
                datastore_row[row.keys()[i]] = r
            self.datastore.append(datastore_row)

        self.setDatastore()

    def setDatastore(self):
        for j, row in enumerate(self.datastore):
            self.setRowCount(j+1)
            for i, ColumnCardElement in enumerate(self.ColumnCard):
                if self.datastore[j][ColumnCardElement["name"]] is not None:
                   item = QTableWidgetItem(unicode(self.datastore[j][ColumnCardElement["name"]]))
                   item.datastoreRowNum = j
                   item.setTextAlignment(ColumnCardElement["alignment"])
                   item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsEnabled)
                   self.setItem(j, i, item)

        for i, ColumnCardElement in enumerate(self.ColumnCard):
            if ColumnCardElement["width"] is not None:
               self.setColumnWidth(i, ColumnCardElement["width"])
            else:
               self.resizeColumnToContents(i)

        self.resizeRowsToContents()


class LToolButtonMenu(QToolButton):
    def __init__(self, parent=None): 
        QToolButton.__init__(self, parent)

        self.setPopupMode(QToolButton.MenuButtonPopup)
        self.setMenu(QMenu(self))

        self.connect(self.menu(), SIGNAL("hovered(QAction *)"), self.setToolButtonAction)

    def addMenuAction(self, icon, text, signal=None, default=False):
        action = QAction(icon, text, self)
        if signal is not None:
           self.connect(action, SIGNAL("triggered()"), signal)

        self.menu().addAction(action)
        if default:
           self.setToolButtonAction(action)

    def setToolButtonAction(self, action):
        self.setDefaultAction(action)
