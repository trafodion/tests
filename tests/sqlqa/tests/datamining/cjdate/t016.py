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
    
def test001(desc="""test016"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test016
    # JClear
    # 1999-06-02
    # CJDate tests (5th ed. p162): subquery with NOT EXISTS
    # "Get supplier numbers for suppliers who supply at least all
    #  those parts supplied by S2"
    #
    stmt = """select distinct snum
from spj x
where not exists
(select *
from spj y
where snum = 's2'
and not exists
(select *
from spj z
where z.snum = x.snum
and z.pnum = y.pnum))
order by snum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test016.exp""", 's1')
    # expect 2 ordered rows with values s2 & s5
    
    #- select distinct snum
    #-   from vpspj x
    #-     where not exists
    #-       (select *
    #-          from vpspj y
    #- 	   where snum = 's2'
    #- 	     and not exists
    #- 	       (select *
    #- 	          from vpspj z
    #- 		    where z.snum = x.snum
    #- 		      and z.pnum = y.pnum))
    #- 		        order by snum;
    # expect 2 ordered rows with values s2 & s5
    
    stmt = """select distinct snum
from hpspj x
where not exists
(select *
from hpspj y
where snum = 's2'
and not exists
(select *
from hpspj z
where z.snum = x.snum
and z.pnum = y.pnum))
order by snum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test016.exp""", 's2')
    # expect 2 ordered rows with values s2 & s5
    
    _testmgr.testcase_end(desc)

