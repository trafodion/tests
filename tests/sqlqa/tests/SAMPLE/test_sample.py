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
Python Unittest Sample
"""
import unittest
import ConfigParser
import subprocess
import re
import os

cnxn = 0
scriptPath = os.path.dirname(os.path.realpath(__file__))
Config = ConfigParser.ConfigParser()
Config.read(os.path.abspath(scriptPath + '../../../config.ini'))
dsn = Config.get("pytest","dsn")
usr = Config.get("pytest","usr")
pwd = Config.get("pytest","pwd")
tcp = Config.get("pytest","tcp")
catalog = Config.get("pytest","catalog")
schema = Config.get("pytest","schema")
t4jdbc_classpath = Config.get("pytest","t4jdbc_classpath")
hpdci_classpath = Config.get("pytest","hpdci_classpath")
hpdci_class = Config.get("pytest","hpdci_class")

nvs_classpath = '-classpath ' + t4jdbc_classpath + ':' + hpdci_classpath + " " + hpdci_class
nvs_host = '-h ' + tcp[4:]
nvs_user = '-u ' + usr
nvs_pwd = '-p ' + pwd
nvs_dsn = '-dsn ' + dsn

if (hpdci_class == 'org.trafodion.ci.UserInterface'):
    nvs_full_param = nvs_classpath + " " + nvs_host + " " + nvs_user + " " + nvs_pwd
else:
    nvs_full_param = nvs_classpath + " " + nvs_dsn + " " + nvs_host + " " + nvs_user + " " + nvs_pwd
nvs_call = 'java ' + nvs_full_param + " "

class TestOS(unittest.TestCase):
    """Test Operating System functions"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_SystemCall(self):
        """"Test a unix system call"""
        output = subprocess.check_output(['cat', '/etc/redhat-release'])
        self.assertRegexpMatches(output, 'Red Hat Enterprise .*Santiago', 'ERROR: Redhat release is not Santiago')


class SQL(unittest.TestCase):
    """Test SQL"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_RunHPDCI(self):
        """"Run HPDCI and look for schema USR"""
        output = subprocess.check_output(
            nvs_call + '-q "show schemas;"',
            shell=True,
            stderr=subprocess.STDOUT,
            )
        self.assertIn(schema, output, 'ERROR: Schema ' + schema + ' not found!')


class TestMisc(unittest.TestCase):
    """Test Misc things"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def removeParen(self, str):
        """This function removes parentheses from str

        :param str: A string to be converted
        :returns: String with no parentheses.
        """
        return re.sub('[\(\)]', '', str)

    def test_RemoveParen(self):
        """Test parenthese removal"""
        output = subprocess.check_output(['cat', '/etc/redhat-release'])
        output_noparen = self.removeParen(output)
        self.assertNotRegexpMatches(output_noparen, '[\(\)]', 'ERROR: Found a parentheses where there should be none!')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOS)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(SQL)
    unittest.TextTestRunner(verbosity=2).run(suite)
