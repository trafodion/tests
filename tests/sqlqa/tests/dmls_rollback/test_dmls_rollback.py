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

import tests.dmls_rollback.is2t003.tunit
import tests.dmls_rollback.is2t012.tunit
import tests.dmls_rollback.is2t014.tunit
import tests.dmls_rollback.is2t015.tunit
import tests.dmls_rollback.is2t019.tunit
import tests.dmls_rollback.is2t021.tunit
import tests.dmls_rollback.is2t022.tunit
import tests.dmls_rollback.r21fix.tunit
import tests.dmls_rollback.r23fix.tunit

class TestDmlsRollback(unittest.TestCase):
    """Legacy Regression Test: dmls_rollback"""

    # @classmethod def setUpClass(cls) and @classmethod def tearDownClass(cls)
    # only work for python 2.7 and 3.2.
    # @classmethod
    # def setUpClass(cls):
    # @classmethod
    # def tearDownClass(cls):

    _testmgr = hpdci.HPTestMgr()

    def __init__(self, *args, **kwargs):
        super(TestDmlsRollback, self).__init__(*args, **kwargs)
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
    def test_is2t003(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.dmls_rollback.is2t003.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_is2t012(self):
        # == GLOBAL TABLES: wisc32
        testlist=[]
        self.run_testunit(tests.dmls_rollback.is2t012.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_is2t014(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.dmls_rollback.is2t014.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_is2t015(self):
        # == GLOBAL TABLES: wisc32
        testlist=[]
        self.run_testunit(tests.dmls_rollback.is2t015.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_is2t019(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.dmls_rollback.is2t019.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_is2t021(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.dmls_rollback.is2t021.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_is2t022(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.dmls_rollback.is2t022.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_r21fix(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.dmls_rollback.r21fix.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_r23fix(self):
        # == GLOBAL TABLES: tpch2x
        testlist=[]
        self.run_testunit(tests.dmls_rollback.r23fix.tunit, testlist)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDmlsRollback)
    unittest.TextTestRunner(verbosity=2).run(suite)

