# -*- coding: utf-8 -*-
import os, sys
import codecs

import sqlite3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from common.lib import *

class MedcardForm(QMainWindow): 
    def __init__(self, parent=None): 
        QMainWindow.__init__(self, parent)
        
        QMessageBox().message(self, u"Здесь!")

class WindowMedcardList(QMainWindow): 
    def __init__(self, medcardid=0, parent=None): 
        QMainWindow.__init__(self, parent)

        if medcardid == 0:
           if QMessageBox().question(self, u"Внимание!", u'У пациента отсутствует амбулаторная карта! Создать?', u"Да", u"Нет") == 0:
              MedcardForm()

