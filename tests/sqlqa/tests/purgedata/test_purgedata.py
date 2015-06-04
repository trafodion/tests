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

import tests.purgedata.purgedata01.tunit
import tests.purgedata.purgedata10.tunit
import tests.purgedata.purgedata13.tunit
import tests.purgedata.purgedata15.tunit
import tests.purgedata.purgedata181.tunit
import tests.purgedata.purgedata182.tunit
import tests.purgedata.purgedata183.tunit
import tests.purgedata.purgedata21.tunit
import tests.purgedata.purgedata23.tunit
import tests.purgedata.purgedata25.tunit
import tests.purgedata.purgedata27.tunit
import tests.purgedata.purgedata29.tunit
import tests.purgedata.purgedata30.tunit
import tests.purgedata.purgedata31.tunit
import tests.purgedata.purgedata32.tunit
import tests.purgedata.purgedata33.tunit

class TestPurgedata(unittest.TestCase):
    """Legacy Regression Test: purgedata"""

    # @classmethod def setUpClass(cls) and @classmethod def tearDownClass(cls)
    # only work for python 2.7 and 3.2.
    # @classmethod
    # def setUpClass(cls):
    # @classmethod
    # def tearDownClass(cls):

    _testmgr = hpdci.HPTestMgr()

    def __init__(self, *args, **kwargs):
        super(TestPurgedata, self).__init__(*args, **kwargs)
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
    def test_purgedata01(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata01.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata10(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata10.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata13(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata13.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata15(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata15.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata181(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata181.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata182(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata182.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata183(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata183.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata21(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata21.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata23(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata23.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata25(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata25.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata27(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata27.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata29(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata29.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata30(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata30.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata31(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata31.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata32(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata32.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_purgedata33(self):
        # == GLOBAL TABLES: g_cmureg
        testlist=[]
        self.run_testunit(tests.purgedata.purgedata33.tunit, testlist)


if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPurgedata)
    unittest.TextTestRunner(verbosity=2).run(suite)

