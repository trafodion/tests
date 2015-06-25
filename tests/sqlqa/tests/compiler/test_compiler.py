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

import tests.compiler.explain.tunit
import tests.compiler.hbasepart.tunit
import tests.compiler.joinelim.tunit
import tests.compiler.skey.tunit
import tests.compiler.smf1.tunit
import tests.compiler.smf2.tunit
import tests.compiler.smf3.tunit
import tests.compiler.smf4.tunit
import tests.compiler.smf5.tunit
import tests.compiler.unnest.tunit

class TestCompiler(unittest.TestCase):
    """Legacy Regression Test: compiler"""

    # @classmethod def setUpClass(cls) and @classmethod def tearDownClass(cls)
    # only work for python 2.7 and 3.2.
    # @classmethod
    # def setUpClass(cls):
    # @classmethod
    # def tearDownClass(cls):

    _testmgr = hpdci.HPTestMgr()

    def __init__(self, *args, **kwargs):
        super(TestCompiler, self).__init__(*args, **kwargs)
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
    def test_explain(self):
        # == GLOBAL TABLES: g_tpch2x, g_tpcds1x, g_wisc32
        testlist=[]
        self.run_testunit(tests.compiler.explain.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_hbasepart(self):
        # == GLOBAL TABLES: g_tpch2x
        testlist=[]
        self.run_testunit(tests.compiler.hbasepart.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_joinelim(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.compiler.joinelim.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_skey(self):
        # == GLOBAL TABLES: g_tpcds1x
        testlist=[]
        self.run_testunit(tests.compiler.skey.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_smf1(self):
        # == GLOBAL TABLES: g_tpch2x
        testlist=[]
        self.run_testunit(tests.compiler.smf1.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_smf2(self):
        # == GLOBAL TABLES: g_tpcds1x
        testlist=[]
        self.run_testunit(tests.compiler.smf2.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_smf3(self):
        # == GLOBAL TABLES: g_tpcds1x
        testlist=[]
        self.run_testunit(tests.compiler.smf3.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_smf5(self):
        # == GLOBAL TABLES: g_tpcds1x
        testlist=[]
        self.run_testunit(tests.compiler.smf5.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_unnest(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.compiler.unnest.tunit, testlist)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCompiler)
    unittest.TextTestRunner(verbosity=2).run(suite)

