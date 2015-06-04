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

import unittest
import tests.lib.hpdci as hpdci
# The arguments need to be parsed and saved before importing test modules,
# as they will be used even in defvars.py, which is evaluated as part of
# the import
hpdci.prog_parse_args_from_initfile()

import tests.olap.olap.tunit
import tests.olap.olap2.tunit

class TestAddcolperf(unittest.TestCase):
    """Regression Test: olap"""

    # @classmethod def setUpClass(cls) and @classmethod def tearDownClass(cls)
    # only work for python 2.7 and 3.2.
    # @classmethod
    # def setUpClass(cls):
    # @classmethod
    # def tearDownClass(cls):

    _testmgr = hpdci.HPTestMgr()

    def __init__(self, *args, **kwargs):
        super(TestAddcolperf, self).__init__(*args, **kwargs)
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
    def test_olap(self):
        # GLOBAL TABLES: g_tpch2x, g_wisc32, g_tpcds1x
        testlist=[]
        self.run_testunit(tests.olap.olap.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_olap2(self):
        # GLOBAL TABLES: g_tpch2x, g_wisc32, g_tpcds1x
        testlist=[]
        self.run_testunit(tests.olap.olap2.tunit, testlist)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddcolperf)
    unittest.TextTestRunner(verbosity=2).run(suite)