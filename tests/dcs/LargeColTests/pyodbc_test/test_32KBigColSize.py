# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@


#!/bin/env python
# -*- coding:utf-8 -*-

'''
    #FileName: __file__
    #Description: Purposed to do big column size test.
    #Author: 
    #CreatedTime: 2015/04
    #LastModifiedTime: 2015/04
    #Version: Undefined
    #Copy Right (c) reserved
'''

import os
import sys
import re
import unittest
import ConfigParser
import pypyodbc
import datetime
import inspect
import logging
import time

__prefixName = "MYSQL"

def _createLogFile():
    scriptName = str(__file__).split('/')[-1].split('.')[0]
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    logFilePath = os.path.abspath(scriptPath + "../../../results/ODBC/" + scriptName)
    logFileName = scriptName + '_' + str(datetime.datetime.now()).replace(' ', '_') + '.log'   
    os.system('mkdir -p ' + logFilePath + ' 1>/dev/null 2>&1')
    return (logFilePath + '/' + logFileName)

def _getConfigParser():
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    configPath = os.path.abspath(scriptPath + "../../../config.ini")
    configParser = ConfigParser.ConfigParser()
    configParser.read(configPath)
    return configParser

def _getConnectionString():
    configParser = _getConfigParser()
    elementsList = {}
    
    for key in ("dsn", "usr", "pwd", "catalog", "schema"):
        elementsList[key] = configParser.get("pytest", key)
        
    return ('DSN=' + elementsList['dsn'] + ';UID=' + elementsList['usr'] + ';PWD=' + elementsList['pwd'])

def _getCurrentFunctionName():
    return inspect.stack()[1][3]

def _getHPDCI():
    configParser = _getConfigParser()
    elementsList = {}
    
    for key in ("host", "port", "dsn", "usr", "pwd"):
        if key == "host":
            elementsList[key] = configParser.get("pytest", "tcp").split(":")[1]
        elif key == "port":
            elementsList[key] = configParser.get("pytest", "tcp").split(":")[2]
        else:
            elementsList[key] = configParser.get("pytest", key)
    target = elementsList["host"] + ":" + elementsList["port"]

    import tests.lib.gvars as gvars
    import tests.lib.hpdci as hpdci
    hpdci.prog_parse_args_from_initfile()
    testmgr = hpdci.HPTestMgr()
    assert testmgr is not None
    dci = testmgr.create_dci_proc(__prefixName, target, elementsList["dsn"], elementsList["usr"], elementsList["pwd"])
    assert dci is not None
    return dci

class MyConnection:
    connection_string = _getConnectionString()
    
    def __init__(self):
        self.conn = None
        self.timeout = 1800
    
    def __del__(self):
        try:
            self.conn.close()
        except:
            self.conn = None
        del self.timeout
    
    def getConnection(self):
        conn = None

        try: 
            conn = pypyodbc.connect(self.__class__.connection_string, autocommit = True, timeout = self.timeout)
            if conn.connected == 1:
                conn.timeout = self.timeout
            else:
                conn = None
        except: 
            logging.debug("[*] Initialize connection failed")
        
        self.conn = conn

        return self.conn
    
    def closeConnection(self, i):
        try:
            if self.conn is None:
                pass
            elif self.conn.connected == 0:
                self.conn = None
            elif self.conn.connected == 1:
                self.conn.close()
            else:
                self.conn = None
        except:
            logging.debug("[*] Close connnection failed.")
        
        self.conn = None
    
class ScenariosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counter = 0
    
    @classmethod
    def tearDownClass(cls):
        del cls.counter
    
    @staticmethod
    def count(v):
        return (v + 1)
    
    def setUp(self):
        self.__class__.counter = self.count(self.__class__.counter)
        logging.info("================ Test Case %03d Start ================" % (self.__class__.counter))
    
    def tearDown(self):
        logging.info("================ Test Case %03d End ==================\n" % (self.__class__.counter))

    @unittest.skip("reserved")
    def testBigColumnSize_ISO0088591(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        obj = MyConnection()
        conn = obj.getConnection()
        cursor = conn.cursor()
        configParser = _getConfigParser()
        catalog = configParser.get("pytest", "catalog")
        schema = configParser.get("pytest", "schema")
        sql = "set schema " + catalog + "." + schema
        cursor.execute(sql)
        sql = "drop table if exists tblcolumnsize32kWithISO88591"
        try: 
            cursor.execute(sql)
        except pypyodbc.Error as e:
            sql = "cleanup table  tblcolumnsize32kWithISO88591";
            cursor.execute(sql)
        sql = "create table tblcolumnsize32kWithISO88591(c1 char(32000) character set iso88591 collate default null, c2 char(32000) character set iso88591 collate default null)"
        cursor.execute(sql)
        a = ""
        b = ""
        for i in range(1, 32000, 1):
            a = a + "a"
            b = b + "b"
        a = a + "E"
        b = b + "E"
        sql = "insert into tblcolumnsize32kWithISO88591(c1, c2) values('" + a + "', '" + b +"')"
        cursor.execute(sql)
        sql = "select left(rtrim(t.c1), 32000) as o1 from tblcolumnsize32kWithISO88591 as t"
        cursor.execute(sql)
        rows = cursor.fetchall()
        #print "---", rows
        print "length of the result set ", len(rows)
        self.assertEqual(len(rows), 1, 'get total rows from table wrong.')
        len_a = len(rows[0][0])
        print "length of the first column value ", len_a
        self.assertEqual(len_a, 32000, 'get length of the first column wrong.')
        self.assertEqual(rows[0][0], a, 'value wrong betwen resultset and table.')

        conn.close()
        print "[*] Passed."
    
    @unittest.skip("reserved")
    def testBigColumnSize_ISO0088591_ext(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        obj = MyConnection()
        conn = obj.getConnection()
        cursor = conn.cursor()
        configParser = _getConfigParser()
        catalog = configParser.get("pytest", "catalog")
        schema = configParser.get("pytest", "schema")
        sql = "set schema " + catalog + "." + schema
        cursor.execute(sql)
        sql = "drop table if exists tblcolumnsize32kWithISO88591_ext";
        try:
            cursor.execute(sql)
        except pypyodbc.Error as e:
            sql = "cleanup table tblcolumnsize32kWithISO88591_ext";
            cursor.execute(sql)
        sql = "create table tblcolumnsize32kWithISO88591_ext(c0 largeint not null, c1 char(32000) character set iso88591 default null, c2 char(32000) character set iso88591, c3 varchar(32000) character set iso88591 default null, c4 varchar(32000) character set iso88591, primary key(c0))"
        cursor.execute(sql)
        import random
        #space: 32
        #~: 126
        #\\: 92
        #': 39
        #": 34
        strList = []
        for i in range(32, 127, 1):
            while 1:
                x = random.randint(32, 126)
                if x != 39 and x != 32 and x != 92 and x != 34:
                    break
            strList.append(chr(x))
        v_char, v_varchar = "", ""
        for i in range(0, 32000, 1):
            v_char += random.choice(strList)
            v_varchar += random.choice(strList)
        ####
        # case 1. length is 0.
        # case 2: length is 1.
        sql = "insert into tblcolumnsize32kWithISO88591_ext(c0, c2, c4) values(?, ?, ?)"
        cursor.execute(sql, [1, v_char[0], v_varchar[0], ])
        sql = "select c0, isnull(c1, 'null'), c2, isnull(c3, 'null'), c4 from tblcolumnsize32kWithISO88591_ext where c0 = ?"
        cursor.execute(sql, [1, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1, "total rows is not 1.")
        self.assertEqual(rows[0][0], 1, "the first column value is not 1.")
        self.assertEqual(rows[0][1], 'null', "the second column is not null.")
        self.assertEqual(rows[0][2].strip(), v_char[0].strip(), "the third column is not " + v_char[0])
        self.assertEqual(rows[0][3], 'null', "the fourth column is not null.")
        self.assertEqual(rows[0][4].strip(), v_varchar[0].strip(), "the fifth column is not " + v_varchar[0])
        self.assertEqual(len(rows[0][2]), 32000, "the third column length is not 32K")
        self.assertEqual(len(rows[0][4]), 1, "the fifth column length is not 1")
        # case 3. length is 32K -1
        # case 4. length is 32K
        sql = "upsert into tblcolumnsize32kWithISO88591_ext(c0, c1, c2, c3, c4) values(?, ?, ?, ?, ?)"
        cursor.execute(sql, [2, v_char, v_char[:-1], v_varchar, v_varchar[:-1], ])
        sql = "select c0, isnull(c1, 'null'), c2, isnull(c3, 'null'), c4 from tblcolumnsize32kWithISO88591_ext where c0 = ?"
        cursor.execute(sql, [2, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1, "total rows is not 1.")
        self.assertEqual(rows[0][0], 2, "the first column value is not 1.")
        self.assertEqual(rows[0][1], v_char, "the second column is not " + v_char)
        self.assertEqual(rows[0][2].strip(), v_char[:-1].strip(), "the third column is not " + v_char[:-1])
        self.assertEqual(rows[0][3], v_varchar, "the fourth column is not " + v_varchar)
        self.assertEqual(rows[0][4].strip(), v_varchar[:-1].strip(), "the fifth column is not " + v_varchar[:-1])
        self.assertEqual(len(rows[0][1]), 32000, "the second column length is not 32K")
        self.assertEqual(len(rows[0][2]), 32000, "the third column length is not 32000") 
        self.assertEqual(len(rows[0][3]), 32000, "the fourth column length is not 32K")
        self.assertEqual(len(rows[0][4]), 31999, "the fifth column length is not 31999") 
        # case 5. length is range(2, 32K - 1)
        sql = "upsert into tblcolumnsize32kWithISO88591_ext(c0, c1, c2, c3, c4) values(?, ?, ?, ?, ?), (?, ?, ?, ?, ?), (?, ?, ?, ?, ?)"
        cursor.execute(sql, [
            1, v_char[:2], v_char[:31999], v_varchar[:2], v_varchar[:31999],
            2, v_char[:32000], v_char, v_varchar[:32000], v_varchar,
            3, v_char[:4096], v_char[:-2], v_varchar[:4096], v_varchar[:-2],
            ])
        sql = "select c0, isnull(c1, 'null'), c2, isnull(c3, 'null'), c4 from tblcolumnsize32kWithISO88591_ext where c0 > ? and c0 < ?"
        cursor.execute(sql, [0, 4, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 3, "total rows is not 3.")
        self.assertEqual(rows[0][0], 1, "the first column value is not 1.")
        self.assertEqual(rows[0][1].strip(), v_char[:2].strip(), "the second column is not " + v_char[:2])
        self.assertEqual(rows[0][2].strip(), v_char[:31999].strip(), "the third column is not " + v_char[:31999])
        self.assertEqual(rows[0][3].strip(), v_varchar[:2].strip(), "the fourth column is not " + v_varchar[:2])
        self.assertEqual(rows[0][4].strip(), v_varchar[:31999].strip(), "the fifth column is not " + v_varchar[:31999])
        self.assertEqual(len(rows[0][1]), 32000, "the second column length is not 32K")
        self.assertEqual(len(rows[0][2]), 32000, "the third column length is not 32K") 
        self.assertEqual(len(rows[0][3]), 2, "the fourth column length is not 2")
        self.assertEqual(len(rows[0][4]), 31999, "the fifth column length is not 31999") 
        self.assertEqual(rows[1][0], 2, "the first column value is not 2.")
        self.assertEqual(rows[1][1].strip(), v_char[:32000].strip(), "the second column is not " + v_char[:32000])
        self.assertEqual(rows[1][2], v_char, "the third column is not " + v_char)
        self.assertEqual(rows[1][3].strip(), v_varchar[:32000].strip(), "the fourth column is not " + v_varchar[:32000])
        self.assertEqual(rows[1][4], v_varchar, "the fifth column is not " + v_varchar)
        self.assertEqual(len(rows[1][1]), 32000, "the second column length is not 32K")
        self.assertEqual(len(rows[1][2]), 32000, "the third column length is not 32K") 
        self.assertEqual(len(rows[1][3]), 32000, "the fourth column length is not 32K")
        self.assertEqual(len(rows[1][4]), 32000, "the fifth column length is not 32K") 
        self.assertEqual(rows[2][0], 3, "the first column value is not 3.")
        self.assertEqual(rows[2][1].strip(), v_char[:4096].strip(), "the second column is not " + v_char[:4096])
        self.assertEqual(rows[2][2].strip(), v_char[:-2].strip(), "the third column is not " + v_char[:-2])
        self.assertEqual(rows[2][3].strip(), v_varchar[:4096].strip(), "the fourth column is not " + v_varchar[:4096])
        self.assertEqual(rows[2][4].strip(), v_varchar[:-2].strip(), "the fifth column is not " + v_varchar[:-2])
        self.assertEqual(len(rows[2][1]), 32000, "the second column length is not 32K")
        self.assertEqual(len(rows[2][2]), 32000, "the third column length is not 32K") 
        self.assertEqual(len(rows[2][3]), 4096, "the fourth column length is not 4096")
        self.assertEqual(len(rows[2][4]), 31998, "the fifth column length is not 31998") 
        # if delete
        sql = "delete from tblcolumnsize32kWithISO88591_ext where c4 in(?, ?)"
        cursor.execute(sql, [v_varchar, (v_varchar[:-2] + ' ' + ' ')])
        sql = "select * from tblcolumnsize32kWithISO88591_ext where c0 in (?, ?)"
        cursor.execute(sql, [2, 3, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 0, "total rows is not 0.")

        conn.close()
        print "[*] Passed."

    @unittest.skip("reserved")
    def testBigColumnSize_UTF8(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        obj = MyConnection()
        conn = obj.getConnection()
        cursor = conn.cursor()
        configParser = _getConfigParser()
        catalog = configParser.get("pytest", "catalog")
        schema = configParser.get("pytest", "schema")
        sql = "set schema " + catalog + "." + schema
        cursor.execute(sql)
        sql = "drop table if exists tblcolumnsize32kWithUTF8"
        try: 
            cursor.execute(sql)
        except pypyodbc.Error as e:
            sql = "cleanup table  tblcolumnsize32kWithUTF8";
            cursor.execute(sql)
        sql = "create table tblcolumnsize32kWithUTF8(c1 char(8000) character set utf8 collate default null, c2 char(8000) character set utf8 collate default null)"
        cursor.execute(sql)
        a = ""
        b = ""
        for i in range(1, 8000, 1):
            a = a + 'a'.encode('utf-8') 
            b = b + 'b'.encode('utf-8')
        a = a + 'E'.encode('utf-8')
        b = b + 'E'.encode('utf-8')
        sql = "insert into tblcolumnsize32kWithUTF8(c1, c2) values('" + a + "', '" + b +"')"
        cursor.execute(sql)
        sql = "select left(rtrim(t.c1), 8000) as o1 from tblcolumnsize32kWithUTF8 as t"
        cursor.execute(sql)
        rows = cursor.fetchall()
        #print "---", rows
        print "length of the result set ", len(rows)
        self.assertEqual(len(rows), 1, 'get total rows from table wrong.')
        len_a = len(rows[0][0].decode('utf-8'))
        print "length of the first column value ", len_a
        self.assertEqual(len_a, 8000, 'get length of the first column wrong.')
        self.assertEqual(rows[0][0].decode('utf-8'), a.decode('utf-8'), 'value wrong betwen resultset and table.')

        conn.close()
        print "[*] Passed."
    
    #@unittest.skip("reserved")
    def testBigColumnSize_UTF8_ext(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        obj = MyConnection()
        conn = obj.getConnection()
        cursor = conn.cursor()
        configParser = _getConfigParser()
        catalog = configParser.get("pytest", "catalog")
        schema = configParser.get("pytest", "schema")
        sql = "set schema " + catalog + "." + schema
        cursor.execute(sql)
        sql = "drop table if exists tblcolumnsize32kWithUTF8_ext";
        try:
            cursor.execute(sql)
        except pypyodbc.Error as e:
            sql = "cleanup table tblcolumnsize32kWithUTF8_ext";
            cursor.execute(sql)
        sql = "create table tblcolumnsize32kWithUTF8_ext(c0 largeint not null, c1 char(8000) character set utf8 default null, c2 char(8000) character set utf8, c3 varchar(8000) character set utf8 default null, c4 varchar(8000) character set utf8, primary key(c0))"
        cursor.execute(sql)
        import random
        #space: 32
        #~: 126
        #\\: 92
        #': 39
        #": 34
        strList = []
        for i in range(32, 127, 1):
            while 1:
                x = random.randint(32, 126)
                if x != 39 and x != 32 and x != 92 and x != 34:
                    break
            strList.append(chr(x))
        v_char, v_varchar = "", ""
        for i in range(0, 8000, 1):
            v_char += random.choice(strList).encode('utf-8')
            v_varchar += random.choice(strList).encode('utf-8')
        ####
        # case 1. length is 0.
        # case 2: length is 1.
        sql = "insert into tblcolumnsize32kWithUTF8_ext(c0, c2, c4) values(?, ?, ?)"
        cursor.execute(sql, [1, v_char[0], v_varchar[0], ])
        sql = "select c0, isnull(c1, 'null'), c2, isnull(c3, 'null'), c4 from tblcolumnsize32kWithUTF8_ext where c0 = ?"
        cursor.execute(sql, [1, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1, "total rows is not 1.")
        self.assertEqual(rows[0][0], 1, "the first column value is not 1.")
        self.assertEqual(rows[0][1], 'null', "the second column is not null.")
        self.assertEqual(rows[0][2].decode('utf-8').strip(), v_char[0].decode('utf-8').strip(), "the third column is not " + v_char[0].decode('utf-8'))
        self.assertEqual(rows[0][3], 'null', "the fourth column is not null.")
        self.assertEqual(rows[0][4].decode('utf-8').strip(), v_varchar[0].decode('utf-8').strip(), "the fifth column is not " + v_varchar[0].decode('utf-8'))
        self.assertEqual(len(rows[0][2].decode('utf-8')), 8000, "the third column length is not 32K")
        self.assertEqual(len(rows[0][4].decode('utf-8')), 1, "the fifth column length is not 1")
        # case 3. length is 32K -1
        # case 4. length is 32K
        sql = "upsert into tblcolumnsize32kWithUTF8_ext(c0, c1, c2, c3, c4) values(?, ?, ?, ?, ?)"
        cursor.execute(sql, [2, v_char, v_char[:-1], v_varchar, v_varchar[:-1], ])
        sql = "select c0, isnull(c1, 'null'), c2, isnull(c3, 'null'), c4 from tblcolumnsize32kWithUTF8_ext where c0 = ?"
        cursor.execute(sql, [2, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1, "total rows is not 1.")
        self.assertEqual(rows[0][0], 2, "the first column value is not 1.")
        self.assertEqual(rows[0][1].decode('utf-8'), v_char.decode('utf-8'), "the second column is not " + v_char.decode('utf-8'))
        self.assertEqual(rows[0][2].decode('utf-8').strip(), v_char[:-1].decode('utf-8').strip(), "the third column is not " + v_char[:-1].decode('utf-8'))
        self.assertEqual(rows[0][3].decode('utf-8'), v_varchar.decode('utf-8'), "the fourth column is not " + v_varchar.decode('utf-8'))
        self.assertEqual(rows[0][4].decode('utf-8').strip(), v_varchar[:-1].decode('utf-8').strip(), "the fifth column is not " + v_varchar[:-1].decode('utf-8'))
        self.assertEqual(len(rows[0][1].decode('utf-8')), 8000, "the second column length is not 32K")
        self.assertEqual(len(rows[0][2].decode('utf-8')), 8000, "the third column length is not 32K") 
        self.assertEqual(len(rows[0][3].decode('utf-8')), 8000, "the fourth column length is not 32K")
        self.assertEqual(len(rows[0][4].decode('utf-8')), 7999, "the fifth column length is not 31999") 
        # case 5. length is range(2, 32K - 1)
        sql = "upsert into tblcolumnsize32kWithUTF8_ext(c0, c1, c2, c3, c4) values(?, ?, ?, ?, ?), (?, ?, ?, ?, ?), (?, ?, ?, ?, ?)"
        cursor.execute(sql, [
            1, v_char[:2], v_char[:7999], v_varchar[:2], v_varchar[:7999],
            2, v_char[:8000], v_char, v_varchar[:8000], v_varchar,
            3, v_char[:4096], v_char[:-2], v_varchar[:4096], v_varchar[:-2],
            ])
        sql = "select c0, isnull(c1, 'null'), c2, isnull(c3, 'null'), c4 from tblcolumnsize32kWithUTF8_ext where c0 > ? and c0 < ?"
        cursor.execute(sql, [0, 4, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 3, "total rows is not 3.")
        self.assertEqual(rows[0][0], 1, "the first column value is not 1.")
        self.assertEqual(rows[0][1].decode('utf-8').strip(), v_char[:2].decode('utf-8').strip(), "the second column is not " + v_char[:2].decode('utf-8'))
        self.assertEqual(rows[0][2].decode('utf-8').strip(), v_char[:7999].decode('utf-8').strip(), "the third column is not " + v_char[:7999].decode('utf-8'))
        self.assertEqual(rows[0][3].decode('utf-8').strip(), v_varchar[:2].decode('utf-8').strip(), "the fourth column is not " + v_varchar[:2].decode('utf-8'))
        self.assertEqual(rows[0][4].decode('utf-8').strip(), v_varchar[:7999].decode('utf-8').strip(), "the fifth column is not " + v_varchar[:7999].decode('utf-8'))
        self.assertEqual(len(rows[0][1].decode('utf-8')), 8000, "the second column length is not 32K")
        self.assertEqual(len(rows[0][2].decode('utf-8')), 8000, "the third column length is not 32K") 
        self.assertEqual(len(rows[0][3].decode('utf-8')), 2, "the fourth column length is not 2")
        self.assertEqual(len(rows[0][4].decode('utf-8')), 7999, "the fifth column length is not 31999") 
        self.assertEqual(rows[1][0], 2, "the first column value is not 2.")
        self.assertEqual(rows[1][1].decode('utf-8').strip(), v_char[:8000].decode('utf-8').strip(), "the second column is not " + v_char[:8000].decode('utf-8'))
        self.assertEqual(rows[1][2].decode('utf-8'), v_char.decode('utf-8'), "the third column is not " + v_char.decode('utf-8'))
        self.assertEqual(rows[1][3].decode('utf-8').strip(), v_varchar[:8000].decode('utf-8').strip(), "the fourth column is not " + v_varchar[:8000].decode('utf-8'))
        self.assertEqual(rows[1][4].decode('utf-8'), v_varchar.decode('utf-8'), "the fifth column is not " + v_varchar.decode('utf-8'))
        self.assertEqual(len(rows[1][1].decode('utf-8')), 8000, "the second column length is not 32K")
        self.assertEqual(len(rows[1][2].decode('utf-8')), 8000, "the third column length is not 32K") 
        self.assertEqual(len(rows[1][3].decode('utf-8')), 8000, "the fourth column length is not 32K")
        self.assertEqual(len(rows[1][4].decode('utf-8')), 8000, "the fifth column length is not 32K") 
        self.assertEqual(rows[2][0], 3, "the first column value is not 3.")
        self.assertEqual(rows[2][1].decode('utf-8').strip(), v_char[:4096].decode('utf-8').strip(), "the second column is not " + v_char[:4096].decode('utf-8'))
        self.assertEqual(rows[2][2].decode('utf-8').strip(), v_char[:-2].decode('utf-8').strip(), "the third column is not " + v_char[:-2].decode('utf-8'))
        self.assertEqual(rows[2][3].decode('utf-8').strip(), v_varchar[:4096].decode('utf-8').strip(), "the fourth column is not " + v_varchar[:4096].decode('utf-8'))
        self.assertEqual(rows[2][4].decode('utf-8').strip(), v_varchar[:-2].decode('utf-8').strip(), "the fifth column is not " + v_varchar[:-2].decode('utf-8'))
        self.assertEqual(len(rows[2][1].decode('utf-8')), 8000, "the second column length is not 32K")
        self.assertEqual(len(rows[2][2].decode('utf-8')), 8000, "the third column length is not 32K") 
        self.assertEqual(len(rows[2][3].decode('utf-8')), 4096, "the fourth column length is not 4096")
        self.assertEqual(len(rows[2][4].decode('utf-8')), 7998, "the fifth column length is not 31998") 
        # if delete
        sql = "delete from tblcolumnsize32kWithUTF8_ext where c4 in(?, ?)"
        cursor.execute(sql, [v_varchar, (v_varchar[:-2] + ' ' + ' ')])
        sql = "select * from tblcolumnsize32kWithUTF8_ext where c0 in (?, ?)"
        cursor.execute(sql, [2, 3, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 0, "total rows is not 0.")

        conn.close()
        print "[*] Passed."

    @unittest.skip("reserved")
    def testBigColumnSize_UCS2(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        obj = MyConnection()
        conn = obj.getConnection()
        cursor = conn.cursor()
        configParser = _getConfigParser()
        catalog = configParser.get("pytest", "catalog")
        schema = configParser.get("pytest", "schema")
        sql = "set schema " + catalog + "." + schema
        cursor.execute(sql)
        sql = "drop table if exists tblcolumnsize32kWithUCS2"
        try: 
            cursor.execute(sql)
        except pypyodbc.Error as e:
            sql = "cleanup table  tblcolumnsize32kWithUCS2";
            cursor.execute(sql)
        sql = "create table tblcolumnsize32kWithUCS2(c1 char(16000) character set ucs2 collate default null, c2 char(16000) character set ucs2 collate default null)"
        cursor.execute(sql)
        a = u""
        b = u""
        for i in range(1, 16000, 1):
            a = a + unicode('a') # print sys.maxunicode, if 65535 then ucs2, if 1114111 then ucs4, manually check
            b = b + unicode('b')
        a = a + unicode('E')
        b = b + unicode('E')
        sql = "insert into tblcolumnsize32kWithUCS2(c1, c2) values('" + a + "', '" + b +"')"
        cursor.execute(sql)
        sql = "select left(rtrim(t.c1), 16000) as o1 from tblcolumnsize32kWithUCS2 as t"
        cursor.execute(sql)
        rows = cursor.fetchall()
        #print "---", rows
        print "length of the result set ", len(rows)
        self.assertEqual(len(rows), 1, 'get total rows from table wrong.')
        len_a = len(rows[0][0]) # error: length=866
        print "length of the first column value ", len_a
        self.assertEqual(len_a, 16000, 'get length of the first column wrong.')
        self.assertEqual(rows[0][0], a, 'value wrong betwen resultset and table.')

        conn.close()
        print "[*] Passed."

    @unittest.skip("reserved")
    def testBigColumnSize_UCS2_ext(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        obj = MyConnection()
        conn = obj.getConnection()
        cursor = conn.cursor()
        configParser = _getConfigParser()
        catalog = configParser.get("pytest", "catalog")
        schema = configParser.get("pytest", "schema")
        sql = "set schema " + catalog + "." + schema
        cursor.execute(sql)
        sql = "drop table if exists tblcolumnsize32kWithUCS2_ext";
        try:
            cursor.execute(sql)
        except pypyodbc.Error as e:
            sql = "cleanup table tblcolumnsize32kWithUCS2_ext";
            cursor.execute(sql)
        sql = "create table tblcolumnsize32kWithUCS2_ext(c0 largeint not null, c1 char(16000) character set ucs2 default null, c2 char(16000) character set ucs2, c3 varchar(16000) character set ucs2 default null, c4 varchar(16000) character set ucs2, primary key(c0))"
        cursor.execute(sql)
        import random
        #space: 32
        #~: 126
        #\\: 92
        #': 39
        #": 34
        strList = []
        for i in range(32, 127, 1):
            while 1:
                x = random.randint(32, 126)
                if x != 39 and x != 32 and x != 92 and x != 34:
                    break
            strList.append(chr(x))
        v_char, v_varchar = u"", u""
        for i in range(0, 16000, 1):
            v_char += unicode(random.choice(strList)) # print sys.maxunicode, if 65535 then ucs2, if 1114111 then ucs4, manually check
            v_varchar += unicode(random.choice(strList))
        ####
        # case 1. length is 0.
        # case 2: length is 1.
        sql = "insert into tblcolumnsize32kWithUCS2_ext(c0, c2, c4) values(?, ?, ?)"
        cursor.execute(sql, [1, v_char[0], v_varchar[0], ])
        sql = "select c0, isnull(c1, 'null'), c2, isnull(c3, 'null'), c4 from tblcolumnsize32kWithUCS2_ext where c0 = ?"
        cursor.execute(sql, [1, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1, "total rows is not 1.")
        self.assertEqual(rows[0][0], 1, "the first column value is not 1.")
        self.assertEqual(rows[0][1], 'null', "the second column is not null.")
        self.assertEqual(rows[0][2].strip(), v_char[0].strip(), "the third column is not " + v_char[0])
        self.assertEqual(rows[0][3], 'null', "the fourth column is not null.")
        self.assertEqual(rows[0][4].strip(), v_varchar[0].strip(), "the fifth column is not " + v_varchar[0])
        self.assertEqual(len(rows[0][2]), 16000, "the third column length is not 32K")
        self.assertEqual(len(rows[0][4]), 1, "the fifth column length is not 1")
        # case 3. length is 32K -1
        # case 4. length is 32K
        sql = "upsert into tblcolumnsize32kWithUCS2_ext(c0, c1, c2, c3, c4) values(?, ?, ?, ?, ?)"
        cursor.execute(sql, [2, v_char, v_char[:-1], v_varchar, v_varchar[:-1], ])
        sql = "select c0, isnull(c1, 'null'), c2, isnull(c3, 'null'), c4 from tblcolumnsize32kWithUCS2_ext where c0 = ?"
        cursor.execute(sql, [2, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1, "total rows is not 1.")
        self.assertEqual(rows[0][0], 2, "the first column value is not 1.")
        self.assertEqual(rows[0][1], v_char, "the second column is not " + v_char)
        self.assertEqual(rows[0][2].strip(), v_char[:-1].strip(), "the third column is not " + v_char[:-1])
        self.assertEqual(rows[0][3], v_varchar, "the fourth column is not " + v_varchar)
        self.assertEqual(rows[0][4].strip(), v_varchar[:-1].strip(), "the fifth column is not " + v_varchar[:-1])
        self.assertEqual(len(rows[0][1]), 16000, "the second column length is not 32K")
        self.assertEqual(len(rows[0][2]), 16000, "the third column length is not 32000") 
        self.assertEqual(len(rows[0][3]), 16000, "the fourth column length is not 32K")
        self.assertEqual(len(rows[0][4]), 15999, "the fifth column length is not 31999") 
        # case 5. length is range(2, 32K - 1)
        sql = "upsert into tblcolumnsize32kWithUCS2_ext(c0, c1, c2, c3, c4) values(?, ?, ?, ?, ?), (?, ?, ?, ?, ?), (?, ?, ?, ?, ?)"
        cursor.execute(sql, [
            1, v_char[:2], v_char[:15999], v_varchar[:2], v_varchar[:15999],
            2, v_char[:16000], v_char, v_varchar[:16000], v_varchar,
            3, v_char[:4096], v_char[:-2], v_varchar[:4096], v_varchar[:-2],
            ])
        sql = "select c0, isnull(c1, 'null'), c2, isnull(c3, 'null'), c4 from tblcolumnsize32kWithUCS2_ext where c0 > ? and c0 < ?"
        cursor.execute(sql, [0, 4, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 3, "total rows is not 3.")
        self.assertEqual(rows[0][0], 1, "the first column value is not 1.")
        self.assertEqual(rows[0][1].strip(), v_char[:2].strip(), "the second column is not " + v_char[:2])
        self.assertEqual(rows[0][2].strip(), v_char[:15999].strip(), "the third column is not " + v_char[:15999])
        self.assertEqual(rows[0][3].strip(), v_varchar[:2].strip(), "the fourth column is not " + v_varchar[:2])
        self.assertEqual(rows[0][4].strip(), v_varchar[:15999].strip(), "the fifth column is not " + v_varchar[:15999])
        self.assertEqual(len(rows[0][1]), 16000, "the second column length is not 32K")
        self.assertEqual(len(rows[0][2]), 16000, "the third column length is not 32K") 
        self.assertEqual(len(rows[0][3]), 2, "the fourth column length is not 2")
        self.assertEqual(len(rows[0][4]), 15999, "the fifth column length is not 31999") 
        self.assertEqual(rows[1][0], 2, "the first column value is not 2.")
        self.assertEqual(rows[1][1].strip(), v_char[:16000].strip(), "the second column is not " + v_char[:16000])
        self.assertEqual(rows[1][2], v_char, "the third column is not " + v_char)
        self.assertEqual(rows[1][3].strip(), v_varchar[:16000].strip(), "the fourth column is not " + v_varchar[:16000])
        self.assertEqual(rows[1][4], v_varchar, "the fifth column is not " + v_varchar)
        self.assertEqual(len(rows[1][1]), 16000, "the second column length is not 32K")
        self.assertEqual(len(rows[1][2]), 16000, "the third column length is not 32K") 
        self.assertEqual(len(rows[1][3]), 16000, "the fourth column length is not 32K")
        self.assertEqual(len(rows[1][4]), 16000, "the fifth column length is not 32K") 
        self.assertEqual(rows[2][0], 3, "the first column value is not 3.")
        self.assertEqual(rows[2][1].strip(), v_char[:4096].strip(), "the second column is not " + v_char[:4096])
        self.assertEqual(rows[2][2].strip(), v_char[:-2].strip(), "the third column is not " + v_char[:-2])
        self.assertEqual(rows[2][3].strip(), v_varchar[:4096].strip(), "the fourth column is not " + v_varchar[:4096])
        self.assertEqual(rows[2][4].strip(), v_varchar[:-2].strip(), "the fifth column is not " + v_varchar[:-2])
        self.assertEqual(len(rows[2][1]), 16000, "the second column length is not 32K")
        self.assertEqual(len(rows[2][2]), 16000, "the third column length is not 32K") 
        self.assertEqual(len(rows[2][3]), 4096, "the fourth column length is not 4096")
        self.assertEqual(len(rows[2][4]), 15998, "the fifth column length is not 31998") 
        # if delete
        sql = "delete from tblcolumnsize32kWithUCS2_ext where c4 in(?, ?)"
        cursor.execute(sql, [v_varchar, (v_varchar[:-2] + ' ' + ' ')])
        sql = "select * from tblcolumnsize32kWithUCS2_ext where c0 in (?, ?)"
        cursor.execute(sql, [2, 3, ])
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 0, "total rows is not 0.")

        conn.close()
        print "[*] Passed."

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=_createLogFile(),
                filemode='w')
    unittest.main()

#!END
