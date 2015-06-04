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
    
def test001(desc="""test031"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test031
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p176): Query with EXISTS & NOT EXISTS
    # Exercise 6.31
    # "Get project numbers from projects using at least one part avaliable
    #  from supplier S1."
    #
    stmt = """select distinct x.jnum
from spj x
where exists
(select *
from spj y
where y.pnum = x.pnum
and y.snum = 's1')
order by x.jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test031.exp""", 's1')
    # expect 2 rows with j1, j4 in order
    
    #- select distinct x.jnum
    #-   from vpspj x
    #-     where exists
    #-       (select *
    #-          from vpspj y
    #- 	   where y.pnum = x.pnum
    #- 	     and y.snum = 's1')
    #- 	       order by x.jnum;
    # expect 2 rows with j1, j4 in order
    
    stmt = """select distinct x.jnum
from hpspj x
where exists
(select *
from hpspj y
where y.pnum = x.pnum
and y.snum = 's1')
order by x.jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test031.exp""", 's2')
    # expect 2 rows with j1, j4 in order
    
    stmt = """select distinct x.jnum
from spj x
where not exists
(select *
from spj y
where y.pnum = x.pnum
and y.snum = 's1')
order by x.jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test031.exp""", 's3')
    # expect 7 rows with j1-7
    
    #- select distinct x.jnum
    #-   from vpspj x
    #-     where not exists
    #-       (select *
    #-          from vpspj y
    #- 	   where y.pnum = x.pnum
    #- 	     and y.snum = 's1')
    #- 	       order by x.jnum;
    # expect 7 rows with j1-7
    
    stmt = """select distinct x.jnum
from hpspj x
where not exists
(select *
from hpspj y
where y.pnum = x.pnum
and y.snum = 's1')
order by x.jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test031.exp""", 's4')
    # expect 7 rows with j1-7
    
    _testmgr.testcase_end(desc)

