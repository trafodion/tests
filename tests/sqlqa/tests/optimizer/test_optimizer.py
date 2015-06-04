# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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

import tests.optimizer.hcube1.tunit
import tests.optimizer.hcube2.tunit
import tests.optimizer.hcube3.tunit
import tests.optimizer.hcube4.tunit
import tests.optimizer.hcube5.tunit
import tests.optimizer.idxelim.tunit

class TestOptimizer(unittest.TestCase):
    """Legacy Regression Test: optimizer"""

    # @classmethod def setUpClass(cls) and @classmethod def tearDownClass(cls)
    # only work for python 2.7 and 3.2.
    # @classmethod
    # def setUpClass(cls):
    # @classmethod
    # def tearDownClass(cls):

    _testmgr = hpdci.HPTestMgr()

    def __init__(self, *args, **kwargs):
        super(TestOptimizer, self).__init__(*args, **kwargs)
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
    def test_hcube1(self):
        # == GLOBAL TABLES: g_tpch2x
        testlist=[]
        self.run_testunit(tests.optimizer.hcube1.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_hcube2(self):
        # == GLOBAL TABLES: g_hcubedb
        testlist=[]
        self.run_testunit(tests.optimizer.hcube2.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_hcube3(self):
        # == GLOBAL TABLES: g_hcubedb
        testlist=[]
        self.run_testunit(tests.optimizer.hcube3.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_hcube4(self):
        # == GLOBAL TABLES: g_hcubedb
        testlist=[]
        self.run_testunit(tests.optimizer.hcube4.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_hcube5(self):
        # == GLOBAL TABLES: g_hcubedb
        testlist=[]
        self.run_testunit(tests.optimizer.hcube5.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_idxelim(self):
        # == GLOBAL TABLES: g_tpch2x
        testlist=[]
        self.run_testunit(tests.optimizer.idxelim.tunit, testlist)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOptimizer)
    unittest.TextTestRunner(verbosity=2).run(suite)

