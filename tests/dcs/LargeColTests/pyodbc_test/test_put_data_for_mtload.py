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
    
    FileName: sys.argv[0]
    Description: This script is purposed to init data in order to test mtload, depends an outer SQL script file which includes all commands of initialized data. 
    CreatedTime: 2014.x
    LastModifiedTime: 2014.x
'''
import tests.lib.gvars as gvars
import tests.lib.hpdci as hpdci
hpdci.prog_parse_args_from_initfile()
import sys
import os
import re
import unittest
import threading
import ConfigParser

'''
    
    Define all global variables for this script, we also can read connection parameters from a configuration file.
'''
_testmgr, _dci1 = None, None
_sql_script_file = os.path.dirname(__file__) + ('/Users_icewall_PLAIN_25k.sql')
_name, _target, _dsn, _user, _pass = 'user', 'targetIP', 'MYTRAFDSN', 'userid', 'passwd'
_clone_name =  'CLONE_SQL'
_count_rows = "SELECT COUNT(*) FROM TRAFODION.ODBCTEST.ODBCTESTTEST_PLAIN;\n"
_f = "" + os.path.dirname(os.path.realpath(__file__)) + "/insert_finished_for_mtload.log"
_rows = 25000
_threads = list()

'''
   
    Init _dci1 variable, Colone _dci1 as _dci2
'''
if _testmgr is None:
    _testmgr = hpdci.HPTestMgr()

assert _testmgr is not None

if _dci1 is None:
    _dci1 = _testmgr.create_dci_proc(_name, _target, _dsn, _user, _pass)

assert _dci1 is not None

'''
    
    Define a subclass MtLoadTestCase of unittest.TestCase
'''
class MtLoadTestCase(unittest.TestCase):
    '''
        
        class name: self.__class__.__name__
        class description: This class is based on the framework of unit test.TestCase, the whole test process is simple, only on case is used to execut SQL command to init data for mtload.
    '''
    
    '''
        
        @setUp()
    '''
    def setUp(self):
        pass
    
    '''
        
        @tearDown()
    '''
    def tearDown(self):
        pass
    
    '''
        
        @testSqlScriptFile(), no assertion
    '''
    def testSqlScriptFile(self):
        global _testmgr, _dci1
        
        if os.path.exists(globals()["_f"]):
            if os.path.isfile(globals()["_f"]):
                os.remove(globals()["_f"])
        
        flag = False
        items = _dci1.cmdexec(globals()["_count_rows"]).split()
        
        for i in items:
            if i.find(str(globals()["_rows"])) == -1:
                continue
            else:
                flag = True
                break
        
        if not flag:
            _dci1.cmdexec("@" + globals()["_sql_script_file"] + "\n")
            
            while not os.path.exists(globals()["_f"]):
                _dci1.cmdexec(";\n")
        
        try:
             _testmgr.delete_dci_proc(globals()["_name"])
        except:
            pass
        
'''
    
    @main()
'''
if __name__ == "__main__":
    suite = unittest.TestSuite()
    _threads.append(threading.Thread(target=suite.addTest, args=[MtLoadTestCase("testSqlScriptFile"), ]))
    for thread in _threads:
        thread.start()
    for thread in _threads:
        thread.join()
    unittest.TextTestRunner().run(suite)
    _testmgr = None

#!END
