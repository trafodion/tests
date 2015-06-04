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

import sys
import unittest
import tests.lib.gvars as gvars
import tests.lib.hpdci as hpdci
# The arguments need to be parsed and saved before importing test modules,
# as they will be used even in defvars.py, which is evaluated as part of
# the import
hpdci.prog_parse_args_from_initfile()

import tests.arkcase.arkcasedb.tunit
import tests.arkcase.arkt0001.tunit
import tests.arkcase.arkt0004.tunit
import tests.arkcase.arkt0008.tunit
import tests.arkcase.arkt0009.tunit
import tests.arkcase.arkt0010.tunit
import tests.arkcase.arkt0013.tunit
import tests.arkcase.arkt0014.tunit
import tests.arkcase.arkt0025.tunit
import tests.arkcase.arkt0030.tunit
import tests.arkcase.arkt0031.tunit
import tests.arkcase.arkt0039.tunit
import tests.arkcase.arkt0041.tunit
import tests.arkcase.arkt0102.tunit
import tests.arkcase.arkt0110.tunit
import tests.arkcase.arkt0121.tunit
import tests.arkcase.arkt0139.tunit
import tests.arkcase.arkt0140.tunit
import tests.arkcase.arkt0142.tunit
import tests.arkcase.arkt0148.tunit
import tests.arkcase.arkt0149.tunit
import tests.arkcase.arkt0151.tunit
import tests.arkcase.arkt0155.tunit
import tests.arkcase.arkt0167.tunit
import tests.arkcase.arkt0168.tunit
import tests.arkcase.arkt0182.tunit
import tests.arkcase.arkt0197.tunit
import tests.arkcase.arkt0199.tunit
import tests.arkcase.arkt0203.tunit
import tests.arkcase.arkt0403.tunit
import tests.arkcase.arkt0409.tunit
import tests.arkcase.arkt0420.tunit
import tests.arkcase.arkt0421.tunit
import tests.arkcase.arkt0422.tunit
import tests.arkcase.arkt0423.tunit
import tests.arkcase.arkt0425.tunit
import tests.arkcase.arkt0426.tunit
import tests.arkcase.arkt0427.tunit
import tests.arkcase.arkt0428.tunit
import tests.arkcase.arkt0429.tunit
import tests.arkcase.arkt0440.tunit
import tests.arkcase.arkt0555.tunit
import tests.arkcase.arkt0556.tunit
import tests.arkcase.arkt1100.tunit
import tests.arkcase.arkt1101.tunit
import tests.arkcase.arkt1102.tunit
import tests.arkcase.arkt1103.tunit
import tests.arkcase.arkt1104.tunit
import tests.arkcase.arkt1105.tunit
import tests.arkcase.arkt1107.tunit
import tests.arkcase.arkt1108.tunit
import tests.arkcase.arkt1109.tunit
import tests.arkcase.arkt1110.tunit
import tests.arkcase.arkt1111.tunit
import tests.arkcase.arkt1112.tunit
import tests.arkcase.arkt1113.tunit
import tests.arkcase.arkt1114.tunit
import tests.arkcase.arkt1116.tunit
import tests.arkcase.arkt1117.tunit
import tests.arkcase.arkt1198.tunit
import tests.arkcase.arkt1199.tunit
import tests.arkcase.arkt1370.tunit
import tests.arkcase.arkt1371.tunit
import tests.arkcase.arkt1372.tunit
import tests.arkcase.arkt1373.tunit
import tests.arkcase.arkt1374.tunit
import tests.arkcase.arkt1375.tunit
import tests.arkcase.arkt1376.tunit
import tests.arkcase.arkt1377.tunit
import tests.arkcase.arkt1422.tunit
import tests.arkcase.arkt1424.tunit
import tests.arkcase.arkt1510.tunit
import tests.arkcase.arkt1511.tunit
import tests.arkcase.datarith.tunit
import tests.arkcase.datecast.tunit
import tests.arkcase.dateurus.tunit
import tests.arkcase.extract.tunit
import tests.arkcase.nistdml.tunit
import tests.arkcase.nonjoin.tunit
import tests.arkcase.timeprec.tunit
import tests.arkcase.year2000.tunit

class TestArkcase(unittest.TestCase):
    """Legacy Regression Test: arkcase"""

    # @classmethod def setUpClass(cls) and @classmethod def tearDownClass(cls)
    # only work for python 2.7 and 3.2.
    # @classmethod
    # def setUpClass(cls):
    # @classmethod
    # def tearDownClass(cls):

    _testmgr = hpdci.HPTestMgr()
   
    def __init__(self, *args, **kwargs):
        super(TestArkcase, self).__init__(*args, **kwargs)
        pass

    def setUp(self):
        # arkcasedb used to be set up as a set of global tables.  Before we 
        # figure out what to do with global tables in Trafodion testing, let's
        # set them up if they don't exist when running any test in this suite.
        stmt = """select count(*) from """ + gvars.g_schema_arkcasedb + ".BTA1P009;"
        output = self._testmgr.exec_dci_with_one_stmt(stmt)
        if """ERROR""" in output:
           testlist=[]
           self.run_testunit(tests.arkcase.arkcasedb.tunit, testlist)
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
    def test_arkt0001(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0001.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0004(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0004.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0008(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0008.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0009(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0009.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0010(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0010.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0013(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0013.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0014(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0014.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0025(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0025.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0030(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0030.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0031(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0031.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0039(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0039.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0041(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0041.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0102(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0102.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0110(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0110.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0121(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0121.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0139(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0139.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0140(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0140.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0142(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0142.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0148(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0148.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0149(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0149.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0151(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0151.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0155(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0155.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0167(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0167.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0168(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0168.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0182(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0182.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0197(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0197.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0199(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0199.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0203(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0203.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0403(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0403.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0409(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0409.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0420(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0420.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0421(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0421.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0422(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0422.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0423(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0423.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0425(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0425.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0426(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0426.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0427(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0427.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0428(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0428.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0429(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0429.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0440(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0440.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0555(self):
        # == NO GLOBAL TABLES, but use jdbc data loader
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0555.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt0556(self):
        # == NO GLOBAL TABLES, but use jdbc data loader
        testlist=[]
        self.run_testunit(tests.arkcase.arkt0556.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1100(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1100.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1101(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1101.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1102(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1102.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1103(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1103.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1104(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1104.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1105(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1105.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1107(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1107.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1108(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1108.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1109(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1109.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1110(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1110.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1111(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1111.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1112(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1112.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1113(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1113.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1114(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1114.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1116(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1116.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1117(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1117.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1198(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1198.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1199(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1199.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1370(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1370.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1371(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1371.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1372(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1372.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1373(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1373.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1374(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1374.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1375(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1375.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1376(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1376.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1377(self):
        # == GLOBAL TABLES: g_arkcasedb
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1377.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1422(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1422.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1424(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1424.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1510(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1510.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_arkt1511(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.arkt1511.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_datarith(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.datarith.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_datecast(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.datecast.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_dateurus(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.dateurus.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_extract(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.extract.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_nistdml(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.nistdml.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_nonjoin(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.nonjoin.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_timeprec(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.timeprec.tunit, testlist)

    # @unittest.skip('skip this test')
    def test_year2000(self):
        # == NO GLOBAL TABLES
        testlist=[]
        self.run_testunit(tests.arkcase.year2000.tunit, testlist)


if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestArkcase)
    unittest.TextTestRunner(verbosity=2).run(suite)

