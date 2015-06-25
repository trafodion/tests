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
    #Description: Purposed to do multi threads loading test.
    #Author: 
    #CreatedTime: 2015/03
    #LastModifiedTime: 2015/03
    #Version: Undefined
    #Copy Right (c) reserved
'''

import os
import sys
import re
import unittest
import ConfigParser
import pypyodbc
import threading
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

class MiniClass:
    connection_string = _getConnectionString()
    global_variable = None
    
    def __init__(self, thrdsnumber = 0, circulation = 0, sqlstatement = ''):
        self.exit = False
        self.thrdspool = {}
        self.thrdsnumber = thrdsnumber
        self.circulation = circulation
        self.sqlstatement = sqlstatement
        self.lock = threading.RLock()
        self.status = "Passed"
        self.timeout = 1800
    
    def __del__(self):
        del self.exit
        self.thrdspool = {}
        del self.thrdsnumber
        del self.circulation
        del self.sqlstatement
        self.lock = None
        del self.status
        del self.timeout
    
    def bindTypeToGlobalVariable(self, v=0):
        self.__class__.global_variable = v
    
    def increaseGlobalVariable(self, step=1):
        if type(self.__class__.global_variable) is int:
            self.__class__.global_variable += step
            return self.__class__.global_variable
        elif type(self.__class__.global_variable) is list:
            self.__class__.global_variable = map(lambda v: v + step , self.__class__.global_variable)
            return ','.join(map(lambda v: str(v) , self.__class__.global_variable))
        else:
            logging.debug("[*] Failed to increase this global class variable.")
        return None
    
    def descreaseGlobalVariable():
        if type(self.__class__.global_variable) is int:
            self.__class__.global_variable -= step
            return self.__class__.global_variable
        elif type(self.__class__.global_variable) is list:
            self.__class__.global_variable = map(lambda v: v - step , self.__class__.global_variable)
            return ','.join(map(lambda v: str(v) , self.__class__.global_variable))
        else:
            logging.debug("[*] Failed to decrease this global class variable.")
        return None
    
    def initConnection(self, i):
        self.thrdspool.setdefault(i, None)
        
        for j in range(0, 100, 1):
            try:
                self.thrdspool[i] = pypyodbc.connect(self.__class__.connection_string, autocommit = True, timeout = self.timeout)
                if self.thrdspool[i].connected == 1:
                    self.thrdspool[i].timeout = self.timeout
                    break
                else:
                    self.thrdspool[i] = None
            except: 
                logging.debug("[*] Initialize connection failed, next to moniotr it.")
        
        return self.thrdspool[i]
    
    def initConnectionsWithParallel(self):
        mxxpool = {}
        
        for i in range(0, self.thrdsnumber, 1):
            t = threading.Thread(target=self.initConnection, args=[i, ])
            t.setName((i + 1))
            mxxpool.setdefault((i + 1), t)
        for i in range(0, self.thrdsnumber, 1):
            mxxpool[i + 1].setDaemon(True)
            mxxpool[i + 1].start()
        
        for i in range(0, self.thrdsnumber, 1):
            try:
                mxxpool[i + 1].join()
                mxxpool[i + 1].isAlive()
            except:
                pass
    
    def closeConnection(self, i):
        try:
            if self.thrdspool[i] is None:
                pass
            elif self.thrdspool[i].connected == 0:
                self.thrdspool[i] = None
            elif self.thrdspool[i].connected == 1:
                self.thrdspool[i].close()
            else:
                self.thrdspool[i] = None
        except:
            logging.debug("[*] Close connnection failed.")
        
        self.thrdspool[i] = None
    
    def closeConnectionsWithParallel(self):
        mxxpool = {}
        
        for i in range(0, self.thrdsnumber, 1):
            t = threading.Thread(target=self.closeConnection, args=[i, ])
            t.setName((i + 1))
            mxxpool.setdefault((i + 1), t)
        for i in range(0, self.thrdsnumber, 1):
            mxxpool[i + 1].setDaemon(True)
            mxxpool[i + 1].start()
        
        for i in range(0, self.thrdsnumber, 1):
            try:
                mxxpool[i + 1].join()
                mxxpool[i + 1].isAlive()
            except:
                pass
    
    def monitorConnections(self):
        while not self.exit:
            for i in range(0, self.thrdsnumber, 1):
                try:
                    if self.thrdspool[i] is None:
                        self.thrdspool[i] = pypyodbc.connect(self.__class__.connection_string, autocommit = True, timeout = self.timeout)
                        self.thrdspool[i].timeout = self.timeout
                    elif self.thrdspool[i].connected == 0:
                        self.thrdspool[i] = pypyodbc.connect(self.__class__.connection_string, autocommit = True, timeout = self.timeout)
                        self.thrdspool[i].timeout = self.timeout
                    elif self.thrdspool[i].connected == 1:
                        continue # nothing to do
                    else:
                        pass
                except:
                    pass #logging.debug(self.thrdspool[i].connected)
        if self.exit:
            self.closeConnectionsWithParallel()
    
    def singTrans(self, seq):
        logging.debug("[*] function %s.%s involked." % (self.__class__.__name__, _getCurrentFunctionName()))
        
        n = 0
        
        for i in range(0, self.circulation, 1):
            try:
                cursor = self.thrdspool[seq].cursor()
                if cursor is not None:
                    cursor.execute(self.sqlstatement)
                    cursor.commit()
                    n = n + 1
            except Exception as ex:
                #logging.error("ERROR: %s" % (ex.message))
                pass
        logging.debug("[*] Total %d transactions have been handled by thread %d" % (n, seq))
        if n != self.circulation:
            self.status = "Failed" # miss some transactions
    
    def multiTrans(self, seq):
        logging.debug("[*] function %s.%s involked." % (self.__class__.__name__, _getCurrentFunctionName()))
        
        n = 0
        mxsqlstatement = self.sqlstatement.split(";")
        
        for i in range(0, self.circulation, 1):
            for ss in mxsqlstatement:
                try:
                    cursor = self.thrdspool[seq].cursor()
                    if cursor is not None:
                        cursor.execute(ss)
                        cursor.commit()
                        n = n + 1
                except Exception as ex:
                    #logging.error("ERROR: %s" % (ex.message))
                    pass
        logging.debug("[*] Total %d transactions have been handled by thread %d" % (n, seq))
        if n != (self.circulation * len(mxsqlstatement)):
            self.status = "Failed" # miss some transactions
    
    def handleDelStmtSingTranstWithLock(self, seq): # not common function, only for soem case used.
        logging.debug("[*] function %s.%s involked." % (self.__class__.__name__, _getCurrentFunctionName()))
        
        n = 0

        if type(self.__class__.global_variable) is list:
            length = len(self.__class__.global_variable)
        elif type(self.__class__.global_variable) is int:
            length = 1
        else:
            length = 1
        
        for i in range(0, self.circulation, 1):
            if self.lock.acquire(100):
                try:
                    cursor = self.thrdspool[seq].cursor()
                    if cursor is not None:
                        s = self.sqlstatement + "(" + self.increaseGlobalVariable(length) + ")"
                        cursor.execute(s)
                        cursor.commit()
                        n = n + 1
                except Exception as ex:
                    #logging.error("ERROR: %s" % (ex.message))
                    pass
            self.lock.release()
        logging.debug("[*] Total %d transactions have been handled by thread %d" % (n, seq))
        if n != self.circulation:
            self.status = "Failed" # miss some transactions
    
    def singTransWithLock(self, seq):
        logging.debug("[*] function %s.%s involked." % (self.__class__.__name__, _getCurrentFunctionName()))
        
        n = 0
        
        for i in range(0, self.circulation, 1):
            if self.lock.acquire(100):
                try:
                    cursor = self.thrdspool[seq].cursor()
                    if cursor is not None:
                        cursor.execute(self.sqlstatement)
                        cursor.commit()
                        n = n + 1
                except Exception as ex:
                    #logging.error("ERROR: %s" % (ex.message))
                    pass
            self.lock.release()
        logging.debug("[*] Total %d transactions have been handled by thread %d" % (n, seq))
        if n != self.circulation:
            self.status = "Failed" # miss some transactions
    
    def multiTransWithLock(self, seq):
        logging.debug("[*] function %s.%s involked." % (self.__class__.__name__, _getCurrentFunctionName()))
        
        n = 0
        mxsqlstatement = self.sqlstatement.split(";")
        
        for i in range(0, self.circulation, 1):
            if self.lock.acquire(100):
                for ss in mxsqlstatement:
                    try:
                        cursor = self.thrdspool[seq].cursor()
                        if cursor is not None:
                            cursor.execute(ss)
                            cursor.commit()
                            n = n + 1
                    except Exception as ex:
                        #logging.error("ERROR: %s" % (ex.message))
                        pass
            self.lock.release()
        logging.debug("[*] Total %d transactions have been handled by thread %d" % (n, seq))
        if n != (self.circulation * len(mxsqlstatement)):
            self.status = "Failed" # miss some transactions
    
    def loadMultiThreads(self, pFun):
        self.initConnectionsWithParallel()
        
        mxxpool = {}
        
        t = threading.Thread(target=self.monitorConnections, args=[]) 
        t.setName(0)
        mxxpool.setdefault(0, t)
        
        for i in range(0, self.thrdsnumber, 1):
            t = threading.Thread(target=pFun, args=[i, ])
            t.setName((i + 1))
            mxxpool.setdefault((i + 1), t)
        
        mxxpool[0].setDaemon(True)
        mxxpool[0].start()
        
        dt1 = (datetime.datetime.now())
        
        for i in range(0, self.thrdsnumber, 1):
            mxxpool[i + 1].setDaemon(True)
            mxxpool[i + 1].start()
        
        for i in range(0, self.thrdsnumber, 1):
            try:
                mxxpool[i + 1].join()
                mxxpool[i + 1].isAlive()
            except:
                pass
        
        dt2 = (datetime.datetime.now())
                
        self.exit = True
        
        mxxpool[0].join()
        
        dt = (dt2 - dt1)
        tt = (dt.seconds + dt.microseconds / 1000000.0)
        
        ops = (self.thrdsnumber * self.circulation * len(self.sqlstatement.split(';')) / tt)
        
        return (self.thrdsnumber, self.circulation, tt, ops)
    
    def callLoadMultiThreads(self, pFun):
        v = self.loadMultiThreads(pFun)
        
        logging.info("[*] total_threads: %d; looping_times: %d; total_time: %.6fs; ops: %.6f/s" % (v[0], v[1], v[2], v[3]))

class MultiThreadsLoadingTestCase(unittest.TestCase):
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
    
    def singTransLine(self, n, i, s):
        o = MiniClass(n, i, s)
        o.callLoadMultiThreads(o.singTrans)
        return o.status
    
    def multiTransLine(self, n, i, s):
        o = MiniClass(n, i, s)
        o.callLoadMultiThreads(o.multiTrans)
        return o.status
    
    def singTransLineWithLock(self, n, i, s):
        o = MiniClass(n, i, s)
        o.callLoadMultiThreads(o.singTransWithLock)
        return o.status
    
    def multiTransLineWithLock(self, n, i, s):
        o = MiniClass(n, i, s)
        o.callLoadMultiThreads(o.multiTransWithLock)
        return o.status
    @unittest.skip("reserved")
    def testAllVisibleConnections(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        s = "drop table if exists TRAFODION.ODBCTEST.ODBCTESTTEST_INSERTION"
        for i in [1, 36, 72]:
            logging.info("[*] Try to start %d mxosrvrs." % (i))
            o = MiniClass(i, 1, s)
            o.loadMultiThreads(o.singTrans)
            logging.info("[*] %s" % (o.status))
    
    @unittest.skip("reserved")
    def testBoundaryValueOfVisibleConnections(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        s = "drop table if exists TRAFODION.ODBCTEST.ODBCTESTTEST_INSERTION"
        pool = [0, 1, 2, 71, 72, 73]
        for i in pool:
            logging.info("[*] Try to start %d mxosrvrs." % (i))
            o = MiniClass(i, 1, s)
            o.loadMultiThreads(o.singTrans)
            e = o.status
            if i == pool[-1]:
                if e == "Failed": e = "Passed"
            logging.info("[*] %s" % (e))
    @unittest.skip("reserved")
    def testSimpleInsertStatementGroup(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        drop_table = "drop table if exists TRAFODION.ODBCTEST.ODBCTESTTEST_INSERTION"
        o = MiniClass(1, 1, drop_table)
        o.initConnection(0)
        o.singTrans(0)
        create_table = "create table TRAFODION.ODBCTEST.ODBCTESTTEST_INSERTION (t_i largeint generated by default as identity, t_c1 varchar(20) no default not null, t_c2 int not null, t_c3 int default 20 , t_c4 timestamp default current_timestamp, primary key(t_i))"
        o.sqlstatement = create_table
        o.singTrans(0)
        o.closeConnection(0)
        s = "insert into TRAFODION.ODBCTEST.ODBCTESTTEST_INSERTION(t_c1, t_c2, t_c3) values('#inseration', 1, 28)"
        e = self.singTransLine(12, 20000, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 10000, s)
        logging.info("[*] %s" % (e))
        sa = s + ";"; sa = sa*100; sa = sa.rstrip(';')
        e = self.multiTransLine(24, 100, sa)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 200000, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(48, 100000, s)
        logging.info("[*] %s" % (e))
        sb = s + ";"; sb = sb*250; sb = sb.rstrip(';')
        e = self.multiTransLine(48, 400, sb)
        logging.info("[*] %s" % (e))

    @unittest.skip("reserved")
    def testSimpleDeleteStatementGroup(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        def getRowCount():
            s = "select count(t_i) as rowcount from TRAFODION.ODBCTEST.ODBCTESTTEST_DELETION;"
            dci = _getHPDCI()
            items = dci.cmdexec(s).split()
            dci.disconnect()
            dci._testmgr.delete_dci_proc(globals()["__prefixName"])
            return int(items[2].strip('\n').strip('\t').strip(' '))
        #o = MiniClass(1, 1, s)
        #o.initConnection(0)
        #cursor = o.thrdspool[0].cursor()
        #cursor.execute(s)
        #cursor.commit()
        #for d in cursor.description:
        #    for i in d:
        #        print i
        #for row in cursor.fetchall():
        #    for field in row:
        #        print field
        #    print "\n"
        #print cursor.getTypeInfo()
        #print cursor.columns(table = "ODBCTESTTEST_DELETION", catalog = "TRAFODION", schema = "ODBCTEST")
        #print cursor.tables(catalog = "TRAFODION", schema = "ODBCTEST")
        #print cursor.primaryKeys(table = "ODBCTESTTEST_DELETION", catalog = "TRAFODION", schema = "ODBCTEST")
        #print cursor.foreignKeys(table = "ODBCTESTTEST_DELETION", catalog = "TRAFODION", schema = "ODBCTEST")
        #print cursor.procedurecolulmns(table = "ODBCTESTTEST_DELETION", catalog = "TRAFODION", schema = "ODBCTEST")
        #print cursor.procedures(catalog = "TRAFODION", schema = "ODBCTEST")
        #cursor.statistics("ODBCTESTTEST_DELETION", catalog = "TRAFODION", schema = "ODBCTEST")
        #print cursor.fetchone()
        #o.closeConnection(0)
        #del o
        drop_table = "drop table if exists TRAFODION.ODBCTEST.ODBCTESTTEST_DELETION"
        o = MiniClass(1, 1, drop_table)
        o.initConnection(0)
        o.singTrans(0)
        create_table = "create table TRAFODION.ODBCTEST.ODBCTESTTEST_DELETION (\
                t_i largeint generated by default as identity, \
                t_1 char(20) no default not null, \
                t_2 int no default, \
                t_3 smallint not null, \
                t_4 float(52) default -1.7272337110188889e-76, \
                t_5 double precision default -2.2250738585072014e-308 not null, \
                t_6 date default current_date, \
                t_7 time(0) default current_time, \
                t_8 decimal (18, 10) signed default 12345678.1234567890 not null, \
                t_9 largeint default 9.223E18, \
                t_a numeric(128, 0) signed default 12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678 not null, \
                t_b real default -1.1579208e38, \
                t_c interval year(5) to month default NULL, \
                t_d pic xxxxxxxxxxxx display upshift default 'defaULT', \
                t_e character(8) default 'summer', \
                t_f varchar(10) default 'china', \
                t__ timestamp default current_timestamp, \
                primary key(t_i))"
        o.sqlstatement = create_table
        o.singTrans(0)
        o.closeConnection(0)
        del o
        #s = "insert into TRAFODION.ODBCTEST.ODBCTESTTEST_DELETION(t_1, t_2, t_3) values('#deletion', 1111, 99)"
        #s = self.singTransLine(10, 100, s)
        s = "insert into TRAFODION.ODBCTEST.ODBCTESTTEST_DELETION(t_1, t_2, t_3) values('#deletion', 1111, 99), ('#deletion', 1111, 99)"
        e = self.multiTransLineWithLock(10, 100, s)
        rc = getRowCount()
        logging.info("[*] totally insert %d rows." % (rc))
        if rc != 4800:
            e = "Failed"
        logging.info("[*] %s" % (e))
        
        
        
        
        
        return 
        s = "insert into TRAFODION.ODBCTEST.ODBCTESTTEST_DELETION(t_1, t_2, t_3) values('#deletion', 1111, 99), ('#deletion', 1111, 99)"
        s = s + ";"; s = s*10; s = s.rstrip(';')
        e = self.multiTransLineWithLock(48, 5, s)
        rc = getRowCount()
        logging.info("[*] totally insert %d rows." % (rc))
        if rc != 4800:
            e = "Failed"
        logging.info("[*] %s" % (e))
        o = MiniClass(48, 10, '')
        o.bindTypeToGlobalVariable(range(-9, 1, 1))
        s = "delete from TRAFODION.ODBCTEST.ODBCTESTTEST_DELETION where t_i in"
        o.sqlstatement = s
        o.callLoadMultiThreads(o.handleDelStmtSingTranstWithLock)
        rc = getRowCount() 
        logging.info("[*] totally exist %d rows after deletion." % (rc))
        if rc != 0:
            o.status = "Failed"
        logging.info("[*] %s" % (o.status))
        del o
    @unittest.skip("reserved")  
    def testSimpleSelectStatementGroup(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        s = "SELECT * FROM TRAFODION.ODBCTEST.ODBCTESTTEST_PLAIN WHERE USERID='user4202'"
        e = self.singTransLine(24, 3600, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 7200, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 10800, s)
        logging.info("[*] %s" % (e))
        sa = s + ";"; sa = sa*50; sa = sa.rstrip(';')
        e = self.multiTransLine(48, 36, sa)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 72, sa)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 108, sa)
        logging.info("[*] %s" % (e))
        sb = s + ";"; sb = sb*25; sb = sb.rstrip(';')
        e = self.multiTransLine(72, 24, sb)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 48, sb)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 72, sb)
        logging.info("[*] %s" % (e))
    @unittest.skip("reserved")
    def testSimpleUpdateStatementGroup(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        s = "UPDATE TRAFODION.ODBCTEST.ODBCTESTTEST_PLAIN SET FAILCOUNT='0',LOGONDATE='20140606204400',LASTDATE='20140606205408' WHERE USERID='user4202'"
        e = self.singTransLine(24, 3600, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 7200, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 10800, s)
        logging.info("[*] %s" % (e))
        sa = s + ";"; sa = sa*50; sa = sa.rstrip(';')
        e = self.multiTransLine(48, 36, sa)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 72, sa)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 108, sa)
        logging.info("[*] %s" % (e))
        sb = s + ";"; sb = sb*25; sb = sb.rstrip(';')
        e = self.multiTransLine(72, 24, sb)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 48, sb)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 72, sb)
        logging.info("[*] %s" % (e))
    @unittest.skip("reserved")
    def testComplexSelectStatementGroup(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        s = "SELECT * FROM TRAFODION.ODBCTEST.ODBCTESTTEST_PLAIN WHERE USERID LIKE '%10%' UNION ALL SELECT * FROM TRAFODION.ODBCTEST.ODBCTESTTEST_PLAIN WHERE USERID IN('user345', 'user456', 'user567', 'user678', 'user789', 'user999')"
        e = self.singTransLine(24, 3600, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 7200, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 10800, s)
        logging.info("[*] %s" % (e))
        sa = s + ";"; sa = sa*50; sa = sa.rstrip(';')
        e = self.multiTransLine(48, 36, sa)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 72, sa)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 108, sa)
        logging.info("[*] %s" % (e))
        sb = s + ";"; sb = sb*25; sb = sb.rstrip(';')
        e = self.multiTransLine(72, 24, sb)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 48, sb)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 72, sb)
        logging.info("[*] %s" % (e))
    @unittest.skip("reserved")
    def testComplexUpdateStatementGroup(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        s = "UPDATE TRAFODION.ODBCTEST.ODBCTESTTEST_PLAIN SET FAILCOUNT=(CASE WHEN FAILCOUNT='0' THEN '1' WHEN FAILCOUNT='1' THEN '0' END), LOGONDATE='20140303030303', LASTDATE='20141111111111' WHERE USERID='user10000'"
        e = self.singTransLine(24, 3600, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 7200, s)
        logging.info("[*] %s" % (e))
        e = self.singTransLine(24, 10800, s)
        logging.info("[*] %s" % (e))
        sa = s + ";"; sa = sa*50; sa = sa.rstrip(';')
        e = self.multiTransLine(48, 36, sa)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 72, sa)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 108, sa)
        logging.info("[*] %s" % (e))
        sb = s + ";"; sb = sb*25; sb = sb.rstrip(';')
        e = self.multiTransLine(72, 24, sb)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 48, sb)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 72, sb)
        logging.info("[*] %s" % (e))
    @unittest.skip("reserved")
    def testComplexTransactionfromLupin(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        s1 = "SELECT * FROM TRAFODION.ODBCTEST.ODBCTESTTEST_PLAIN WHERE USERID='user4202'"
        s2 = "UPDATE TRAFODION.ODBCTEST.ODBCTESTTEST_PLAIN SET FAILCOUNT='0',LOGONDATE='20140606204400',LASTDATE='20140606205408' WHERE USERID='user4202'"
        s = s1 + ";" + s2
        e = self.multiTransLine(24, 3600, s)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(24, 7200, s)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(24, 10800, s)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 1800, s)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 3600, s)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(48, 5400, s)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 1800, s)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 3600, s)
        logging.info("[*] %s" % (e))
        e = self.multiTransLine(72, 7200, s)
        logging.info("[*] %s" % (e))
    
    #@ttest.skip("reserved")
    def test_0(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        #s = 'select [first 10] left(rtrim(t1.explain_plan), 32768) as "explain_plan_text" from TRAFODION."_REPOS_".metric_query_table as t1'
        s = 'select rtrim(t1.query_id) as "query_id", rtrim(t1.query_text) as "query_text", rtrim(t1.explain_plan) as "explain_plan_text" from TRAFODION."_REPOS_".metric_query_table as t1' 
        o = MiniClass(1, 1, s)
        o.initConnection(0)
        cursor = o.thrdspool[0].cursor()
        cursor.execute(s)
        for i in cursor.fetchall():
            print i
        o.closeConnection(0)
        del o

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=_createLogFile(),
                filemode='w')
    unittest.main()

#!END
