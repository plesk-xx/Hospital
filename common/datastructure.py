# -*- coding: utf-8 -*-
import sqlite3

class dataStructure():
   def __init__(self, _dbFile, _tableName, _query=None, _autocommit=False):
       self.autocommit = False

       self.dbFile     = _dbFile
       self.tableName  = _tableName
       self.query      = _query
       self.connection = sqlite3.connect(self.dbFile)

       self.rec = {}

       if not self.getRecord():
          print "Cannot get record"

   def commit(self):
       self.connection.commit()

   def getRecord(self):
       if self.query is None:
          return True

       try:
          self.connection.row_factory = sqlite3.Row
          cur = self.connection.cursor()
          cur.execute("SELECT * FROM {0} WHERE 1 = 1 AND {1}".format(self.tableName, self.query))

          for row in cur:
              self.rec = {}
              for i, r in enumerate(row):
                  self.rec[row.keys()[i]] = r
              break

          return True
       except:
          return False

   def insert(self):
       try:
          if len(self.rec) == 0:
             return False

          tmp = map(str, self.rec.keys())

          self.connection.execute("INSERT INTO {0} ({1}) VALUES ({2})".format(self.tableName, ", ".join(tmp), ":" + ", :".join(tmp)), self.rec)

          if self.autocommit:
             self.commit()

          return True
       except:
          return False

   def delete(self):
       if self.query is None:
          return True

       try:
          if len(self.rec) == 0:
             return False

          self.connection.execute("DELETE FROM {0} WHERE {1}".format(self.tableName, self.query), self.rec)

          if self.autocommit:
             self.commit()

          return True
       except:
          return False

   def update(self):
       if self.query is None:
          return True

       try:
          if len(self.rec) == 0:
             return False

          s = ""
          for i in map(str, self.rec.keys()):
              if len(s) <> 0:
                 s += ", "
              s += "{0}=:{1}".format(i, i)

          self.connection.execute("UPDATE {0} SET {1} WHERE {2}".format(self.tableName, s, self.query), self.rec)

          if self.autocommit:
             self.commit()

          return True
       except:
          return False
