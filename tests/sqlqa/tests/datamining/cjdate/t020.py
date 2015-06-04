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
    
def test001(desc="""test020"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test020
    # JClear
    # 1999-06-02
    # CJDate tests (5th ed. p171): v. complicated NOT EXISTS query
    # "Get project numbers for projects that use only parts that are
    #  available from supplier S1" Exercise 6.37
    #
    stmt = """select distinct jnum
from spj x
where not exists
(select *
from spj y
where y.jnum = x.jnum
and not exists
(select *
from spj z
where z.pnum = y.pnum
and z.snum = 's1'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 0 rows
    
    #- select distinct jnum
    #-   from vpspj x
    #-     where not exists
    #-       (select *
    #-          from vpspj y
    #- 	   where y.jnum = x.jnum
    #- 	     and not exists
    #- 	       (select *
    #- 	          from vpspj z
    #- 		    where z.pnum = y.pnum
    #- 		      and z.snum = 's1'));
    # expect 0 rows
    
    stmt = """select distinct jnum
from hpspj x
where not exists
(select *
from hpspj y
where y.jnum = x.jnum
and not exists
(select *
from hpspj z
where z.pnum = y.pnum
and z.snum = 's1'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 0 rows
    
    _testmgr.testcase_end(desc)

