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

from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""test011"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test011
    # minus.sql
    # jclear
    # 22 Apr 1997
    # Test for the new aggreate functions
    # Tests Variance and StdDev on an integer column with 500 rows
    # of which 251 contain negative values.
    # The results of this test depend on the previous running of
    # the test test010 (distall.sql which creates 10 duplicate rows)
    # generate some negatives
    stmt = """update ints500 
set int500 = -int500
where counter between 125 and 375;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 251)
    
    stmt = """select count (*) from ints500 
where int500 <= 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test011exp""", 'test011b')
    # expect count of 251
    
    stmt = """select
Variance (int500) as "Var",
StdDev (int500) as "StDev"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test011exp""", 'test011c')
    # expect 1 row with the following values:
    #    Var    1.54017417695211E+18
    #    StDev  1241037540.50879
    #
    
    # restore
    stmt = """update ints500 
set int500 = -int500
where counter between 125 and 375;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 251)
    
    stmt = """select count (*) from ints500 
where int500 <= 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test011exp""", 'test011e')
    # expect count of 0
    
    _testmgr.testcase_end(desc)

