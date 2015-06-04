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
    
def test001(desc="""test030"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test030
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p175): Nested subquery with aggregate (AVG)
    # Exercise 6.29
    # "Get supplier numbers for suppliers supplying some project with part
    #  P1 in a quantity greater than the average shipment quantity of part
    #  P1 for that project."
    #
    stmt = """select distinct snum
from spj x
where pnum = 'p1'
and qty >
(select avg (qty)
from spj y
where pnum = 'p1'
and y.jnum = x.jnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test030.exp""", 's1')
    # expect 1 row with 's1'
    
    #- select distinct snum
    #-   from vpspj x
    #-     where pnum = 'p1'
    #-       and qty >
    #-         (select avg (qty)
    #- 	   from vpspj y
    #- 	      where pnum = 'p1'
    #- 	        and y.jnum = x.jnum);
    # expect 1 row with 's1'
    
    stmt = """select distinct snum
from hpspj x
where pnum = 'p1'
and qty >
(select avg (qty)
from hpspj y
where pnum = 'p1'
and y.jnum = x.jnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test030.exp""", 's2')
    # expect 1 row with 's1'
    
    _testmgr.testcase_end(desc)

