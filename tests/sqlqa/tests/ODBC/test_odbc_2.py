# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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

scriptPath = os.path.dirname(os.path.realpath(__file__))
Config = ConfigParser.ConfigParser()
Config.read(os.path.abspath(scriptPath + '../../../config.ini'))
dsn = Config.get("pytest","dsn")
usr = Config.get("pytest","usr")
pwd = Config.get("pytest","pwd")
tcp = Config.get("pytest","tcp")
catalog = Config.get("pytest","catalog")
schema = Config.get("pytest","schema")
hpdci_class = Config.get("pytest","hpdci_class")

class SQLTest(unittest.TestCase):
    """Test cases for SQL using ODBC"""
    def setUp(self):
        connect_str = 'DSN=' + dsn + ';UID=' + usr + ';PWD=' + pwd + ';'
        self.cnxn = pyodbc.connect(connect_str, autocommit=True)
        self.cursor = self.cnxn.cursor()

        try:
            self.cnxn.execute('CREATE SCHEMA ' + catalog + '.' + schema + ';')
        except:
            pass

        self.cnxn.execute('SET SCHEMA ' + catalog + '.' + schema + ';')
        pass

    def tearDown(self):
        try:
            self.cnxn.execute('DROP SCHEMA ' + catalog + '.' + schema + ' CASCADE;')
        except:
            pass

        self.cursor.close()
        self.cnxn.close()
        pass

    def test_FetchByColumnName(self):
        """Test fetching a column by name"""
        try:
            self.cursor.execute('DROP TABLE EMP')
        except:
            pass

        self.cursor.execute('CREATE TABLE EMP (EMPNUM INT NOT NULL, EMPNAME VARCHAR(20), PRIMARY KEY(EMPNUM))')
        self.cursor.execute('INSERT INTO EMP VALUES (20001, \'JACK NIMBLE\')')
        self.cursor.execute('SELECT * FROM EMP')
        found = 0
        while 1:
            row = self.cursor.fetchone()
            if not row:
                break
            if (row.EMPNAME == 'JACK NIMBLE'):
                found = 1
        assert found == 1, 'ERROR: Fetching data using column name failed!'

    def test_PyodbcError(self):
        """Test checking a Pyodbc error"""
        # Use print sys.exc_info() in the except part of the try block to see exactly what exception is being thrown
        with self.assertRaisesRegexp(pyodbc.Error, '.*ERROR.*15001.*A syntax error occurred.*'):
            self.cursor.execute('DRP TABLE PyodbcError')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SQLTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
