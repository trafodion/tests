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

import unittest
import tests.lib.hpdci as hpdci
# The arguments need to be parsed and saved before importing test modules,
# as they will be used even in defvars.py, which is evaluated as part of
# the import
hpdci.prog_parse_args_from_initfile()

import tests.groupby.grpby001.tunit
import tests.groupby.grpby002.tunit
import tests.groupby.grpby003.tunit
import tests.groupby.grpby004.tunit
import tests.groupby.grpby005.tunit
import tests.groupby.grpby006.tunit
import tests.groupby.grpby007.tunit
import tests.groupby.grpby008.tunit
import tests.groupby.grpby009.tunit
import tests.groupby.grpby010.tunit
import tests.groupby.grpby011.tunit
import tests.groupby.grpby012.tunit

class TestGroupby(unittest.TestCase):
    """Legacy Regression Test: groupby"""

    # @classmethod def setUpClass(cls) and @classmethod def tearDownClass(cls)
    # only work for python 2.7 and 3.2.
    # @classmethod
    # def setUpClass(cls):
    # @classmethod
    # def tearDownClass(cls):

    _testmgr = hpdci.HPTestMgr()

    def __init__(self, *args, **kwargs):
        super(TestGroupby, self).__init__(*args, **kwargs)
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def run_testunit(self, testunit, testlist=[]):
        try:
           self._testmgr.testunit_begin(testunit)
           testunit.sq_testunit(self._testmgr, testlist)
           status = self._testmgr.testunit_end(testunit)
        except:
           # kill all hpdci processes
           self._testmgr.delete_all_dci_procs()
           raise

        self.assertTrue(status, '*** MISMATCH(es) *** found')

    # NOTE @unittest.skip('skip this test') only work for python 2.7 

    # @unittest.skip('skip this test')
    def test_grpby001(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.groupby.grpby001.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby002(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby002.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby003(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby003.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby004(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby004.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby005(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby005.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby006(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby006.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby007(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby007.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby008(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby008.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby009(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby009.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby010(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby010.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby011(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby011.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_grpby012(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.groupby.grpby012.tunit, testlist)


if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGroupby)
    unittest.TextTestRunner(verbosity=2).run(suite)

