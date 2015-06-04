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
    
def test001(desc="""test036"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test036
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p176): EXISTS with nested NOT EXISTSs
    # Exercise 6.36
    # "Get project numbers for projects with at least all parts available
    #  from supplier S1."
    #
    stmt = """select distinct jnum
from spj x
where not exists
(select pnum
from spj y
where y.snum = 's1'
and not exists
(select *
from spj z
where z.pnum = y.pnum
and z.jnum = x.jnum))
order by jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test036.exp""", 's1')
    # expext 2 ordered rows with values j1 j4
    
    #- select distinct jnum
    #-   from vpspj x
    #-     where not exists
    #-       (select pnum
    #-          from vpspj y
    #- 	   where y.snum = 's1'
    #- 	     and not exists
    #- 	       (select *
    #- 	          from vpspj z
    #- 		    where z.pnum = y.pnum
    #- 		      and z.jnum = x.jnum))
    #- 		        order by jnum;
    # expext 2 ordered rows with values j1 j4
    
    stmt = """select distinct jnum
from hpspj x
where not exists
(select pnum
from hpspj y
where y.snum = 's1'
and not exists
(select *
from hpspj z
where z.pnum = y.pnum
and z.jnum = x.jnum))
order by jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test036.exp""", 's2')
    # expext 2 ordered rows with values j1 j4
    
    _testmgr.testcase_end(desc)

