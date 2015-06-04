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
Python Unittest Using ODBC Part 1
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

class ConnectTest(unittest.TestCase):
    """Test cases to test ODBC connection"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_DSNConnection(self):
        try:
            connect_str = 'DSN=' + dsn + ';UID=' + usr + ';PWD=' + pwd
            print connect_str
            cnxn = pyodbc.connect(connect_str, autocommit=True)
        except Exception,e:
            print str(e)
            assert 0, 'ERROR: DSN Connection failed!'
        else:
            cnxn.close();

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ConnectTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
