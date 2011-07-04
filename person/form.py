# -*- coding: utf-8 -*-
import os, sys
import codecs

import sqlite3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from common.lib import *

class Tab_PersonCommonInfo(QWidget): 
    def __init__(self, parent, personid=None): 
        QWidget.__init__(self, parent)

        self.id = QLineEdit()
        self.id.setAlignment(Qt.AlignRight)
        self.id.setEnabled(False)

        self.name1 = QLineEdit()
        self.name1.setMaxLength(80)
        self.name2 = QLineEdit()
        self.name2.setMaxLength(80)
        self.name3 = QLineEdit()
        self.name3.setMaxLength(80)

        self.gender = QButtonGroup()
        self.gender.male   = QRadioButton(u"муж.")
        self.gender.female = QRadioButton(u"жен.")
        self.gender.addButton(self.gender.male,   0)
        self.gender.addButton(self.gender.female, 1)

        self.layout_h0 = QHBoxLayout()
        self.layout_h0.addWidget(self.gender.male)
        self.layout_h0.addWidget(self.gender.female)
        self.layout_h0.addStretch(1)

        self.bornplace  = QTextEdit()
        self.bornplace.setFixedHeight(40)

        self.born = LDateEditCheckBox()
        self.dead = LDateEditCheckBox()

        self.layout = QFormLayout()
        self.layout.addRow(u"ID:",             self.id       )
        self.layout.addRow(u"Фамилия:",        self.name1    )
        self.layout.addRow(u"Имя:",            self.name2    )
        self.layout.addRow(u"Отчество:",       self.name3    )
        self.layout.addRow(u"Пол:",            self.layout_h0)
        self.layout.addRow(u"Место рождения:", self.bornplace)
        self.layout.addRow(u"Дата рождения:",  self.born     )
        self.layout.addRow(u"Дата смерти:",    self.dead     )
        self.setLayout(self.layout)

        self.load(personid)

        self.connect(self.name3, SIGNAL("editingFinished()"), self.action_name3_editingFinished)

    def action_name3_editingFinished(self):
        name3 = unicode(self.name3.text())
        if name3.endswith(u'вич'):
           self.gender.male.setChecked(True)
        elif name3.endswith(u'вна'):
           self.gender.female.setChecked(True)

    def clear(self):
        pass

    def load(self, personid):
        if personid is not None:
           conn = sqlite3.connect(os.path.join('db', 'hospital.db'))

           cur = conn.cursor()
           cur.execute("SELECT id, ifnull(name1, ''), ifnull(name2, ''), ifnull(name3, ''), gender, ifnull(bornplace, ''), born, dead FROM person WHERE id=?", (personid,))

           for row in cur:
               self.id.setText(unicode(row[0]))
               self.name1.setText(unicode(row[1]))
               self.name2.setText(unicode(row[2]))
               self.name3.setText(unicode(row[3]))
               self.gender.male.setChecked(unicode(row[4]) == 'M')
               self.gender.female.setChecked(unicode(row[4]) == 'F')
               self.bornplace.setText(unicode(row[5]))
               self.born.setDate(unicode(row[6]), '%Y-%m-%d')
               self.dead.setDate(unicode(row[7]), '%Y-%m-%d')


           conn.close()

    def check(self): 
        if len(unicode(self.name1.text()) + unicode(self.name2.text()) + unicode(self.name3.text())) == 0:
           QMessageBox().information(self, u"Внимание!", u'Не указано имя!')
           return False

        if not (self.gender.male.isChecked() or self.gender.female.isChecked()):
           QMessageBox().information(self, u"Внимание!", u'Выберите пол!')
           return False

        if not (self.born.checkbox.isEnabled()):
           QMessageBox().information(self, u"Внимание!", u'Укажите дату рождения!')
           return False

        return True

    def save(self, conn, personid=None): 
        if self.gender.male.isChecked():
           gender = 'M'
        elif self.gender.female.isChecked():
           gender = 'F'


        if personid is None:
           values = (unicode(self.name1.text()), 
                     unicode(self.name2.text()), 
                     unicode(self.name3.text()), 
                     gender, 
                     unicode(self.bornplace.toPlainText()), 
                     self.born.date.date().toPyDate() if self.born.checkbox.isEnabled() else None,
                     self.dead.date.date().toPyDate() if self.dead.checkbox.isEnabled() else None
                     )                                                	
           conn.execute('INSERT INTO person (name1, name2, name3, gender, bornplace, born, dead) VALUES (?,?,?,?,?,?,?)', values)
        else:
           values = (unicode(self.name1.text()), 
                     unicode(self.name2.text()), 
                     unicode(self.name3.text()), 
                     gender, 
                     unicode(self.bornplace.toPlainText()), 
                     self.born.date.date().toPyDate() if self.born.checkbox.isEnabled() else None,
                     self.dead.date.date().toPyDate() if self.dead.checkbox.isEnabled() else None,
                     personid
                     )                                                	
           conn.execute('UPDATE person SET name1 = ?, name2 = ?, name3 = ?, gender = ?, bornplace = ?, born = ?, dead = ? WHERE id = ?', values)

        return True


class Tab_PersonAddress(QWidget): 
    def __init__(self, parent, personid=None): 
        QWidget.__init__(self, parent)

        self.address_legal = QTextEdit()
        self.address_legal.setFixedHeight(80)

        self.address_fact = QTextEdit()
        self.address_fact.setFixedHeight(80)

        self.copy = QPushButton(u'Копировать')
        self.copy.setIcon(QIcon(os.path.join('pic', 'arrow_down_16.png')))

        self.layout = QFormLayout()
        self.layout.addRow(u"Прописки:",           self.address_legal)
        self.layout.addRow(u"",                    self.copy )
        self.layout.addRow(u"Фактич. проживания:", self.address_fact )
        self.setLayout(self.layout)

        self.load(personid)

        self.connect(self.copy, SIGNAL("clicked()"), self.action_copy)

    def action_copy(self):
        address_legal = unicode(self.address_legal.toPlainText())
        if len(address_legal) == 0:
           return

        if len(unicode(self.address_fact.toPlainText())) <> 0:
           if QMessageBox().question(self, u"Внимание!", u'Поле "Адрес фактического проживания" заполнено! Продолжить?', u"Да", u"Нет") == 0:
              self.address_fact.setPlainText(address_legal)

    def clear(self):
        pass

    def load(self, personid):
        if personid is not None:
           pass

    def check(self): 
        return True

    def save(self, conn, personid=None): 
        return True


class Tab_PersonDocuments(QWidget): 
    def __init__(self, parent, personid=None): 
        QWidget.__init__(self, parent)

        self.idntdoc = QGroupBox(u"Идентификационный документ")
        self.idntdoc.setCheckable(True)
        self.idntdoc.setChecked(False)

        self.idntdoc.type  = QComboBox()
        self.idntdoc.type.setMaximumWidth(250)
        self.idntdoc.type.datastore = [[],[],[]]
        try:
           conn = sqlite3.connect(os.path.join('db', 'dictionares.db'))

           cur = conn.cursor()
           cur.execute('SELECT id, name, mask FROM identdoc_type ORDER BY id')

           for row in cur:
               self.idntdoc.type.datastore[0].append(row[0])
               self.idntdoc.type.datastore[1].append(row[1])
               self.idntdoc.type.datastore[2].append(row[2])

               self.idntdoc.type.addItem(row[1])

        except:
          pass

        self.idntdoc.series = QLineEdit()
        self.idntdoc.series.setInputMask('00 00')

        self.idntdoc.number = QLineEdit()
        self.idntdoc.number.setInputMask('000000')

        self.idntdoc.issued_date = LDateEditCheckBox()

        self.idntdoc.issuer      = QTextEdit()
        self.idntdoc.issuer.setFixedHeight(40)

        self.idntdoc.issuer_code = QLineEdit()
        self.idntdoc.issuer_code.setInputMask('000-000')

        self.idntdoc.layout = QFormLayout()
        self.idntdoc.layout.addRow(u"Тип:",               self.idntdoc.type       )
        self.idntdoc.layout.addRow(u"Серия:",             self.idntdoc.series     )
        self.idntdoc.layout.addRow(u"Номер:",             self.idntdoc.number     )
        self.idntdoc.layout.addRow(u"Дата выдачи:",       self.idntdoc.issued_date)
        self.idntdoc.layout.addRow(u"Подразделение:",     self.idntdoc.issuer     )
        self.idntdoc.layout.addRow(u"Код подразделения:", self.idntdoc.issuer_code)
        self.idntdoc.setLayout(self.idntdoc.layout)

        self.pensdoc = QGroupBox(u"Пенсионное удостоверение")
        self.pensdoc.setCheckable(True)
        self.pensdoc.setChecked(False)
        self.pensdoc.number = QLineEdit()
        self.pensdoc.layout = QFormLayout()
        self.pensdoc.layout.addRow(u"Номер:", self.pensdoc.number)
        self.pensdoc.setLayout(self.pensdoc.layout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.idntdoc)
        self.layout.addWidget(self.pensdoc)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

        self.load(personid)

    def clear(self):
        pass

    def load(self, personid):
        if personid is not None:
           pass

    def check(self): 
        return True

    def save(self, conn, personid=None): 
        return True

class MedicalPolis(QGroupBox):
    def __init__(self, name): 
        QGroupBox.__init__(self)

        self.setTitle(name)
        self.setCheckable(True)
        self.setChecked(False)
        self.series  = QLineEdit()
        self.number  = QLineEdit()
        self.ensuer  = QTextEdit()
        self.ensuer.setFixedHeight(40)
        self.begdate = LDateEditCheckBox()
        self.enddate = LDateEditCheckBox()

        self.layout = QFormLayout()
        self.layout.addRow(u"Серия:",                   self.series )
        self.layout.addRow(u"Номер:",                   self.number )
        self.layout.addRow(u"Страховая компания:",      self.ensuer )
        self.layout.addRow(u"Дата начала действия:",    self.begdate)
        self.layout.addRow(u"Дата окончания действия:", self.enddate)
        
        self.setLayout(self.layout)
    

class SNILS(QLineEdit):
    def __init__(self, parent=None): 
        QLineEdit.__init__(self, parent)

        self.setInputMask('000-000-000 00')

        self.connect(self, SIGNAL("editingFinished()"), self.check)

    def calcSNILSkey(self):
        if int(self.norm_number()[:3]) <= 1 and int(self.norm_number()[4:6]) <= 1 and int(self.norm_number()[7:9]) <= 998:
           return self.norm_number()[10:]

        key = 0
        for i, k in enumerate(self.norm_number()[:9]):
            key += int(k)*(len(self.norm_number()[:9])-i)

        if   key < 100:  key = str(key)
        elif key >= 100: key = str(key%101)

        return key.zfill(2)

    def norm_number(self):
        return unicode(self.text()).replace("-", "").replace(" ", "")

    def check(self):
        if (self.norm_number() is not None and len(self.norm_number()) <> 0) and (len(self.norm_number()) < 11 or self.calcSNILSkey() <> self.norm_number()[9:]):
           QMessageBox().information(self, u"Внимание!", u'Контрольное число СНИЛС не соответствует алгоритму проверки!')


class Tab_PersonEnsure(QWidget): 
    def __init__(self, parent, personid=None): 
        QWidget.__init__(self, parent)

        self.snils = QGroupBox(u"Страховой номер индивидуального лицевого счета")
        self.snils.setCheckable(True)
        self.snils.setChecked(False)
        self.snils.number = SNILS()

        self.snils.layout = QHBoxLayout()
        self.snils.layout.addWidget(QLabel(u"СНИЛС:"))
        self.snils.layout.addWidget(self.snils.number)
        self.snils.layout.addStretch(1)
        self.snils.setLayout(self.snils.layout)

        self.oms_polis = MedicalPolis(u"Полис обязательного медицинского страхования")
        self.dms_polis = MedicalPolis(u"Полис добровольного медицинского страхования")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.snils)
        self.layout.addWidget(self.oms_polis)
        self.layout.addWidget(self.dms_polis)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

        self.load(personid)

    def clear(self):
        pass

    def load(self, personid):
        if personid is not None:
           pass

    def check(self): 
        return True

    def save(self, conn, personid=None): 
        return True

class WidgetPersonCard(QTabWidget): 
    def __init__(self, personid=None): 
        QTabWidget.__init__(self)

        self.personid  = personid

        self.setTabPosition(QTabWidget.North)

        self.tab_Comm = self.addTab(Tab_PersonCommonInfo(self, personid), u"Основная информация")
        self.tab_Addr = self.addTab(Tab_PersonAddress(self, personid)   , u"Адреса"             )
        self.tab_Docs = self.addTab(Tab_PersonDocuments(self, personid) , u"Документы"          )
        self.tab_Ensr = self.addTab(Tab_PersonEnsure(self, personid)    , u"Страховка"          )

    def load(self, personid): 
        if personid is not None:
           self.widget(self.tab_Comm).load(personid)
           self.widget(self.tab_Addr).load(personid)
           self.widget(self.tab_Docs).load(personid)
           self.widget(self.tab_Ensr).load(personid)

    def check(self): 
        return (self.widget(self.tab_Comm).check() and
                self.widget(self.tab_Addr).check() and
                self.widget(self.tab_Docs).check() and
                self.widget(self.tab_Ensr).check())

    def save(self): 
        state = False

        if self.check():
           conn = sqlite3.connect(os.path.join('db', 'hospital.db'))

           if not (self.widget(self.tab_Comm).save(conn, self.personid) and
                   self.widget(self.tab_Addr).save(conn, self.personid) and
                   self.widget(self.tab_Docs).save(conn, self.personid) and
                   self.widget(self.tab_Ensr).save(conn, self.personid)):
              QMessageBox().warning(self, u"Ошибка!", u'Ошибка при сохранении!')
           else:
              conn.commit()

              cur = conn.cursor()
              cur.execute('SELECT last_insert_rowid()')
              self.widget(self.tab_Comm).id.setText(str(cur.fetchone()[0]))

              state = True

           conn.close()

        return state

class WindowPersonCard(QMainWindow): 
    def __init__(self, parent, personid=None): 
        QMainWindow.__init__(self, parent)

        self.setWindowTitle(u'Карточка пациента')

        self.widget = WidgetPersonCard(personid)

        tb = QToolBar(u'Главное');
        tb.addAction(QIcon(os.path.join('pic', 'save_32.png')), u'Сохранить')
        self.addToolBar(tb)

        self.setCentralWidget(self.widget)

    def action_save(self): 
        save_state = QMessageBox().question(self, u"Внимание!", u'Сохранить изменения?', u"Да", u"Нет")
        if save_state == 0:
           self.widget.save()

