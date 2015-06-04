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
    
def test001(desc="""test022"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test022
    # JClear
    # 1999-06-02
    # CJDate tests (5th ed. p172): complicated NOT EXISTS-EXISTS-NOT EXISTS query
    # "Get project numbers for projects such that at least some of every part
    #  they use is supplied to them by supplier S1" Exercise 6.39
    #
    stmt = """select distinct jnum
from spj x
where not exists
(select *
from spj y
where exists
(select *
from spj a
where a.pnum = y.pnum
and a.jnum = x.jnum)
and not exists
(select *
from spj b
where b.snum = 's1'
and b.pnum = y.pnum
and b.jnum = x.jnum));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 0 rows with values
    
    #- select distinct jnum
    #-   from vpspj x
    #-     where not exists
    #-       (select *
    #-          from vpspj y
    #- 	   where exists
    #- 	     (select *
    #- 	        from vpspj a
    #- 		  where a.pnum = y.pnum
    #- 		    and a.jnum = x.jnum)
    #-       and not exists
    #-         (select *
    #- 	   from vpspj b
    #- 	     where b.snum = 's1'
    #- 	       and b.pnum = y.pnum
    #- 	       and b.jnum = x.jnum));
    # expect 0 rows with values
    
    stmt = """select distinct jnum
from hpspj x
where not exists
(select *
from hpspj y
where exists
(select *
from hpspj a
where a.pnum = y.pnum
and a.jnum = x.jnum)
and not exists
(select *
from hpspj b
where b.snum = 's1'
and b.pnum = y.pnum
and b.jnum = x.jnum));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 0 rows with values
    
    _testmgr.testcase_end(desc)

