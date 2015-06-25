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



"""
Python Unittest Using ODBC Part 2
"""
import unittest
import pyodbc 
import ConfigParser
import os
import datetime
import exceptions

#from ..lib import tstest
import tests.lib.tstest as tstest

local_dir = tstest.my_test_dir(__name__)
local_file = tstest.my_test_file(__name__)

def setUpModule():
    print "enter setUpModule..."

def tearDownModule():
    print "enter tearDownModule..."

class SQLTest(unittest.TestCase):
    """Test cases for SQL using ODBC"""

    #_odbc = None
    #_odbc2 = None

    @classmethod
    def setUpClass(self):
        print "enter setupClass..."

    @classmethod
    def tearDownClass(self):
        print "enter tearDownClass..."

    def setUp(self):
        print "\nenter setUp..."

        self._odbc = tstest.tsodbc(local_file)
        self._odbc.connect()

        self._log_file = tstest.openLogFile(local_file, self.id())
        self._odbc.setLogFile(self._log_file)

    def tearDown(self):
        print "enter tearDown..."

        self._odbc.disconnect()
        tstest.closeLogFile(self._log_file)

    def test_FetchByColumnName(self):
        """Test fetching a column by name"""
        print ''

        stmt = 'SET SCHEMA HSU1;'
        self._odbc.expect_complete(stmt);

        stmt = 'DROP TABLE EMP'
        self._odbc.ignore_complete(stmt)

        stmt = 'CREATE TABLE EMP (EMPNUM INT NOT NULL, EMPNAME VARCHAR(20), PRIMARY KEY(EMPNUM))'
        self._odbc.expect_complete(stmt);

        stmt = 'INSERT INTO EMP VALUES (20001, \'JACK NIMBLE\')'
        self._odbc.expect_insert(stmt, 1);

        stmt = 'INSERT INTO EMP VALUES (30001, \'JOHN SMITH\'), (40001, \'ADAM SMITH\')'
        self._odbc.expect_insert(stmt, 2);

        stmt = 'DELETE FROM EMP WHERE EMPNUM = 40001'
        self._odbc.expect_delete(stmt, 1);

        stmt = 'UPDATE EMP SET EMPNAME = \'FRANK SMITH\' WHERE EMPNUM = 30001'
        self._odbc.expect_update(stmt, 1);

        stmt = 'SELECT * FROM EMP'
        self._odbc.expect_select(stmt, 2);

        stmt = 'SELECT * FROM EMPTABLE'
        self._odbc.expect_error_msg(stmt, 8822);
        #self._odbc.expect_error_msg(stmt, 8800);

        stmt = 'SELECT * FROM EMPTABLE'
        self._odbc.unexpect_error_msg(stmt, 8800);

        stmt = 'SELECT * FROM EMP'
        self._odbc.expect_any_substr(stmt, 'FRANK SMITH');

        stmt = 'SELECT * FROM EMP'
        self._odbc.expect_any_substr(stmt, 'FRANK S.{1}ITH', is_regex=True);

        stmt = 'SHOWDDL EMP'
        self._odbc.expect_any_substr(stmt, 'CREATE TABLE *.EMP', False);

        stmt = 'SHOWDDL EMP'
        self._odbc.unexpect_any_substr(stmt, 'CREATE TABLE EMP', False);

        stmt = 'SELECT * FROM EMP'
        self._odbc.expect_file(stmt, 'exp/a1exp', 's01');

        stmt = 'SHOWDDL EMP'
        self._odbc.expect_file(stmt, 'exp/a2exp', 's01', False);


    def test_GetTables(self):
        """Test get tables"""

        stmt = 'SET SCHEMA HSU1;'
        self._odbc.expect_complete(stmt);

        stmt = 'GET TABLES'
        self._odbc.expect_complete(stmt);

    def not_test_warnings(self):
        """Test SQL statement return warnings"""

        self._odbc.expect_complete('SET SCHEMA TRAFODION.HSU1;')
        self._odbc.expect_complete("cqd AUTO_QUERY_RETRY_WARNINGS 'ON'")
        self._odbc.expect_complete("cqd query_cache '0'")
        self._odbc.expect_complete("cqd query_cache reset")

        self._odbc.expect_warning_msg("create table t001 (a int not null, b int not null,primary key(a)) attribute blocksize 4096", 3250)
        self._odbc.expect_complete("insert into t001 values (101,50),(102,5),(103,20)")
        self._odbc.expect_complete("drop table t001")
        self._odbc.expect_complete("create table t001 (a int not null, b int not null,primary key(a))")
        self._odbc.expect_warning_msg("insert into t001 values (101,50),(102,5),(103,20)")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SQLTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
